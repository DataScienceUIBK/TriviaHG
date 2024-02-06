import json
import os
import numpy as np


class Normalize_Hints:
    def __init__(self, model):
        self.model = model

    def _normalize_and_remove_outliers(self, pops):
        pops = [(idx, popularity) for idx, popularity in enumerate(pops)]
        pops = sorted(pops, key=lambda x: x[1])
        pops_arr = np.array([p[1] for p in pops])
        # q3, q1 = np.percentile(pops_arr, [75, 25])
        ######################################################
        q3, q1 = 24054.25, 1521
        ######################################################
        iqr = q3 - q1

        floor_outliers = pops_arr < q1 - 1.5 * iqr
        ceil_outliers = pops_arr > q3 + 1.5 * iqr
        valid_pops = np.logical_not(np.logical_or(floor_outliers, ceil_outliers))
        y_valid = np.extract(valid_pops, pops_arr)

        # min_val = np.min(y_valid)
        # max_val = np.max(y_valid)
        ######################################################
        min_val = 0
        max_val = 57837
        ######################################################

        scaled_data = (pops_arr - min_val) / (max_val - min_val)
        scaled_data = np.where(scaled_data > 1.0, 1.0, scaled_data)
        scaled_data = np.where(scaled_data < 0.0, 0.0, scaled_data)

        pops = np.array(pops, dtype=np.float64)
        pops = np.insert(pops, 2, scaled_data, axis=1)
        pops_list = pops.tolist()
        pops_list = sorted([(int(p[0]), round(p[2], 3)) for p in pops_list], key=lambda x: x[0])
        pops_list = [p[1] for p in pops_list]
        return pops_list

    def _normalize_dataset(self, dataset):
        pops = []
        for rec in dataset:
            for itm in rec['Q_Popularity'].keys():
                if itm.find('(AVG)') >= 0:
                    pops.append(rec['Q_Popularity'][itm])
            for hint in rec['H_Popularity']:
                for itm in hint.keys():
                    if itm.find('(AVG)') >= 0:
                        pops.append(hint[itm])
        pops = self._normalize_and_remove_outliers(pops)
        for rec_idx, rec in enumerate(dataset):
            q_popularity = list(rec['Q_Popularity'].keys())
            for itm in q_popularity:
                if itm.find('(AVG)') >= 0:
                    rec['Q_Popularity'][f'{itm[:-5]}(NORM)'] = pops.pop(0)
            for hint in rec['H_Popularity']:
                h_popularity = list(hint.keys())
                for itm in h_popularity:
                    if itm.find('(AVG)') >= 0:
                        hint[f'{itm[:-5]}(NORM)'] = pops.pop(0)
        return dataset

    def normalize(self):
        with open(f'./outputs/hints-scores/{self.model}.json', mode='r', encoding='utf8') as f:
            dataset = json.load(f)
        new_dataset = self._normalize_dataset(dataset)
        if not os.path.exists(f'./outputs/hints-metric'):
            os.mkdir(f'./outputs/hints-metric')
        with open(f'./outputs/hints-metric/{self.model}.json', mode='w', encoding='utf8') as f:
            json.dump(new_dataset, f)
