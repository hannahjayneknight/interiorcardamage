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

NB: 
Total renders = number of objects (6) * number of car colours * 8 (number of shots) * n * m
With n=3 for test data, n=12 for train data and m=34, we prioritise having as many different 
dirty cars as possible with fewer renders per view of the car. 

If we reduced m and increased n, we would prioritise having more renders per view of the car.
'''

output_str = "../Data/test" # ../Data/train or test
n = 3 # n=3 for test data, n=12 for train data
m = 17


'''
---------------------------  SCRIPT HERE (DON'T CHANGE)  ------------------
'''

all_objects = bm.getallObjs()
# make all objects invisible at the start
bm.makeINvisible( all_objects )
array_index_count = 0
array_index = int(os.environ['PBS_ARRAY_INDEX'])
output_path = Path(output_str)


for obj_name in all_objects:
    # current count for each object
    DIR = str( output_str + "/" + obj_name ) 
    if (os.path.isdir(DIR) == True):
        count = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
    else:
        count = 0
    # loop through all objects
    obj = bpy.data.objects[ obj_name ]

    # for parallelism on HPC
    array_index_count += 1
    if array_index_count == array_index:
           
        # loop through car interior colour and change here
        colours = ['brown', 'black', 'cream']
        texture_dir = "../textures/Interior"
        for colour in colours:
            bm.change_car_colour(colour, texture_dir)

            for z in range(m):
                # 1. Make WHOLE car dirty
                for key in shots:
                    surface_obj = bpy.data.objects[ key ]
                    bm.add_dirt(surface_obj, obj)

                
                # 2. Take renders at different angles, positions and backgrounds    
                for key in shots:
                    surface_obj = bpy.data.objects[ key ]
                    for y in range(n):
                        bm.random_cam( shots[key] )
                        dir = "../Backgrounds/"
                        bm.randomly_change_background( dir )
                        active_cam_coll = bpy.context.scene.camera.users_collection[0].name
                        if (active_cam_coll in CAMs['camsL']):
                            bm.togglesidecar('R')  
                        if (active_cam_coll in CAMs['camsR']):
                            bm.togglesidecar('L')
                        if (active_cam_coll in CAMs['camsC']):
                            bm.togglesidecar('C')
                        bpy.context.scene.render.filepath = str( output_path / 'dirty' / f'{obj_name}_{str(count).zfill(6)}.png')
                        bpy.ops.render.render(write_still=True)
                        count += 1