import cv2
import numpy as np
from sklearn.decomposition import PCA
import os

'''
Loops through all files in a folder (and sub folders) and performs principle component analysis augmentation.

This form of augmentation is documented in the AlexNet paper.

NB: Make a copy of files first!
'''

def pca_augmentation( image_path ):
    '''
    Randomly changes image intensity for training. 
    '''
    pca = PCA()
    img = cv2.imread( image_path, cv2.IMREAD_UNCHANGED ) 
    #img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    blue,green,red, a = cv2.split(img) 
    red_transformed = pca.fit_transform(red)
    red_inverted = pca.inverse_transform(red_transformed)

    green_transformed = pca.fit_transform(green)
    green_inverted = pca.inverse_transform(green_transformed)


    blue_transformed = pca.fit_transform(blue)
    blue_inverted = pca.inverse_transform(blue_transformed)

    random_val = np.random.normal(0, 0.1)
    img_compressed = (np.dstack((red_inverted+(random_val*red_inverted), green_inverted+(random_val*green_inverted), blue_inverted+(random_val*blue_inverted)))).astype(np.uint8)
    image = cv2.cvtColor(img_compressed, cv2.COLOR_BGR2RGB)
    cv2.imwrite(image_path, image)
    return

rootdir = '../'

for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        pca_augmentation( os.path.join(subdir, file) )
    print(f'PCA performed on all files in {subdir}')    

print('PCA finished.')