from pydantic import BaseModel


class TrainingConfig(BaseModel):
    experiment_name: str = "Test"