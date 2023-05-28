# Testing alexnet

import torch
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
from torchvision import datasets
import torchvision.transforms as transforms
import pathlib

import torch.multiprocessing as mp
from torch.utils.data.distributed import DistributedSampler
from torch.nn.parallel import DistributedDataParallel as DDP
from torch.distributed import init_process_group, destroy_process_group
import os
from AlexNet import AlexNet


def ddp_setup():
    init_process_group(backend="nccl")
    torch.autograd.set_detect_anomaly(True)

class Trainer:
    def __init__(
        self,
        model: torch.nn.Module,
        train_data: DataLoader,
        optimizer: torch.optim.Optimizer,
        save_every: int,
        snapshot_path: str,
        lr_scheduler: torch.optim.Optimizer
    ) -> None:
        self.gpu_id = int(os.environ["LOCAL_RANK"])
        torch.cuda.set_device(self.gpu_id) # THE IMPORTANT LINE!
        self.model = model.to(self.gpu_id)
        self.train_data = train_data
        self.optimizer = optimizer
        self.save_every = save_every
        self.epochs_run = 0
        self.snapshot_path = snapshot_path
        self.lr_scheduler = lr_scheduler
        if os.path.exists(snapshot_path):
            print("Loading snapshot")
            self._load_snapshot(snapshot_path)

        self.model = DDP(self.model, device_ids=[self.gpu_id])

    def _load_snapshot(self, snapshot_path):
        loc = f"cuda:{self.gpu_id}"
        snapshot = torch.load(snapshot_path, map_location=loc)
        self.model.load_state_dict(snapshot["MODEL_STATE"])
        self.epochs_run = snapshot["EPOCHS_RUN"]
        print(f"Resuming training from snapshot at Epoch {self.epochs_run}")

    def _run_batch(self, source, targets):
        self.optimizer.zero_grad()
        output = self.model(source).to(self.gpu_id)
        targets = targets.to(self.gpu_id)
        loss = F.cross_entropy(output, targets)
        loss.backward()
        self.optimizer.step()

    def _run_epoch(self, epoch):
        self.lr_scheduler.step()
        b_sz = len(next(iter(self.train_data))[0])
        print(f"[GPU{self.gpu_id}] Epoch {epoch} | Batchsize: {b_sz} | Steps: {len(self.train_data)}")
        self.train_data.sampler.set_epoch(epoch)
        for source, targets in self.train_data:
            source = source.to(self.gpu_id)
            targets = targets.to(self.gpu_id)
            self._run_batch(source, targets)

    def _save_snapshot(self, epoch):
        snapshot = {
            "MODEL_STATE": self.model.module.state_dict(),
            "EPOCHS_RUN": epoch,
        }
        torch.save(snapshot, self.snapshot_path)
        print(f"Epoch {epoch} | Training snapshot saved at {self.snapshot_path}")

    def train(self, max_epochs: int):
        for epoch in range(self.epochs_run, max_epochs):
            self._run_epoch(epoch)
            if self.gpu_id == 0 and epoch % self.save_every == 0:
                self._save_snapshot(epoch)
        
        if self.gpu_id == 0:
            torch.save(self.model.module.state_dict(), "model_Data3.pt")
            print("Final model saved.")


def load_train_objs():
    #device=torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    train_path = '../Data3/train'
    transformer=transforms.Compose([
        transforms.Resize((227, 227)),
        #transforms.RandomCrop(224),
        #transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    train_set = datasets.ImageFolder(root=train_path, transform=transformer)
    root=pathlib.Path(train_path)
    classes=sorted([j.name.split('/')[-1] for j in root.iterdir()])
    alexnet = AlexNet(num_classes=len(classes)) #.to(device)
    optimizer = torch.optim.Adam(params=alexnet.parameters(), lr=0.0001)
    lr_scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=30, gamma=0.1)
    return train_set, alexnet, optimizer, lr_scheduler


def prepare_dataloader(dataset: Dataset, batch_size: int):
    return DataLoader(
        dataset,
        batch_size=batch_size,
        pin_memory=True,
        shuffle=False,
        sampler=DistributedSampler(dataset),
        #drop_last=True,
    )


def main(save_every: int, total_epochs: int, batch_size: int, snapshot_path: str = "snapshot_AlexNet_Data3.pt"):
    print("Starting main")
    ddp_setup()
    print("ddp started")
    dataset, model, optimizer, lr_scheduler = load_train_objs()
    print("Load Training objects")
    train_data = prepare_dataloader(dataset, batch_size)
    trainer = Trainer(model, train_data, optimizer, save_every, snapshot_path, lr_scheduler)
    trainer.train(total_epochs)
    destroy_process_group()


if __name__ == "__main__":
    #print("current_device" + str(torch.cuda.current_device()))
    #print("Local_rank" + os.environ["LOCAL_RANK"])
    #print("CUDA_VISIBLE_DEVICES" + os.environ["CUDA_VISIBLE_DEVICES"])
    import argparse
    parser = argparse.ArgumentParser(description='simple distributed training job')
    parser.add_argument('total_epochs', type=int, help='Total epochs to train the model')
    parser.add_argument('save_every', type=int, help='How often to save a snapshot')
    parser.add_argument('--batch_size', default=128, type=int, help='Input batch size on each device (default: 32)')
    args = parser.parse_args()

    # EPOCHS = 90
    # BATCH_SIZE = 128
    # SAVE_EVERY = 10

    main(args.save_every, args.total_epochs, args.batch_size)
