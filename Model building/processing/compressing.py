'''
Loop through a directory of images, compress them and resave to a new directory.

Discovered the importance of this after realising the outputted image sizes from Blender 
(i.e. my raw data) are all 2.40 MB!!! Dataloader was INCREDIBLY slow so want to try compressing images first.

Size of my blender generated files: 
    
    1920 x 1080

    72 dpi

    32 bit

    Size: 2-3MB 
'''

from PIL import Image
import os
from pathlib import Path

'---------------------------------------ATTEMPT 1-------------------------------------------------'


def compress( dir, new_dir ):
    '''
    dir is the directory with the raw image files in. 

    new_dir is the directory where the compressed images will be saved.

    This works for compressing one folder and exporting it to a new folder.

    '''
    files = os.listdir( dir )

    for index, file in enumerate(files): # loop through rough route directory

        foo = Image.open(os.path.join(dir, file))
        size = foo.size

        # downsize the image with an ANTIALIAS filter (gives the highest quality)
        foo = foo.resize((256, 256),resample=Image.LANCZOS)
        

        new_save_path = os.path.join(new_dir, ''.join([str(index).zfill(6), '.png']))

        foo.save(new_save_path, optimize=True, quality=95) #  could try with quality=85


dir = "C:/Users/hanna/Desktop/git/interiorcardamage/Data/test/KnitCap"
new_dir = "C:/Users/hanna/Desktop/git/interiorcardamage/Data/compressed"

#compress( dir, new_dir )

'---------------------------------------ATTEMPT 2-------------------------------------------------'


import os
dir = 'C:/Users/hanna/Desktop/git/interiorcardamage/Data2/raw'
#newdir = 'C:/Users/hanna/Desktop/git/interiorcardamage/Data2/processed'

def compress_to_processed( rootdir ):
    '''
    Loops through an ImageFolder structure, compresses the images and 
    saves them to the "processed" folder with the same sub-directory structure
    as rootdir.
    '''
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            x = os.path.join(subdir, file)

            foo = Image.open(x)
            foo = foo.resize((256, 256),resample=Image.LANCZOS)

            
            start = Path(*Path(x).parts[:-4])
            middle = Path("processed")
            end = Path(*Path(x).parts[-3:]) 
            new_save_path = Path(start / middle / end)

            foo.save(new_save_path, optimize=True, quality=95)
            #print(new_save_path)


compress_to_processed( dir )
