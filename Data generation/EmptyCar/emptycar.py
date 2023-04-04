import sys
import bpy
import random
from pathlib import Path
from os import listdir
from mathutils import Euler, Color
import os
sys.path.insert(0, "../modules")
import HJKBlenderModule as bm

'''
---------------------------  FOR REFERENCE  -----------------------------
'''
#where particles spawn and their corresponding cameras
shots = bm.shots()

#camera dictionary
CAMs = bm.getallCAMs()

'''
---------------------------  VARIABLES TO CHANGE  -----------------------
'''
output_str = "../Data/test/clear" # train or test
n = 6 # n=6 for test data, n=25 for train data



'''
---------------------------  SCRIPT HERE (DON'T CHANGE)  -------------------
'''

output_path = Path(output_str)


DIR = str( output_str + "/" ) 
if (os.path.isdir(DIR) == True):
    count = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
else:
    count = 0

# loop through car interior colour and change here
colours = ['brown', 'black', 'cream']
texture_dir = "../textures/Interior"
for colour in colours:
    bm.change_car_colour(colour, texture_dir)

    for key in shots:   

        for y in range(n):
            # change camera angle 
            bm.random_cam( shots[key] )
            # change background
            dir = "../Backgrounds/"
            bm.randomly_change_background( dir )
            
            # the current active camera's collection
            active_cam_coll = bpy.context.scene.camera.users_collection[0].name
            
            # randomly toggle doors open or closed depending on which camera is active
            if (active_cam_coll in CAMs['camsL']):
                bm.togglesidecar('R')
                    
            if (active_cam_coll in CAMs['camsR']):
                bm.togglesidecar('L')
                
            if (active_cam_coll in CAMs['camsC']):
                bm.togglesidecar('C')

            # Update file path and render
            bpy.context.scene.render.filepath = str( output_path / f'clear_{str(count).zfill(6)}.png')
            bpy.ops.render.render(write_still=True)
            count += 1
