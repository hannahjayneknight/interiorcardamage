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
output_str = "../testing/testingdata" # ../Data/train or test
n = 6 # n=6 for test data, n=25 for train data


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

            for key in shots:
                # update surface_obj
                surface_obj = bpy.data.objects[ key ]     

                for y in range(n):
                    # add random object to scene
                    bm.add_particles(surface_obj, obj)
                    # change camera angle 
                    bm.random_cam( shots[key] )
                    # change background
                    dir = "../Backgrounds/"
                    bm.randomly_change_background( dir )
                    # change colour of object
                    bm.change_colorramp( obj)
                    
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
                    bpy.context.scene.render.filepath = str( output_path / obj_name / f'{obj_name}_{str(count).zfill(6)}.png')
                    bpy.ops.render.render(write_still=True)
                    count += 1
                    
                # remove final particle system so that it does not appear in next round
                bm.remove_particle_system(surface_obj)