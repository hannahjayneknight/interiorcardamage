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

#shots for testing
#shots = bm.shots_test()
#shots = bm.shots_test2()


#camera dictionary
CAMs = bm.getallCAMs()

'''
---------------------------  SCRIPT HERE  -------------------------------
'''

all_objects = bm.getallObjs()
# make all objects invisible at the start
bm.makeINvisible( all_objects )


output_path = Path("./testingdata")

# choose a random object
obj_num = int(random.random()*(len(all_objects)-1))
obj_name = all_objects[ obj_num ]
obj = bpy.data.objects[ obj_name ]
# choose a random surface
surfaces = list( shots )
surf_num = int(random.random()*(len(surfaces)-1))
surface_obj = bpy.data.objects[ surfaces[ surf_num ] ]

# add random object to surface
bm.add_particles(surface_obj, obj)
# change camera angle
bm.random_cam( shots[ surfaces[ surf_num ] ] )
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
bpy.context.scene.render.filepath = str( output_path / obj_name / f'{str(int(random.random()*1000000)).zfill(6)}.png')
bpy.ops.render.render(write_still=True)

bm.remove_particle_system(surface_obj)