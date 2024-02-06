import json
import os
from tqdm import tqdm
from termcolor import colored


class Clean_File:
    def __init__(self, model):
        self.model = model

    def clean(self):
        with open(f'./outputs/hints-metric/{self.model}.json', mode='r', encoding='utf8') as f:
            dataset = json.load(f)
        for q in tqdm(dataset, desc=colored('Cleaning', attrs=['bold', 'underline'])):
            # Cleaning Q_Popularity
            q_p_copy = q['Q_Popularity'].copy()
            for ent in q_p_copy:
                if not ent.endswith('(NORM)'):
                    del q['Q_Popularity'][ent]
            q_p_copy = q['Q_Popularity'].copy()
            for ent in q_p_copy:
                val = q['Q_Popularity'][ent]
                del q['Q_Popularity'][ent]
                q['Q_Popularity'][ent[:-6].strip()] = val

            # Cleaning Exact_Answer_Popularity
            ea_p_copy = q['Exact_Answer_Popularity'].copy()
            for ex_p in ea_p_copy:
                if ex_p not in ['Normalized', 'Category']:
                    del q['Exact_Answer_Popularity'][ex_p]

            # Cleaning H_Popularity
            for h_p in q['H_Popularity']:
                h_p_copy = h_p.copy()
                for ent in h_p_copy:
                    if not ent.endswith('(NORM)'):
                        del h_p[ent]

            for h_p in q['H_Popularity']:
                h_p_copy = h_p.copy()
                for ent in h_p_copy:
                    val = h_p[ent]
                    del h_p[ent]
                    h_p[ent[:-6].strip()] = val

            # Cleaning Convergence
            con_copy = q['Convergence'].copy()
            for con_idx, con in enumerate(con_copy):
                con_len = len(q['Convergence'][con_idx])
                q['Convergence'][con_idx] = q['Convergence'][con_idx][f'Up to {con_len}']

            # Cleaning Familiarity
            fam_copy = q['Familiarity'].copy()
            for fam_idx, fam in enumerate(fam_copy):
                q['Familiarity'][fam_idx] = q['Familiarity'][fam_idx]['Avg']

        if not os.path.exists('./outputs/FINAL_OUTPUT'):
            os.mkdir('./outputs/FINAL_OUTPUT')
        with open(f'./outputs/FINAL_OUTPUT/{self.model}.json', mode='w', encoding='utf8') as f:
            json.dump(dataset, f)
