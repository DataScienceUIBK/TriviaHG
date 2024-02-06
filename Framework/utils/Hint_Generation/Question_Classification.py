import torch
import random
import numpy as np
import torch.nn as nn
import pickle
from transformers import logging as tr_logging
from transformers import AutoModel, AutoTokenizer, AutoConfig
import logging
from torch.utils.data import TensorDataset, DataLoader

logging.disable(logging.WARNING)
tr_logging.set_verbosity_error()


class Classifier(nn.Module):
    def __init__(self, model_name, num_labels=2, dropout_rate=0.1):
        super(Classifier, self).__init__()
        self.encoder = AutoModel.from_pretrained(model_name)
        config = AutoConfig.from_pretrained(model_name)
        self.cls_size = int(config.hidden_size)
        self.input_dropout = nn.Dropout(p=dropout_rate)
        self.fully_connected_layer = nn.Linear(self.cls_size, num_labels)

    def forward(self, input_ids, attention_mask):
        model_outputs = self.encoder(input_ids, attention_mask)
        encoded_cls = model_outputs.last_hidden_state[:, 0]
        encoded_cls_dp = self.input_dropout(encoded_cls)
        logits = self.fully_connected_layer(encoded_cls_dp)
        return logits, encoded_cls


class QC:

    def __init__(self, batch_size: int = 256):
        seed_val = 213
        random.seed(seed_val)
        np.random.seed(seed_val)
        torch.manual_seed(seed_val)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(seed_val)
        self.device = torch.device('cuda')
        self.max_seq_length = 64
        self.batch_size = batch_size
        self.out_dropout_rate = 0.1
        self.output_model_name = './utils/Hint_Generation/Question_Classification/best_qc_model.pickle'
        self.model_name = 'roberta-large'
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        with open('./utils/Hint_Generation/Question_Classification/label_to_id.pickle', mode='rb') as f:
            self.label_to_id_map = pickle.load(f)
        with open('./utils/Hint_Generation/Question_Classification/id_to_label.pickle', mode='rb') as f:
            self.id_to_label_map = pickle.load(f)
        with open('./utils/Hint_Generation/Question_Classification/labels_dict.pickle', mode='rb') as f:
            self.labels = pickle.load(f)

    def _generate_data_loader(self, questions: list, label_map, tokenizer):
        input_ids = []
        input_mask_array = []
        label_id_array = []

        for (text, label) in questions:
            encoded_sent = tokenizer.encode_plus(text, add_special_tokens=True, max_length=self.max_seq_length,
                                                 padding='max_length', truncation=True)
            input_ids.append(encoded_sent['input_ids'])
            input_mask_array.append(encoded_sent['attention_mask'])

            id = -1
            if label in label_map:
                id = label_map[label]
            label_id_array.append(id)

        input_ids = torch.tensor(input_ids)
        input_mask_array = torch.tensor(input_mask_array)
        label_id_array = torch.tensor(label_id_array, dtype=torch.long)

        dataset = TensorDataset(input_ids, input_mask_array, label_id_array)
        return DataLoader(dataset, batch_size=self.batch_size)

    def get_question_label(self, questions: list):
        import __main__
        setattr(__main__, "Classifier", Classifier)
        best_model: Classifier = torch.load(self.output_model_name)

        my_list = [(question, '_') for question in questions]
        my_data_loader = self._generate_data_loader(my_list, self.label_to_id_map, self.tokenizer)
        for batch in my_data_loader:
            b_input_ids = batch[0].to(self.device)
            b_input_mask = batch[1].to(self.device)

            with torch.no_grad():
                logits, _ = best_model(b_input_ids, b_input_mask)

            _, preds = torch.max(logits, 1)
            labels = []
            for ex_id in range(len(b_input_mask)):
                predicted_label = self.id_to_label_map[preds[ex_id].item()]
                coarse_lbl, fine_lbl = tuple(predicted_label.split(':'))
                labels.append({'major_type': '{}:{}'.format(coarse_lbl, self.labels['short_to_desc'][coarse_lbl]),
                               'minor_type': '{}:{}'.format(fine_lbl, self.labels['labels'][coarse_lbl][fine_lbl])})
        return labels
