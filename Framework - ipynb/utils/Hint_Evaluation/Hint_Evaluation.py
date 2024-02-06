import os
import random
import asyncio
import json
from utils.Hint_Evaluation.Popularity import Popularity
from utils.Hint_Evaluation.Can_Ans_Generator import Can_Ans_Generator
from utils.Hint_Evaluation.Hint_Scorer import Hint_Scorer
from utils.Hint_Evaluation.Normalize_Hints import Normalize_Hints
from utils.Hint_Evaluation.Metrics import Metrics
from termcolor import colored


class Hint_Evaluation:
    def __init__(self, base_url, api_key, model):
        self.model = model
        self.base_url = base_url
        self.api_key = api_key

    def _use_duplicate_candidates(self):
        file_with_candidates = os.listdir('./outputs/hints-candidates')[0]
        with open(f'./outputs/hints-candidates/{file_with_candidates}', mode='r', encoding='utf8') as f:
            candidates_json = json.load(f)
        with open(f'./outputs/hints-popularity/{self.model}.json', mode='r', encoding='utf8') as f:
            generated_hints = json.load(f)
        for q_idx, _ in enumerate(candidates_json):
            generated_hints[q_idx]['Candidates_Answers'] = candidates_json[q_idx]['Candidates_Answers']
        with open(f'./outputs/hints-candidates/{self.model}.json', mode='w', encoding='utf8') as f:
            json.dump(generated_hints, f)

    def evaluate(self):
        random.seed(1234)

        print(colored('\nEntities Popularity:', attrs=['bold', 'underline']))
        popularity = Popularity(self.model)
        popularity.popularity()

        print(colored('\nCandidate Generating:', attrs=['bold', 'underline']))
        files_with_candidates = []
        if os.path.exists('./outputs/hints-candidates'):
            files_with_candidates = os.listdir('./outputs/hints-candidates')
        if len(files_with_candidates) == 0:
            candidate_generator = Can_Ans_Generator(self.base_url, self.api_key, self.model)
            candidate_generator.generate_candidate_answers()
        else:
            print('A duplicate file is used.')
            self._use_duplicate_candidates()

        print(colored('\nHint Scorer:', attrs=['bold', 'underline']))
        hint_evaluator = Hint_Scorer(self.base_url, self.api_key, self.model)
        asyncio.run(hint_evaluator.rate())

        print(colored('\nCompute by Metrics:', attrs=['bold', 'underline']))
        print('Normalizing')
        normalize_hints = Normalize_Hints(self.model)
        normalize_hints.normalize()

        print('Computing metrics')
        metrics = Metrics(self.model)
        metrics.compute_metrics()

        print()
