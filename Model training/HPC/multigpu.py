import torch
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
from datautils import MyTrainDataset

import torch.multiprocessing as mp
from torch.utils.data.distributed import DistributedSampler
from torch.nn.parallel import DistributedDataParallel as DDP
from torch.distributed import init_process_group, destroy_process_group
import os


def ddp_setup(rank, world_size):
    """
    Args:
        rank: Unique identifier of each process -->pbs array index?
        world_size: Total number of processes --> number of gpus I have?
    """
    os.environ["MASTER_ADDR"] = "localhost" # ip address of machine running rank 0 process
    os.environ["MASTER_PORT"] = "12355" # master coordinates communication across all processes
    init_process_group(backend="nccl", rank=rank, world_size=world_size) #nccl = nvidia communications library