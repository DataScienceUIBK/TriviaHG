import json
import asyncio
from openai import AsyncOpenAI
import os
import os.path as path
from termcolor import colored


class Hint_Scorer:
    def __init__(self, base_url, api_key, model):
        if path.exists(f'./outputs/hints-candidates/{model}.json'):
            with open(f'./outputs/hints-candidates/{model}.json', mode='r', encoding='utf8') as f:
                self.candidates = json.load(f)
        self.len_of_questions = len(self.candidates)
        self.api_key = api_key
        self.base_url = base_url
        self.model = model
        self.client = AsyncOpenAI(base_url=base_url, api_key=api_key)

    @staticmethod
    def _clear_hint(hint: str):
        idx = hint.find('[^')
        if idx >= 0:
            hint = hint[:idx] + '.'
        return hint

    async def _execute_prompt(self, messages):
        model = 'meta-llama/Llama-2-70b-chat-hf:Hint_Generator:NispySP'
        response = await self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0,
            top_p=1,
            max_tokens=512
        )
        return response

    async def _hint_thread(self, info):
        try:
            hint, can = info
            hint_prompt = f'Does the hint "{hint}" refer to "{can}"? Write ONLY between "Yes" or "No"'
            hint_prompt_messages = [{"role": "user", "content": hint_prompt}]
            hint_prompt_executed = await self._execute_prompt(hint_prompt_messages)
            inclusion = hint_prompt_executed.choices[0].message.content.strip().lower()
            inclusion = 1 if inclusion.lower().startswith('yes') else 0
            return can, inclusion
        except:
            return can, -1

    async def _hint_prompt(self, hint, candidate_answers):
        hint_candidate_list = list(zip([hint] * len(candidate_answers), candidate_answers))
        tasks = []
        for hint_candidate in hint_candidate_list:
            tasks.append(asyncio.create_task(self._hint_thread(hint_candidate)))
        results = dict()
        for task in asyncio.as_completed(tasks):
            task = await task
            results[task[0]] = task[1]
        hint_candidate_answers_dict = {candidate_answers[idx]: results[candidate_answers[idx]] for idx in
                                       range(len(candidate_answers))}
        return hint_candidate_answers_dict

    async def rate(self):
        scored_test_set = []
        if path.exists(f'./outputs/hints-scores/{self.model}.json'):
            with open(f'./outputs/hints-scores/{self.model}.json', mode='r',
                      encoding='utf8') as f:
                scored_test_set = json.load(f)
        for rec_idx, rec in enumerate(self.candidates, start=1):
            while True:
                try:
                    if rec_idx <= len(scored_test_set):
                        break
                    new_elements = ['Q_ID', 'Question', 'Hints', 'ExactAnswer', 'MajorType',
                                    'MinorType', 'Candidates_Answers', 'Q_Popularity', 'Exact_Answer_Popularity',
                                    'H_Popularity']
                    new_rec = {k: rec[k] for k in new_elements if k in rec.keys()}
                    question = rec['Question']
                    candidate_answers = rec['Candidates_Answers']
                    hints = rec['Hints']
                    len_of_hints = len(rec['Hints'])
                    print(colored('[{}:{} ({})]- {}: '.format(rec_idx, self.len_of_questions, self.model, question),
                                  'cyan'))
                    new_rec['Scores'] = []

                    for hint_idx, hint in enumerate(hints, start=1):
                        hint = self._clear_hint(hint)
                        print('  [{}:{}]- {}: '.format(hint_idx, len_of_hints, hint), end='', flush=True)
                        hint_prompt = await self._hint_prompt(hint, candidate_answers)
                        if -1 not in hint_prompt.values():
                            print('✅')
                        else:
                            raise Exception()
                        new_rec['Scores'].append(hint_prompt)

                    scored_test_set.append(new_rec)

                    if len(scored_test_set) % 10 == 0 or len(scored_test_set) == self.len_of_questions:
                        if not path.exists('./outputs/hints-scores'):
                            os.mkdir('./outputs/hints-scores')
                        with open(f'./outputs/hints-scores/{self.model}.json', mode='w',
                                  encoding='utf8') as f:
                            json.dump(scored_test_set, f)
                except:
                    print('❌')
                    continue
                break
