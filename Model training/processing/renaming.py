import os
path = "C:/Users/hanna/Desktop/git/interiorcardamage/Data/Data generation V5/KnitCap"
files = os.listdir(path)


for index, file in enumerate(files):
    newindex = index + 240
    os.rename(os.path.join(path, file), os.path.join(path, ''.join([str(newindex).zfill(6), '.png'])))