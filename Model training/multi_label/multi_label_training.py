# Attempting to actually train a model

import torch
import torch.nn as nn
from torchvision.transforms import transforms
from torch.utils.data import DataLoader
from torch.optim import Adam
import torchvision
import pathlib
from cnn_multi_label import ConvNet_Multi_Label

device=torch.device('cuda' if torch.cuda.is_available() else 'cpu')
train_transformer=transforms.Compose([
    transforms.Resize((150,150)),
    transforms.RandomHorizontalFlip(), # flips image with p=0.5 to augment data
    transforms.ToTensor(),  #0-255 to 0-1, numpy to tensors
    transforms.Normalize([0.5,0.5,0.5], # 0-1 to [-1,1] , formula (x-mean)/std
                        [0.5,0.5,0.5])
])
train_path = '../classifying_dirt/train'
train_loader=DataLoader(
    torchvision.datasets.ImageFolder(root=train_path, transform=train_transformer),
    batch_size=32, shuffle=True, num_workers=4,
    pin_memory=True,
)
root=pathlib.Path(train_path)
classes=sorted([j.name.split('/')[-1] for j in root.iterdir()])
     
model=ConvNet_Multi_Label(num_classes=len(classes))
model.to(device)
optimizer=Adam(model.parameters(),lr=0.001,weight_decay=0.0001)
loss_function=nn.BCEWithLogitsLoss()
num_epochs=90
for epoch in range(num_epochs):
    #model.train()
    #print("Starting epoch " + str(epoch))
    for i, data in enumerate(train_loader, 0):
        inputs, labels = data[0].to(device), data[1].to(device)
        # One-hot encode the target labels
        labels_one_hot = torch.zeros(labels.size(0), len(classes)).to(device)
        labels_one_hot.scatter_(1, labels.unsqueeze(1), 1)  # Perform one-hot encoding
    
        optimizer.zero_grad()
        outputs=model(inputs)
        loss=loss_function(outputs,labels_one_hot)
        loss.backward()
        optimizer.step()
    print('Epoch '+str(epoch) + ' finished.')
    torch.save(model.state_dict(),'multi_label_cnn.model')
    print("Model saved")

