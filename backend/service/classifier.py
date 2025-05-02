import json
import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration
from typing import Tuple, Optional, Dict
from config.settings import settings

class MedicalClassifier:
    def __init__(self):
        self.device = torch.device(settings.DEVICE)
        self.tokenizer = T5Tokenizer.from_pretrained(settings.T5_MODEL_PATH)
        self.model = T5ForConditionalGeneration.from_pretrained(settings.T5_MODEL_PATH).to(self.device)
        with open(settings.T5_LABEL_PATH, 'r', encoding='utf-8') as f:
            label2id = json.load(f)
        self.id2label = {v: k for k, v in label2id.items()}

    def predict(self, text: str) -> Tuple[Optional[int], str]:
        enc = self.tokenizer(text,
                              max_length=settings.MAX_LEN,
                              padding='max_length',
                              truncation=True,
                              return_tensors='pt')
        input_ids = enc['input_ids'].to(self.device)
        attention_mask = enc['attention_mask'].to(self.device)
        with torch.no_grad():
            gen_ids = self.model.generate(input_ids=input_ids,
                                          attention_mask=attention_mask,
                                          max_length=10)
        pred_str = self.tokenizer.decode(gen_ids[0], skip_special_tokens=True).strip()
        try:
            pid = int(pred_str)
        except ValueError:
            pid = None
        return pid, self.id2label.get(pid, 'unknown')