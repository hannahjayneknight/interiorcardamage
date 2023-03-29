#Load libraries
import os
import numpy as np
import torch
import glob
import torch.nn as nn
from torchvision.transforms import transforms
from torch.utils.data import DataLoader
from torch.optim import Adam
from torch.autograd import Variable
import torchvision
import pathlib

device=torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(device)

'''

transformer=transforms.Compose([
    transforms.Resize((150,150)),
    transforms.RandomHorizontalFlip(), # flips image with p=0.5 to augment data
    transforms.ToTensor(),  #0-255 to 0-1, numpy to tensors
    transforms.Normalize([0.5,0.5,0.5], # 0-1 to [-1,1] , formula (x-mean)/std
                        [0.5,0.5,0.5])
])

train_path = '../Data/train'
test_path = '../Data/test'

train_loader=torch.utils.data.DataLoader(
    torchvision.datasets.ImageFolder(root=train_path, transform=transformer),
    batch_size=64, shuffle=True
)
test_loader=torch.utils.data.DataLoader(
    torchvision.datasets.ImageFolder(root=test_path, transform=transformer),
    batch_size=32, shuffle=True
)

root=pathlib.Path(train_path)
classes=sorted([j.name.split('/')[-1] for j in root.iterdir()])
print(len(classes))

'''