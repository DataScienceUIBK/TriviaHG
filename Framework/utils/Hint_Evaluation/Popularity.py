import json
import spacy
import requests
import os
import shutil
import os.path as path
import numpy as np
from faker import Faker
from mwviews.api import PageviewsClient


class Popularity:
    def __init__(self, model):
        self.model = model
        self.dataset = []
        if not path.exists('./outputs/hints-popularity'):
            os.mkdir('./outputs/hints-popularity')
        if not path.exists(f'./outputs/hints-popularity/{self.model}.json'):
            shutil.copy(f'./outputs/hints_filtered/{self.model}.json',
                        f'./outputs/hints-popularity/{self.model}.json')
        with open(f'./outputs/hints-popularity/{self.model}.json', mode='r', encoding='utf8') as f:
            self.dataset = json.load(f)
        self.nlp = spacy.load('en_core_web_trf')
        self.faker = Faker()

    @staticmethod
    def _clear_hint(hint: str):
        idx = hint.find('[^')
        if idx >= 0:
            hint = hint[:idx] + '.'
        return hint

    def _sent_entities(self, sentence: str):
        valid_entities = ['PERSON', 'NORP', 'FAC', 'ORG', 'GPE', 'LOC', 'PRODUCT', 'EVENT', 'WORK_OF_ART', 'LAW',
                          'LANGUAGE']
        doc = self.nlp(sentence)
        entities = []
        for ent in doc.ents:
            if ent.label_ in valid_entities:
                entities.append(ent.text)
        return entities

    def _init_requests(self, q_id):
        self._session = requests.Session()
        self._user_agent = f'<{self.faker.company_email()}> {q_id} analyzer'

    def _find_similar_titles(self, title):
        params = {
            "action": "query",
            "format": "json",
            "list": "search",
            "srsearch": title
        }

        request = self._session.get(url='https://en.wikipedia.org/w/api.php', params=params)
        request_json = request.json()

        if request_json['query']['search']:
            return [page['title'] for page in request_json['query']['search']]
        else:
            return None

    def _extract_views(self, entities):
        if len(entities) == 0:
            return {}
        most_similar_entities = set()
        for entity in entities:
            top_result = self._find_similar_titles(entity)
            if top_result is None:
                continue
            most_similar_entities.add(top_result[0])
        if len(most_similar_entities) == 0:
            return {}
        p = PageviewsClient(user_agent=self._user_agent, parallelism=len(entities))
        views = p.article_views('en.wikipedia.org', list(most_similar_entities), granularity='monthly',
                                start='20150101',
                                end='20231231')
        views_dict_list = {}
        for entity_dict in views.values():
            for key in entity_dict.keys():
                if key not in views_dict_list:
                    views_dict_list[key] = []
                views_dict_list[key].append(entity_dict[key] if entity_dict[key] is not None else -1)

        views_dict = {}
        for key in views_dict_list.keys():
            valid_months = [num for num in views_dict_list[key] if num >= 0]
            if len(valid_months) == 0:
                views_dict[f'{key} (AVG)'] = 0
                views_dict[key] = 0
            else:
                views_dict[f'{key} (AVG)'] = int(sum(valid_months) / len(valid_months))
                views_dict[key] = sum(valid_months)
        return views_dict

    def _normalize_and_remove_outliers(self, pops):
        pops = [(idx, popularity) for idx, popularity in enumerate(pops)]
        pops = sorted(pops, key=lambda x: x[1])
        pops_arr = np.array([p[1] for p in pops])
        # q3, q1 = np.percentile(pops_arr, [75, 25])
        q3, q1 = 24054.25, 1521
        iqr = q3 - q1

        floor_outliers = pops_arr < q1 - 1.5 * iqr
        ceil_outliers = pops_arr > q3 + 1.5 * iqr
        valid_pops = np.logical_not(np.logical_or(floor_outliers, ceil_outliers))
        y_valid = np.extract(valid_pops, pops_arr)

        # min_val = np.min(y_valid)
        # max_val = np.max(y_valid)
        min_val = 0
        max_val = 57837
        scaled_data = (pops_arr - min_val) / (max_val - min_val)
        scaled_data = np.where(scaled_data > 1.0, 1.0, scaled_data)
        scaled_data = np.where(scaled_data < 0.0, 0.0, scaled_data)

        pops = np.array(pops, dtype=np.float64)
        pops = np.insert(pops, 2, scaled_data, axis=1)
        pops_list = pops.tolist()
        pops_list = sorted([(int(p[0]), round(p[2], 3)) for p in pops_list], key=lambda x: x[0])
        pops_list = [p[1] for p in pops_list]
        return pops_list

    def normalize(self):
        pops = []
        for rec in self.dataset:
            pops.append(rec['Exact_Answer_Popularity'][list(rec['Exact_Answer_Popularity'].keys())[0]])
        pops = self._normalize_and_remove_outliers(pops)
        for rec_idx, rec in enumerate(self.dataset):
            rec['Exact_Answer_Popularity']['Normalized'] = pops[rec_idx]
            if pops[rec_idx] < 0.33:
                category = 'Hard'
            elif pops[rec_idx] < 0.66:
                category = 'Medium'
            else:
                category = 'Easy'
            rec['Exact_Answer_Popularity']['Category'] = category
        with open(f'./outputs/hints-popularity/{self.model}.json', mode='w',
                  encoding='utf8') as f:
            json.dump(self.dataset, f)

    def popularity(self):
        for rec_idx, rec in enumerate(self.dataset, start=1):
            while True:
                try:
                    if 'Exact_Answer_Popularity' in rec:
                        break
                    q_id = rec['Q_ID']
                    question = rec['Question']
                    hints = rec['Hints']
                    wiki_entity = rec['ExactAnswer']
                    self._init_requests(q_id)
                    q_entities = self._sent_entities(question)
                    print(f'{rec_idx}: {question} ', end='', flush=True)
                    q_popularity = self._extract_views(q_entities)
                    exact_answer_popularity = self._extract_views([wiki_entity])
                    rec['Q_Popularity'] = q_popularity
                    rec['Exact_Answer_Popularity'] = exact_answer_popularity
                    rec['H_Popularity'] = []
                    for hint in hints:
                        hint = self._clear_hint(hint)
                        h_entities = self._sent_entities(hint)
                        hint_popularity = self._extract_views(h_entities)
                        hint_popularity = {k: v for k, v in hint_popularity.items() if k not in q_popularity.keys()}
                        rec['H_Popularity'].append(hint_popularity)
                    print('✅')
                    if rec_idx % 10 == 0 or rec_idx == len(self.dataset):
                        with open(f'./outputs/hints-popularity/{self.model}.json', mode='w', encoding='utf8') as f:
                            json.dump(self.dataset, f)
                except KeyboardInterrupt:
                    exit(0)
                except Exception as e:
                    print('❌')
                    if str(e).find('The pageview API returned nothing useful at') >= 0:
                        break
                    print(e)
                    if 'Exact_Answer_Popularity' in rec:
                        del rec['Exact_Answer_Popularity']
                    continue
                break
        self.normalize()
