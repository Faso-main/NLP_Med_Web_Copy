from typing import Dict, Any

class EDSSCalculator:
    def __init__(self):
        self.scores: Dict[str, int] = {k: 0 for k in [
            'mobility','sensory','visual','bladder_bowel','cognitive',
            'motor','cerebellar','speech','mental_state','fatigue'
        ]}
        self.key_map = {
            'visual_acuity': 'visual',
            'sensory_feedback': 'sensory',
            'bladder_bowel_function': 'bladder_bowel',
            'cognitive_feedback': 'cognitive',
            'motor_strength': 'motor',
            'speech_condition': 'speech',
            'mental_state': 'mental_state',
            'fatigue': 'fatigue',
            'cerebellar_symptoms': 'cerebellar'
        }

    def assess_features(self, features: Dict[str, Any]):
        for feat, lvl in features.items():
            cat = self.key_map.get(feat)
            if lvl is not None and cat:
                self.assess(cat, lvl)

    def assess(self, category: str, level: Any):
        scoring = {
            'sensory': {'normal':1,'mild':2,'moderate':3,'severe':4},
            'visual': self._visual(level),
            'bladder_bowel': {'normal':1,'mild_incontinence':2,'severe_incontinence':3},
            'cognitive': {'normal':1,'mild':2,'moderate':3,'severe':4},
            'motor': {'normal':1,'mild':2,'moderate':3,'severe':4},
            'cerebellar': {'normal':1,'mild':2,'severe':3},
            'speech': {'normal':1,'mild':2,'moderate':3,'severe':4},
            'mental_state': {'normal':1,'mild':2,'moderate':3,'severe':4},
            'fatigue': {'none':1,'mild':2,'moderate':3,'severe':4},
        }
        self.scores[category] = scoring[category] if isinstance(scoring[category], int) else scoring[category].get(level, 4)

    def _visual(self, acuity: Any) -> int:
        if isinstance(acuity, tuple) and len(acuity) == 2:
            l,r = acuity
            if l>=1.0 and r>=1.0: return 1
            if l>=0.7 or r>=0.7: return 2
            return 3
        return 4

    def calculate(self) -> float:
        if self.scores['motor']>=3 and self.scores['sensory']>=3:
            return 6.0
        if self.scores['visual']>=2:
            return 4.0
        return sum(self.scores.values())/len(self.scores)