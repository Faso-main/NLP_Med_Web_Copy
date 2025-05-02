import re
import spacy
from typing import Dict, Any

# Загружаем модель spaCy для русского языка
nlp = spacy.load('ru_core_news_md')

class TextExtractor:
    """
    Класс для извлечения медицинских признаков из текста.
    """
    def __init__(self):
        self.extractors = [
            self._extract_visual,
            self._extract_motor,
            self._extract_sensory,
            self._extract_bladder,
            self._extract_cognitive,
            self._extract_fatigue,
            self._extract_speech,
            self._extract_mental,
            self._extract_onset,
            self._extract_cerebellar
        ]

    def extract(self, text: str) -> Dict[str, Any]:
        """
        Извлекает все доступные признаки из текста.
        :param text: Клинический текст пациента
        :return: Словарь {признак: уровень или значение}
        """
        doc = nlp(text)
        results: Dict[str, Any] = {}
        for fn in self.extractors:
            results.update(fn(doc))
        return results

    def _extract_visual(self, doc) -> Dict[str, Any]:
        """
        Поиск описания остроты зрения в формате "OD=0.8; OS=1.2".
        """
        for sent in doc.sents:
            if 'острота зрения' in sent.text:
                match = re.search(r'OD=(\S+);\s*OS=(\S+)', sent.text)
                if match:
                    try:
                        left = float(match.group(1).replace(',', '.'))
                        right = float(match.group(2).replace(',', '.'))
                        return {'visual_acuity': (left, right)}
                    except ValueError:
                        return {'visual_acuity': (0.0, 0.0)}
        return {'visual_acuity': (0.0, 0.0)}

    def _extract_motor(self, doc) -> Dict[str, Any]:
        """
        Поиск упоминаний слабости или неустойчивости.
        """
        cond = any('слабость' in sent.text or 'неустойчивость' in sent.text for sent in doc.sents)
        return {'motor_strength': 'severe' if cond else None}

    def _extract_sensory(self, doc) -> Dict[str, Any]:
        """
        Поиск упоминаний онемения или покалывания.
        """
        cond = any('онемение' in sent.text or 'покалывание' in sent.text for sent in doc.sents)
        return {'sensory_feedback': 'mild' if cond else None}

    def _extract_bladder(self, doc) -> Dict[str, Any]:
        """
        Поиск упоминаний недержания или частых позывов.
        """
        cond = any('недержание' in sent.text or 'частые позывы' in sent.text for sent in doc.sents)
        return {'bladder_bowel_function': 'mild_incontinence' if cond else None}

    def _extract_cognitive(self, doc) -> Dict[str, Any]:
        """
        Поиск упоминаний головокружения или снижения памяти.
        """
        cond = any('головокружение' in sent.text or 'снижение памяти' in sent.text for sent in doc.sents)
        return {'cognitive_feedback': 'mild' if cond else None}

    def _extract_fatigue(self, doc) -> Dict[str, Any]:
        """
        Поиск упоминаний утомляемости.
        """
        cond = any('утомляемость' in sent.text for sent in doc.sents)
        return {'fatigue': 'moderate' if cond else None}

    def _extract_speech(self, doc) -> Dict[str, Any]:
        """
        Поиск упоминаний дизартрии или затруднения речи.
        """
        cond = any('дизартрия' in sent.text or 'затруднение речи' in sent.text for sent in doc.sents)
        return {'speech_condition': 'moderate' if cond else None}

    def _extract_mental(self, doc) -> Dict[str, Any]:
        """
        Поиск упоминаний депрессии или тревожности.
        """
        cond = any('депрессия' in sent.text or 'тревожность' in sent.text for sent in doc.sents)
        return {'mental_state': 'moderate' if cond else None}

    def _extract_onset(self, doc) -> Dict[str, Any]:
        """
        Поиск упоминаний начала симптомов: "заболела", "появилось".
        """
        cond = any('заболела' in sent.text or 'появилось' in sent.text for sent in doc.sents)
        return {'symptoms_onset': cond}

    def _extract_cerebellar(self, doc) -> Dict[str, Any]:
        """
        Поиск упоминаний нистагма или атаксии.
        """
        cond = any('нистагм' in sent.text or 'атаксия' in sent.text for sent in doc.sents)
        return {'cerebellar_symptoms': 'severe' if cond else None}