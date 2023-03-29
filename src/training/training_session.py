import mlflow
import random
import numpy as np
import torch

from src.training.model import MNISTClassifier
from src.training.training_config import TrainingConfig
from pytorch_lightning import Trainer


class TrainingSession:
    def __init__(self, config: TrainingConfig):
        self.config = config
        self.model = None
        self.trainer = None

    def start_experiment_run(self):
        mlflow.set_experiment(self.config.experiment_name)
        with mlflow.start_run() as run:
            run_data = mlflow.get_run(run_id=run.info.run_id)
            mlflow.set_tag("git_commit_hash", run_data.data.tags["mlflow.source.git.commit"])
            mlflow.set_tag("run_id", run_data.info.run_id)

            self.run()

            run_id = run_data.info.run_uuid
            mlflow.register_model(model_uri=f"runs:/{run_id}/initial", name="Llama Model")

    def run(self):
        self.seed_generators()
        self.configure_logging()
        self.create_model()
        self.create_trainer()
        self.run_trainer()

    def seed_generators(self):
        if self.config.seed is not None:
            random.seed(self.config.seed)
            np.random.seed(self.config.seed)
            torch.manual_seed(self.config.seed)
            torch.cuda.manual_seed(self.config.seed)
            torch.backends.cudnn.deterministic = True

    def configure_logging(self):
        mlflow.autolog()

    def create_model(self):
        self.model = MNISTClassifier(hparams=self.config)

    def create_trainer(self):
        self.trainer = Trainer(
            logger=None,
            max_epochs=self.config.max_epochs,
        )

    def run_trainer(self):
        self.trainer.fit(self.model)


if __name__ == "__main__":
    config = TrainingConfig()
    training_session = TrainingSession(config)
    training_session.start_experiment_run()