import json
import os


class Metrics:
    def __init__(self, model):
        self.model = model

    def _compute_convergence(self, hint_score, up_to):
        if up_to == 1:
            scores = [hint_score[-1]]
        else:
            scores = hint_score[:up_to - 1] + [hint_score[-1]]
        if scores[-1] == 0:
            return 0
        return round(1 - ((sum(scores) - 1) / len(scores)), 2)

    def _convergence(self, dataset):
        for rec_idx, rec in enumerate(dataset):
            rec['Convergence'] = []
            scores = rec['Scores']
            for hint_score in scores:
                hint_score = list(hint_score.values())
                hint_convergence = dict()
                for up_to in range(1, len(hint_score) + 1):
                    conv = self._compute_convergence(hint_score, up_to)
                    hint_convergence[f'Up to {up_to}'] = conv
                rec['Convergence'].append(hint_convergence)
        return dataset

    def _compute_familarity(self, normilized_pops):
        if len(normilized_pops) == 0:
            return {'Min': 1, 'Avg': 1, 'Max': 1}
        min_pop = min(normilized_pops)
        max_pop = max(normilized_pops)
        avg_pop = round(sum(normilized_pops) / len(normilized_pops), 3)
        return {'Min': min_pop, 'Avg': avg_pop, 'Max': max_pop}

    def _familarity(self, dataset):
        for rec_idx, rec in enumerate(dataset):
            rec['Familiarity'] = []
            popularity = rec['H_Popularity']
            for hint_popularity in popularity:
                normilized_pops = []
                for key in hint_popularity.keys():
                    if key.find('(NORM)') >= 0:
                        normilized_pops.append(hint_popularity[key])
                family = self._compute_familarity(normilized_pops)
                rec['Familiarity'].append(family)
        return dataset

    def compute_metrics(self):
        with open(f'./outputs/hints-metric/{self.model}.json', mode='r', encoding='utf8') as f:
            dataset = json.load(f)
        new_dataset = self._convergence(dataset)
        new_dataset = self._familarity(new_dataset)
        with open(f'./outputs/hints-metric/{self.model}.json', mode='w', encoding='utf8') as f:
            json.dump(new_dataset, f)
