import json
import os.path
from termcolor import colored
from openai import OpenAI


class Can_Ans_Generator:
    def __init__(self, base_url, api_key, model):
        with open(f'./outputs/hints-popularity/{model}.json', mode='r', encoding='utf8') as f:
            self.generated_hints = json.load(f)
        self.len_of_questions = len(self.generated_hints)
        self.api_key = api_key
        self.base_url = base_url
        self.model = model
        self.candidate_number = 11
        self.client = OpenAI(base_url=base_url, api_key=api_key)

    def _execute_prompt(self, messages):
        model = 'meta-llama/Llama-2-70b-chat-hf:Hint_Generator:NispySP'
        result = self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0,
            top_p=1,
            max_tokens=512
        )
        return result.choices[0].message.content.strip()

    @staticmethod
    def _clear_candidate(candidate):
        candidate_raw: list = candidate.strip().split('\n')
        if len(candidate_raw) > 1 and candidate_raw[1] == '':
            cleared_candidate = candidate_raw[2:]
        else:
            cleared_candidate = candidate_raw

        if len(cleared_candidate) == 1:
            can: str = cleared_candidate[0]
            start_chars = ('-', '•', '*')
            if can.strip().startswith(start_chars):
                can = can[1:].strip()
            if can.strip().startswith('\"'):
                can = can.strip()[1:-1]
            cleared_candidate[0] = can
        return '\n'.join(cleared_candidate)

    def _generate_candidate_list(self, prompt_content):
        candidate_answers_raw: list = prompt_content.strip().split('\n')
        candidate_answers = []
        for candidate in candidate_answers_raw:
            candidate: str = candidate.strip()
            if candidate == '':
                break
            candidate_answers.append(self._clear_candidate(candidate))
        return candidate_answers

    def _question_prompt(self, question, exact_answer):
        candidate_answers = dict()
        candidate_answers[exact_answer] = 1

        question_prompt = 'Write a most-expected candidate answer for the following question that is not included in the following list. Write the only candidate answer as a bullet without using sentences.\nQuestion: {}\n\n{}'.format(
            question, '\n'.join(candidate_answers.keys()))
        question_messages = [{"role": "user", "content": question_prompt}]
        candidate_answer_raw = self._clear_candidate(self._execute_prompt(question_messages))
        candidate_answers[candidate_answer_raw] = 2
        extend_messages = question_messages.copy()
        extend_messages.append({"role": "assistant", "content": candidate_answer_raw})

        while len(candidate_answers.keys()) < self.candidate_number:
            try:
                extend_prompt = 'Write another candidate answer, WITHOUT any description, for the following question that is not included in the following list.\nQuestion: {}\n\n{}'.format(
                    question, '\n'.join(candidate_answers.keys()))
                extend_messages.append({"role": "user", "content": extend_prompt})
                candidate_answer_raw = self._execute_prompt(extend_messages)
                cleaned_candidate = self._clear_candidate(candidate_answer_raw)
                extend_messages.append({"role": "assistant", "content": candidate_answer_raw})
                candidate_answers[cleaned_candidate] = len(candidate_answers.keys()) + 1
            except:
                break

        del candidate_answers[exact_answer]

        extend_prompt = 'Rewrite the following list in a bullet list. DO NOT write (correct) or (correct answer).\n\n{}'.format(
            '\n'.join(candidate_answers.keys()))
        extend_messages = extend_messages[:(self.candidate_number-1)*2]
        extend_messages.append({"role": "user", "content": extend_prompt})
        extend_messages = [{"role": "user", "content": extend_prompt}]
        candidate_answer_old_raw = self._execute_prompt(extend_messages)
        candidate_answers_old = self._clear_candidate(candidate_answer_old_raw)
        candidate_answers_old = self._generate_candidate_list(candidate_answers_old)

        extend_prompt = 'Add "{}" to the following list and Write the updated list in a bullet list. DO NOT write (correct) or (correct answer).\n\n{}'.format(
            exact_answer, '\n'.join(candidate_answers_old))
        extend_messages = extend_messages[:(self.candidate_number-1)*2]
        extend_messages.append({"role": "user", "content": extend_prompt})
        candidate_answer_raw = self._execute_prompt(extend_messages)
        candidate_answers = self._clear_candidate(candidate_answer_raw)
        candidate_answers = self._generate_candidate_list(candidate_answers)

        new_exact_answer = [key for key in candidate_answers if key not in candidate_answers_old]
        if len(new_exact_answer) > 0:
            candidate_answers.remove(new_exact_answer[0])
            candidate_answers.append(new_exact_answer[0])
            return {'Candidate_Question': candidate_answers, 'Exact_Answer': new_exact_answer[0]}
        else:
            new_item = candidate_answers.pop(0)
            candidate_answers.append(new_item)
            new_exact_answer.append(new_item)
            return {'Candidate_Question': candidate_answers, 'Exact_Answer': new_exact_answer[0]}

    def generate_candidate_answers(self):
        candidate_answer_test_set = []
        questions_with_problem = []
        if os.path.exists(f'./outputs/hints-candidates/{self.model}.json'):
            with open(f'./outputs/hints-candidates/{self.model}.json', mode='r',
                      encoding='utf8') as f:
                candidate_answer_test_set = json.load(f)
        if os.path.exists(f'./outputs/hints-candidates/{self.model}_errors.json'):
            with open(f'./outputs/hints-candidates/{self.model}_errors.json', mode='r',
                      encoding='utf8') as f:
                questions_with_problem = json.load(f)

        for rec_idx, rec in enumerate(self.generated_hints, start=1):
            while True:
                try:
                    if rec_idx <= len(candidate_answer_test_set) + len(questions_with_problem):
                        break

                    new_elements = ['Q_ID', 'Question', 'Hints', 'ExactAnswer', 'MajorType',
                                    'MinorType', 'Q_Popularity', 'Exact_Answer_Popularity', 'H_Popularity']
                    new_rec = {k: rec[k] for k in new_elements if k in rec.keys()}
                    new_rec['ExactAnswer'] = [new_rec['ExactAnswer']]
                    question = rec['Question']
                    exact_answer = rec['ExactAnswer']
                    print('[{}:{}]- {}: {}'.format(rec_idx, self.len_of_questions, question,
                                                   colored(exact_answer, 'green')))

                    question_prompt = self._question_prompt(question, exact_answer)
                    for can in question_prompt['Candidate_Question']:
                        if can == question_prompt['Exact_Answer']:
                            print(colored(f'\t{can}', 'green'))
                        else:
                            print(colored(f'\t{can}', 'yellow'))

                    if question_prompt['Exact_Answer'] is not None:
                        new_rec['ExactAnswer'].append(question_prompt['Exact_Answer'])
                        new_rec['Candidates_Answers'] = question_prompt['Candidate_Question'][:-1] + [
                            question_prompt['Candidate_Question'][-1]]
                    else:
                        new_rec['Candidates_Answers'] = question_prompt['Candidate_Question']
                        print(colored('\tNone', 'red'))

                    candidate_answer_test_set.append(new_rec)

                    if len(candidate_answer_test_set) % 10 == 0 or rec_idx == len(self.generated_hints):
                        if not os.path.exists('./outputs/hints-candidates'):
                            os.mkdir('./outputs/hints-candidates')
                        with open(f'./outputs/hints-candidates/{self.model}.json', mode='w', encoding='utf8') as f:
                            json.dump(candidate_answer_test_set, f)
                except Exception as e:
                    rec['Error'] = str(e)
                    if rec['Error'].find('HTTP code') >= 0:
                        continue
                    questions_with_problem.append(rec)
                    if len(questions_with_problem) % 1 == 0 or rec_idx == len(self.generated_hints):
                        if not os.path.exists('./outputs/hints-candidates'):
                            os.mkdir('./outputs/hints-candidates')
                        with open(
                                f'./outputs/hints-candidates/{self.model}_errors.json', mode='w', encoding='utf8') as f:
                            json.dump(questions_with_problem, f)
                break
