import cv2
import numpy as np
from sklearn.decomposition import PCA
import os

'''
Loops through all files in a folder (and sub folders) and performs principle component analysis augmentation as
 documented in the AlexNet paper.

NB: Make a copy of files first!
'''

def pca_augmentation( image_path ):
    pca = PCA()
    img = cv2.imread( image_path, cv2.IMREAD_UNCHANGED ) 
    if img.shape[2] == 3:
        blue,green,red = cv2.split(img) 
    if img.shape[2] == 4:
        blue,green,red, a = cv2.split(img) 
    
    random_val = np.random.normal(0, 0.1)
        
    red_transformed = pca.fit_transform(red)
    red_evals = pca.explained_variance_ratio_
    red_evects = pca.components_

    green_transformed = pca.fit_transform(green)
    green_evals = pca.explained_variance_ratio_
    green_evects = pca.components_


    blue_transformed = pca.fit_transform(blue)
    blue_evals = pca.explained_variance_ratio_
    blue_evects = pca.components_

    image = (np.dstack((red+(random_val*red_evals*red_evects.T).T, green+(random_val*green_evals*green_evects.T).T, blue+(random_val*blue_evals*blue_evects.T).T))).astype(np.uint8)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    cv2.imwrite(image_path, image)
    return

rootdir = '../augmented_foreign_vs_clear'

for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        pca_augmentation( os.path.join(subdir, file) )
    print(f'PCA performed on all files in {subdir}')    

print('PCA finished.')