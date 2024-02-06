import json
import os.path
import string
import termcolor
import torch
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sentence_transformers import SentenceTransformer, util
from termcolor import colored


class Hint_Filtering:

    def __init__(self, model):
        self.device = "cuda:0" if torch.cuda.is_available() else "cpu"
        self.model = SentenceTransformer('all-mpnet-base-v2').to(self.device)

        nltk.download('stopwords')
        nltk.download('punkt')
        nltk.download('wordnet')
        nltk.download('omw-1.4')
        self.model_name = model

        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()

    def _clear_question(self, sent: str):
        if sent.startswith('"'):
            sent = sent.replace('""', "\"")
            sent = sent[1:-1]
        elif sent.startswith(('‘', '\'', '“')):
            sent = sent.replace(sent[0], '"').replace('’', '"')
        return sent

    def _clear_answer(self, sent: str):
        if sent.startswith('"'):
            sent = sent.replace('"""', "\"")
            sent = sent[1:-1]
        elif sent.startswith(('‘', '“')):
            sent = sent[1:-1]
        elif sent.startswith('\'') and sent.endswith('\''):
            sent = sent[1:-1]
        return sent.strip()

    def _clear_hint(self, sent: str):
        if sent.find('Is there anything else you would like to know?') >= 0:
            sent = sent.replace('Is there anything else you would like to know?', '') \
                .replace('😊', '').replace(' .', '').strip()
        if sent.find('I hope these hints help you guess the answer!') >= 0:
            sent = sent.replace('I hope these hints help you guess the answer!', '') \
                .replace('😊', '').replace(' .', '').strip()
        if sent == '"':
            sent = ''
        if sent.find('😊') >= 0:
            sent = sent.replace('😊', '')
        if sent.startswith('.'):
            sent = ''
        sent = sent.strip()

        return None if sent == '' else sent

    def _include_answer(self, idx, question, hint_original, answer):
        hint = hint_original.lower()
        hint_tokens = word_tokenize(hint)
        hint = [self.lemmatizer.lemmatize(w) for w in hint_tokens]

        word_tokens = word_tokenize(answer)
        filtered_answer = [self.lemmatizer.lemmatize(w).lower() for w in word_tokens if
                           not w.lower() in self.stop_words and w not in string.punctuation and w != '\'s']
        found = False
        for split in filtered_answer:
            if split in hint and not found:
                found = True
                print()
                print(idx, ':', termcolor.colored(question, 'light_blue'))
                print(hint_original)
            if split in hint:
                print(answer, ':', termcolor.colored(split, 'red'))
        return found

    def _question_hint_similarity(self, question, hints):
        emb1 = self.model.encode(question)
        emb2 = self.model.encode(hints)
        cos_sim = util.cos_sim(emb1, emb2)
        result = list(zip(hints, cos_sim[0].numpy()))
        return result

    def filtering(self):
        print(colored('Hint Filtering:', attrs=['bold', 'underline']))
        with open(f'./outputs/question_type/{self.model_name}.json', mode='r', encoding='utf-8') as f:
            hints = json.load(f)

        cleared_hints = []
        if os.path.exists(f'./outputs/hints_filtered/{self.model_name}.json'):
            with open(f'./outputs/hints_filtered/{self.model_name}.json', mode='r', encoding='utf8') as f:
                cleared_hints = json.load(f)

        for idx, rec in enumerate(hints, 1):
            if idx <= len(cleared_hints):
                continue
            if rec['MajorType'] == 'DESC:DESCRIPTION':
                print(f'\"{rec["Question"]}\" was deleted because it is not a factoid question.')
                continue
            question: str = rec['Question']
            exact_answer: str = rec['ExactAnswer']
            if not question.startswith(tuple(string.ascii_letters)):
                question = self._clear_question(question)
            if not exact_answer.startswith(tuple(string.ascii_letters)):
                exact_answer = self._clear_answer(exact_answer)

            new_hints = []

            for hint in rec['Hints']:
                hint = self._clear_hint(hint)
                if hint is not None:
                    new_hints.append(hint)

            if len(new_hints) == 0:
                continue

            q_h_sim = self._question_hint_similarity(question, new_hints)
            new_hints = [hint[0] for hint in q_h_sim if hint[1] < 0.72]

            new_hints_temp = []
            for hint in new_hints:
                is_included = self._include_answer(idx, question, hint, exact_answer)
                if not is_included:
                    new_hints_temp.append(hint)
            new_hints = new_hints_temp.copy()

            new_rec = {key: value for key, value in rec.items()}
            new_rec.update({'Question': question, 'Hints': new_hints, 'ExactAnswer': exact_answer})
            cleared_hints.append(new_rec)

        cleared_hints_temp = []
        for rec in cleared_hints:
            cleared_hints_temp.append(rec)
        cleared_hints = cleared_hints_temp.copy()

        with open(f'./outputs/hints_filtered/{self.model_name}.json', mode='w', encoding='utf-8') as f:
            json.dump(cleared_hints, f)
