import json
import os

import openai
import shutil
import os.path as path
from tqdm import tqdm
from utils.Hint_Generation.Question_Classification import QC
from utils.Hint_Generation.Hint_Filtering import Hint_Filtering
from termcolor import colored


class Hint_Generation:
    def __init__(self, base_url, api_key, model):
        _models = {'LLaMA_7b_Vanilla': 'meta-llama/Llama-2-7b-chat-hf',
                   'LLaMA_7b_Finetuned': 'meta-llama/Llama-2-7b-chat-hf:Hint_Generator:X6odC0D',
                   'LLaMA_13b_Vanilla': 'meta-llama/Llama-2-13b-chat-hf',
                   'LLaMA_13b_Finetuned': 'meta-llama/Llama-2-13b-chat-hf:Hint_Generator:ajid9Dr',
                   'LLaMA_70b_Vanilla': 'meta-llama/Llama-2-70b-chat-hf',
                   'LLaMA_70b_Finetuned': 'meta-llama/Llama-2-70b-chat-hf:Hint_Generator:NispySP'
                   }

        self.client = openai.OpenAI(
            base_url=base_url,
            api_key=api_key)
        self.model_name = model
        self.model_link = _models[model]

    @staticmethod
    def _clear_candidate(prompt_content):
        candidate_raw: list = prompt_content.strip().split('\n')
        if len(candidate_raw) > 1 and candidate_raw[1] == '':
            cleared_candidate = candidate_raw[2:]
        else:
            cleared_candidate = candidate_raw

        if len(cleared_candidate) > 1 and cleared_candidate[-2] == '':
            cleared_candidate = cleared_candidate[:-2]
        else:
            cleared_candidate = cleared_candidate

        for i in range(len(cleared_candidate)):
            can = cleared_candidate[i]
            start_chars = ('-', '•', '*', '1', '2', '3', '4', '5', '6', '7', '8', '9')
            if can.strip().startswith(start_chars):
                if can.strip().startswith('10'):
                    can = can[3:].strip()
                else:
                    can = can[2:].strip()
            if can.strip().startswith('\"'):
                can = can.strip()[1:-1]
            cleared_candidate[i] = can
        return cleared_candidate

    def _execute_prompt(self, messages):
        result = self.client.chat.completions.create(
            model=self.model_link,
            messages=messages,
            temperature=0,
            top_p=1,
            max_tokens=512
        )
        return result.choices[0].message.content

    def _generate_hints(self):
        if not path.exists(f'./outputs/hints/{self.model_name}.json'):
            shutil.copy('./questions/questions.json', f'./outputs/hints/{self.model_name}.json')
        with open(f'./outputs/hints/{self.model_name}.json', mode='r', encoding='utf8') as f:
            questions = json.load(f)
        for rec in tqdm(questions, total=len(questions), desc=colored('Generating Hints', attrs=['bold', 'underline'])):
            if 'Hints' in rec:
                continue
            while True:
                try:
                    question = rec['Question']
                    exact_answer = rec['ExactAnswer']
                    messages = [{"role": "system",
                                 "content": "You are a helpful assistant that generates hints for user questions. You are given the question, and your goal is to generate hints for the question."},
                                {"role": "user",
                                 "content": "Generate 10 hints for the following question without using \"{}\" word in the hints. Question: {}".format(
                                     exact_answer, question)}]
                    hints = self._execute_prompt(messages)
                    hints = self._clear_candidate(hints)
                    rec['Hints'] = hints
                    break
                except KeyboardInterrupt:
                    exit(0)
                except:
                    pass
            with open(f'./outputs/hints/{self.model_name}.json', mode='w', encoding='utf8') as f:
                json.dump(questions, f)

    def _question_type_labeler(self):
        with open(f'./outputs/hints/{self.model_name}.json', mode='r', encoding='utf8') as f:
            questions = json.load(f)
        batch_size = 128
        questions_batches = [questions[idx: idx + batch_size] for idx in range(0, len(questions), batch_size)]
        for batch in tqdm(questions_batches, desc=colored('Question Type Labelling', attrs=['bold', 'underline'])):
            if all(['MajorType' in q for q in batch]):
                continue
            self.qc = QC(batch_size)
            questions_batch_string = [q['Question'] for q in batch]
            qc_labels = self.qc.get_question_label(questions_batch_string)
            for q, q_class in zip(batch, qc_labels):
                q['MajorType'] = q_class['major_type']
                if q['MajorType'] in ['NUM:NUMERIC', 'ABBR:ABBREVIATION']:
                    q['MajorType'] = 'OTH:OTHER'
                q['MinorType'] = q_class['minor_type']

        questions = []
        for batch in questions_batches:
            questions.extend(batch)
        with open(f'./outputs/question_type/{self.model_name}.json', mode='w', encoding='utf8') as f:
            json.dump(questions, f)

    def _hint_filtering(self):
        hint_filtering = Hint_Filtering(self.model_name)
        hint_filtering.filtering()

    def generate(self):
        ############################################
        if not path.exists('./outputs/hints'):
            os.mkdir('./outputs/hints')
        self._generate_hints()
        ############################################
        if not path.exists('./outputs/question_type'):
            os.mkdir('./outputs/question_type')
        self._question_type_labeler()
        ############################################
        if not os.path.exists('./outputs/hints_filtered'):
            os.mkdir('./outputs/hints_filtered')
        self._hint_filtering()
        ############################################
