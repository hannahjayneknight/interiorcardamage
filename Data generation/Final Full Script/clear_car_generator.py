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
output_str = "../Data/"
n = 6 # test data 
m = 25 # train data
background_dir = "../Backgrounds/" # directory where background images are
CAR_NAME = "VWUP"

'''
---------------------------  SCRIPT HERE (DON'T CHANGE)  -------------------
'''
# current count of renders
TRAIN_DIR = str( output_str + "/train/clear" )
TEST_DIR = str( output_str + "/test/clear" )
FILE_NAME = f'clear_{CAR_NAME}_'
if (os.path.isdir(TEST_DIR) == True):
    test_count = len([name for name in os.listdir( TEST_DIR ) if FILE_NAME in name])
else:
    test_count = 0
if (os.path.isdir(TRAIN_DIR) == True):
    train_count = len([name for name in os.listdir( TRAIN_DIR ) if FILE_NAME in name])
else:
    train_count = 0


for key in shots:   
    for y in range(n):
        bm.random_cam( shots[key] )
        bm.randomly_change_background( background_dir )
        active_cam_coll = bpy.context.scene.camera.users_collection[0].name
        if (active_cam_coll in CAMs['camsL']):
            bm.togglesidecarV2('R')    
        if (active_cam_coll in CAMs['camsR']):
            bm.togglesidecarV2('L')
        if (active_cam_coll in CAMs['camsC']):
            bm.togglesidecarV2('C')
        bpy.context.scene.render.filepath = str( Path(TEST_DIR) / f'{FILE_NAME}_{str(test_count).zfill(6)}.png')
        bpy.ops.render.render(write_still=True)
        test_count += 1
    for y in range(m):
        bm.random_cam( shots[key] )
        bm.randomly_change_background( background_dir )
        active_cam_coll = bpy.context.scene.camera.users_collection[0].name
        if (active_cam_coll in CAMs['camsL']):
            bm.togglesidecarV2('R')    
        if (active_cam_coll in CAMs['camsR']):
            bm.togglesidecarV2('L')
        if (active_cam_coll in CAMs['camsC']):
            bm.togglesidecarV2('C')
        bpy.context.scene.render.filepath = str( Path(TRAIN_DIR) / f'{FILE_NAME}_{str(train_count).zfill(6)}.png')
        bpy.ops.render.render(write_still=True)
        train_count += 1
