'''
Functions to change the background image of a render in blender's python api.

'''

import bpy
from pathlib import Path
from os import listdir
from random import randint

directory = "C:/Users/hanna/OneDrive - Imperial College London/Year 4 work/Master's/Car interior/Backgrounds"
output_path = Path('')
background_images = listdir(directory)

def generate_for_all():
    i=0
    for f in directory.iterdir():
        image = bpy.data.images.load(str(f))
        bpy.data.materials['Background'].node_tree.nodes['Image Texture'].image = image
        bpy.context.scene.render.filepath = str(output_path / f'{str(i).zfill(6).png}')
        bpy.ops.render.render(write_stil=True)
        i+=1

def randomly_change_background(directory):
    background_images = listdir(directory)
    randomIndex = randint(0, len(background_images))
    background = bpy.data.images.load(str(background_images[randomIndex])) # check this line!
    bpy.data.materials['Background'].node_tree.nodes['Image Texture'].image = background


