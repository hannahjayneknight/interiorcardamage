import torch
import torch.nn as nn
import torch.optim as optim
import torchvision.transforms as transforms
from torch.utils.data import DataLoader
from torchvision.datasets import ImageFolder
from torch.utils.data import Subset
import numpy as np
from rnn import RNN

# Set device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Hyperparameters
image_size = 150
input_size = image_size * image_size * 3  # Image size: 32x32 with 3 color channels
hidden_size = 128
num_layers = 2
num_classes = 2
num_epochs = 100
learning_rate = 0.001

# Data transforms
transformer = transforms.Compose([
    transforms.Resize((image_size, image_size)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

# Load the dataset
train_path = "../Data/train"
train_dataset = ImageFolder(root=train_path, transform=transformer)

n = 1275

train_dataset_subset = Subset(train_dataset, np.random.choice(len(train_dataset), n, replace=False))

train_loader=DataLoader(
    train_dataset_subset,
    batch_size=32, shuffle=True, num_workers=4,
    pin_memory=True,
)

# Initialize the model
model = RNN(input_size, hidden_size, num_layers, num_classes).to(device)

# Loss and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=learning_rate)

# Training loop
total_step = len(train_loader)
for epoch in range(num_epochs):
    for i, (images, labels) in enumerate(train_loader):
        images = images.to(device)
        labels = labels.to(device)

        # Reshape images
        images = images.view(-1, input_size)

        # Forward pass
        outputs = model(images)
        loss = criterion(outputs, labels)

        # Backward and optimize
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    torch.save(model.state_dict(),'rnn_foreign_obj_vs_clear.model')
    print(f"Epoch [{epoch}], Loss: {loss.item():.4f}")
