from pydantic import BaseModel
from typing import Optional, Dict, Any


class PredictRequest(BaseModel):
    text: str

class PredictResponse(BaseModel):
    class_id: Optional[int]
    class_name: str
    features: Dict[str, Any]
    edss_score: float
    scores: Dict[str, int]
