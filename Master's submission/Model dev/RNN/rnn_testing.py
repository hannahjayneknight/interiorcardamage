import torch
import torch.nn as nn
from torchvision.transforms import transforms
import torchvision
import torch.optim as optim
import pathlib
import torch.nn.functional as F



device=torch.device('cuda' if torch.cuda.is_available() else 'cpu')
test_path = '../foreign_vs_clear/test'
BATCH=1000
image_size = 150
input_size = image_size * image_size * 3  # Image size: 32x32 with 3 color channels
root=pathlib.Path(test_path)
classes=sorted([j.name.split('/')[-1] for j in root.iterdir()])

# Data transforms
transform = transforms.Compose([
    transforms.Resize((image_size, image_size)),     # Resize the image to 32x32
    transforms.ToTensor(),           # Convert image to tensor
    transforms.Normalize(            # Normalize image channels
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])


# Test the model
model.eval()
with torch.no_grad():
    correct = 0
    total = 0
    for images, labels in test_loader:
        images = images.to(device)
        labels = labels.to(device)
        images = images.view(-1, input_size)
        outputs = model(images)
        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

    accuracy = 100 * correct / total
    print(f"Test Accuracy: {accuracy:.2f}%")
















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

'''
--------------------------------- RNN -----------------------------------------
'''

transformer = transforms.Compose([
    transforms.Resize((image_size, image_size)),     # Resize the image to 32x32
    transforms.ToTensor(),           # Convert image to tensor
    transforms.Normalize(            # Normalize image channels
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
correct = 0
total = 0


with torch.no_grad():
    # method 1
    for data in loader:
        inputs, labels = data[0].to(device), data[1].to(device)
        images = images.view(-1, input_size)
        outputs = net(inputs)
        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

    print(f'Accuracy of the network on the test images: {100 * correct // total} %')

