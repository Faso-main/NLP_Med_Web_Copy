import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    T5_MODEL_PATH: str = os.getenv('T5_MODEL_PATH', 'models/fake_t5-small_20ep')
    T5_LABEL_PATH: str = os.getenv('T5_LABEL_PATH', 'models/label2id.json')
    MAX_LEN: int = int(os.getenv('MAX_LEN', 128))
    DEVICE: str = os.getenv('DEVICE', 'cpu')

settings = Settings()