import torch
import torch.nn as nn
import torch.optim as optim
import torchvision.transforms as transforms
from torch.utils.data import DataLoader
from torchvision.datasets import ImageFolder
import pathlib
from rnn import RNN


device=torch.device('cuda' if torch.cuda.is_available() else 'cpu')
test_path = '../foreign_vs_clear/test'
BATCH=1000
hidden_size = 128
num_layers = 2
root=pathlib.Path(test_path)
num_classes=sorted([j.name.split('/')[-1] for j in root.iterdir()])
image_size = 150
input_size = image_size * image_size * 3  

'''
--------------------------------- RNN -----------------------------------------
'''

transformer = transforms.Compose([
    transforms.Resize((image_size, image_size)), 
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

loader=DataLoader(
    ImageFolder(root=test_path, transform=transformer),
    batch_size=BATCH, shuffle=True, num_workers=4,
    pin_memory=True,
)

PATH = "rnn_foreign_obj_vs_clear.model"
net = RNN(input_size, hidden_size, num_layers, num_classes).to(device)
net.load_state_dict(torch.load(PATH))
net.to(device)
net.eval()


'''
--------------------------------- Testing -----------------------------------------
'''

net.eval()
with torch.no_grad():
    correct = 0
    total = 0
    for images, labels in loader:
        images = images.to(device)
        labels = labels.to(device)
        images = images.view(-1, input_size)
        outputs = net(images)
        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

    accuracy = 100 * correct / total
    print(f"Test Accuracy: {accuracy:.2f}%")

