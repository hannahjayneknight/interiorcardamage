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
Total renders = number of car colours * 9 (number of shots) * n * m
With n=3 for test data, n=12 for train data and m=34, we prioritise having as many different 
dirty cars as possible with fewer renders per view of the car. 

If we reduced m and increased n, we would prioritise having more renders per view of the car.
'''

output_str = "../Data/test" # ../Data/train or test
n = 6 # n=6 for test data, n=18 for train data
# i.e. n*8 shots for one dirty car
# n*8*3 shots for each car colour
m = 102


'''
---------------------------  SCRIPT HERE (DON'T CHANGE)  ------------------
'''

array_index_count = 0
array_index = int(os.environ['PBS_ARRAY_INDEX'])
output_path = Path(output_str)
colours = ['brown', 'black', 'cream']
texture_dir = "../textures/Interior"

for colour in colours:
    # current count
    DIR = str( output_str + "/" + colour ) 
    if (os.path.isdir(DIR) == True):
        count = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
    else:
        count = 0

    bm.change_car_colour(colour, texture_dir)

    # for parallelism on HPC
    array_index_count += 1
    if array_index_count == array_index:

        for z in range(m):
            # 1. Make WHOLE car hairy
            for key in shots:
                surface_obj = bpy.data.objects[ key ]
                bm.add_hair(surface_obj)

            
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
                    bpy.context.scene.render.filepath = str( output_path / 'hairy' / f'hairy_{colour}_{str(count).zfill(6)}.png')
                    bpy.ops.render.render(write_still=True)
                    count += 1