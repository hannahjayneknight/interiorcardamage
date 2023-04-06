import torch
import torch.nn as nn
from torchvision.transforms import transforms
import torchvision
import pathlib
#from AlexNet import AlexNet
from cnn import ConvNet

device=torch.device('cuda' if torch.cuda.is_available() else 'cpu')

test_transformer=transforms.Compose([
    transforms.Resize((150,150)),
    transforms.ToTensor(),
    transforms.Normalize([0.5,0.5,0.5],
                        [0.5,0.5,0.5])
])

test_path = '../Data/test'

test_loader=torch.utils.data.DataLoader(
    torchvision.datasets.ImageFolder(root=test_path, transform=test_transformer),
    batch_size=16, shuffle=True
)

root=pathlib.Path(test_path)
classes=sorted([j.name.split('/')[-1] for j in root.iterdir()])

correct = 0
total = 0

PATH = "best_checkpoint.model" # when using basic cnn
net = ConvNet(len(classes))
net.load_state_dict(torch.load(PATH))
net.to(device)
net.eval()

# PATH = "snapshot.pt" # when using AlexNet model
# model = torch.load(PATH)
# model.eval()


with torch.no_grad():
    for data in test_loader:
        inputs, labels = data[0].to(device), data[1].to(device)
        outputs = net(inputs)
        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

print(f'Accuracy of the network on the 10000 test images: {100 * correct // total} %')