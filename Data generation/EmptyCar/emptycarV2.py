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
CAR_NAME = "VWUP"



'''
---------------------------  SCRIPT HERE (DON'T CHANGE)  -------------------
'''

output_path = Path(output_str)


# current count for each object
DIR = str( output_str + "/" )
FILE_NAME = str("clear_" + CAR_NAME + "_")
count = len([name for name in os.listdir( DIR ) if FILE_NAME in name])



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
            bm.togglesidecarV2('R')
                
        if (active_cam_coll in CAMs['camsR']):
            bm.togglesidecarV2('L')
            
        if (active_cam_coll in CAMs['camsC']):
            bm.togglesidecarV2('C')

        # Update file path and render
        bpy.context.scene.render.filepath = str( output_path / f'clear_{CAR_NAME}_{str(count).zfill(6)}.png')
        bpy.ops.render.render(write_still=True)
        count += 1
