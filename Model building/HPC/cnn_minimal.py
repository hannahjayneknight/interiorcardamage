import torch
import torch.nn as nn
from torchvision.transforms import transforms
from torch.utils.data import DataLoader
from torch.optim import Adam
import torchvision
import pathlib

device=torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(device)
train_transformer=transforms.Compose([
    transforms.Resize((150,150)),
    transforms.RandomHorizontalFlip(), # flips image with p=0.5 to augment data
    transforms.ToTensor(),  #0-255 to 0-1, numpy to tensors
    transforms.Normalize([0.5,0.5,0.5], # 0-1 to [-1,1] , formula (x-mean)/std
                        [0.5,0.5,0.5])
])
test_transformer=transforms.Compose([
    transforms.Resize((150,150)),
    transforms.ToTensor(),
    transforms.Normalize([0.5,0.5,0.5],
                        [0.5,0.5,0.5])
])
train_path = '../Data/train'
test_path = '../Data/test'
train_loader=torch.utils.data.DataLoader(
    torchvision.datasets.ImageFolder(root=train_path, transform=train_transformer),
    batch_size=64, shuffle=True
)
test_loader=torch.utils.data.DataLoader(
    torchvision.datasets.ImageFolder(root=test_path, transform=test_transformer),
    batch_size=32, shuffle=True
)
print('data loaded')
root=pathlib.Path(train_path)
classes=sorted([j.name.split('/')[-1] for j in root.iterdir()])
print('No. classes: '+str(len(classes)))

class ConvNet(nn.Module):
    def __init__(self,num_classes=len(classes)):
        super(ConvNet,self).__init__()
        self.conv1=nn.Conv2d(in_channels=3,out_channels=12,kernel_size=3,stride=1,padding=1)
        self.bn1=nn.BatchNorm2d(num_features=12)
        self.relu1=nn.ReLU()
        self.pool=nn.MaxPool2d(kernel_size=2)
        self.conv2=nn.Conv2d(in_channels=12,out_channels=20,kernel_size=3,stride=1,padding=1)
        self.relu2=nn.ReLU()
        self.conv3=nn.Conv2d(in_channels=20,out_channels=32,kernel_size=3,stride=1,padding=1)
        self.bn3=nn.BatchNorm2d(num_features=32)
        self.relu3=nn.ReLU()
        self.fc=nn.Linear(in_features=75 * 75 * 32,out_features=num_classes)
    def forward(self,input):
        output=self.conv1(input)
        output=self.bn1(output)
        output=self.relu1(output)
        output=self.pool(output)   
        output=self.conv2(output)
        output=self.relu2(output)
        output=self.conv3(output)
        output=self.bn3(output)
        output=self.relu3(output)            
        output=output.view(-1,32*75*75)
        output=self.fc(output) 
        return output        
    

model=ConvNet(num_classes=len(classes))
model.to(device)
print("model loaded")
optimizer=Adam(model.parameters(),lr=0.001,weight_decay=0.0001)
print("optimizer defined")
loss_function=nn.CrossEntropyLoss()
print("loss defined")
num_epochs=5
for epoch in range(num_epochs):
    print("Starting epoch " + str(epoch))
    for i, (images,labels) in enumerate(train_loader):  
        images, labels = images.to(device), labels.to(device)
        optimizer.zero_grad()
        outputs=model(images)
        loss=loss_function(outputs,labels)
        loss.backward()
        optimizer.step()    
    print('Epoch '+str(epoch) + ' finished.')
    torch.save(model.state_dict(),'best_checkpoint.model')
    print("Model saved")
