from pydantic import BaseModel
from time import time


class TrainingConfig(BaseModel):
    experiment_name: str = "Exploration"
    batch_size: int = 64
    max_epochs: int = 2
    patience: int = 5
    num_classes: int = 10
    hidden_size: int = 64
    seed: int = 42
    log_dir: str = f"logs/{time()}"
    data_dir: str = "data/mnist"
    learning_rate: float = 2e-4