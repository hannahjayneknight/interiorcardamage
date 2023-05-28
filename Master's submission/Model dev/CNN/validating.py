import torch
import torch.nn as nn
from torchvision.transforms import transforms
import torchvision
import torch.optim as optim
import pathlib
import torch.nn.functional as F



device=torch.device('cuda' if torch.cuda.is_available() else 'cpu')
test_path = '../Data3/validate'
BATCH=1000
root=pathlib.Path(test_path)
classes=sorted([j.name.split('/')[-1] for j in root.iterdir()])

'''
--------------------------------- CNN -----------------------------------------
'''

from cnn import ConvNet

transformer=transforms.Compose([
    transforms.Resize((150,150)),
    transforms.ToTensor(),
    transforms.Normalize([0.5,0.5,0.5],
                        [0.5,0.5,0.5])
])

loader=torch.utils.data.DataLoader(
    torchvision.datasets.ImageFolder(root=test_path, transform=transformer),
    batch_size=BATCH, shuffle=True, num_workers=4, 
    pin_memory=True,
)

PATH = "best_checkpoint_Data3.model" # when using basic cnn
net = ConvNet(len(classes))
net.load_state_dict(torch.load(PATH))
net.to(device)
net.eval()

'''
--------------------------------- AlexNet -----------------------------------------
'''
# from AlexNet import AlexNet

# transformer = transforms.Compose([
#         transforms.Resize((227, 227)),
#         transforms.RandomCrop(224),
#         transforms.ToTensor(),
#         transforms.Normalize([0.5,0.5,0.5],
#                             [0.5,0.5,0.5])
# ])
# loader=torch.utils.data.DataLoader(
#     torchvision.datasets.ImageFolder(root=test_path, transform=transformer),
#     batch_size=BATCH, shuffle=False, num_workers=4,
#     pin_memory=True,
# )

# PATH = "snapshot.pt" # when using AlexNet model
# snapshot = torch.load(PATH)
# net = AlexNet(len(classes))
# net.load_state_dict(snapshot["MODEL_STATE"])
# net.to(device)
# net.eval()


'''
--------------------------------- Testing -----------------------------------------
'''
correct = 0
total = 0


with torch.no_grad():
    # method 1
    for data in loader:
        inputs, labels = data[0].to(device), data[1].to(device)
        outputs = net(inputs)
        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()
        #print("data tested")
    
    print(f'Accuracy of the network on the test images: {100 * correct // total} %')

    # method 2
    test_accuracy=0.0
    for i, (images,labels) in enumerate(loader):
        images,labels = images.to(device), labels.to(device)
            
        outputs=net(images)
        _,prediction=torch.max(outputs.data,1)
        test_accuracy+=int(torch.sum(prediction==labels.data))
    
    test_accuracy=test_accuracy/total
    
    print(' Test Accuracy: '+str(test_accuracy))
