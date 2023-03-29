import torch
from torch import nn
from pytorch_lightning import LightningModule
from pytorch_lightning.callbacks import ModelCheckpoint
from torch.nn import functional as F
from torch.utils.data import DataLoader, random_split
from torchvision import transforms
from torchvision.datasets import MNIST

from src.training.training_config import TrainingConfig


class MNISTClassifier(LightningModule):
    def __init__(self, hparams: TrainingConfig):
        super().__init__()
        for key in hparams.__dict__.keys():
            self.hparams[key] = hparams.__dict__[key]
        self.dims = (1, 28, 28)
        channels, width, height = self.dims
        self.transform = transforms.Compose(
            [transforms.ToTensor(), transforms.Normalize((0.1307,), (0.3081,))]
        )
        self.model = nn.Sequential(
            nn.Flatten(),
            nn.Linear(channels * width * height, hparams.hidden_size),
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(hparams.hidden_size, hparams.hidden_size),
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(hparams.hidden_size, hparams.num_classes),
        )

    def forward(self, x):
        x = self.model(x)
        return F.log_softmax(x, dim=1)

    def training_step(self, batch, batch_idx):
        x, y = batch
        logits = self(x)
        loss = F.nll_loss(logits, y)
        return loss

    def validation_step(self, batch, batch_idx):
        x, y = batch
        logits = self(x)
        loss = F.nll_loss(logits, y)
        return loss

    def test_step(self, batch, batch_idx):
        return self.validation_step(batch, batch_idx)

    def configure_optimizers(self):
        optimizer = torch.optim.Adam(self.parameters(), lr=self.hparams.learning_rate)
        return optimizer

    def prepare_data(self):
        MNIST(str(self.hparams.data_dir), train=True, download=True)
        MNIST(str(self.hparams.data_dir), train=False, download=True)

    def setup(self, stage=None):
        if stage == "fit" or stage is None:
            mnist_full = MNIST(
                self.hparams.data_dir, train=True, transform=self.transform
            )
            self.mnist_train, self.mnist_val = random_split(mnist_full, [55000, 5000])

        if stage == "test" or stage is None:
            self.mnist_test = MNIST(
                self.hparams.data_dir, train=False, transform=self.transform
            )

    def train_dataloader(self):
        return DataLoader(self.mnist_train, batch_size=self.hparams.batch_size)

    def val_dataloader(self):
        return DataLoader(self.mnist_val, batch_size=self.hparams.batch_size)

    def test_dataloader(self):
        return DataLoader(self.mnist_test, batch_size=self.hparams.batch_size)

    def create_callbacks(self):
        return [
            ModelCheckpoint(
                dirpath=self.hparams.log_dir,
                monitor="val_loss",
                save_last=True,
                verbose=True,
                mode="max",
                save_top_k=2,
            )
        ]