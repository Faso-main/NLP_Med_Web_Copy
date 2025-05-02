from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
from .schemas import PredictRequest, PredictResponse
from service.classifier import MedicalClassifier
from service.extractor import TextExtractor
from service.edss import EDSSCalculator

router = APIRouter(prefix="/api")

classifier = MedicalClassifier()
extractor = TextExtractor()

@router.post('/predict', response_model=PredictResponse)
def predict(request: PredictRequest):
    if not request.text:
        raise HTTPException(status_code=400, detail="Text is empty")

    class_id, class_name = classifier.predict(request.text)
    features = extractor.extract(request.text)

    edss_calc = EDSSCalculator()
    edss_calc.assess_features(features)
    edss_score = edss_calc.calculate()

    return PredictResponse(
        class_id=class_id,
        class_name=class_name,
        features=features,
        edss_score=edss_score,
        scores=edss_calc.scores
    )
