import mlflow

from src.training.training_config import TrainingConfig


class TrainingSession:
    def __init__(self, config: TrainingConfig):
        self.config = config

    def run(self):
        self._start_mlflow()

    def _start_mlflow(self):
        mlflow.set_experiment(self.config.experiment_name)
        with mlflow.start_run():
            #repo = Repo("/workspace")
            #commit_hash = repo.head.object.hexsha
            mlflow.source.git.commit()
            mlflow.autolog()


if __name__ == "__main__":
    config = TrainingConfig()
    training_session = TrainingSession(config)
    training_session.run()