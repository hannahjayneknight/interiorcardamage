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
# dict mapping interior surface that particles are spawned on with cameras
shots = bm.shots()

#camera dictionary
CAMs = bm.getallCAMs()

'''
---------------------------  VARIABLES TO CHANGE  -----------------------
'''

output_str = "../VWUP" # directory to save renders
background_dir = "../Backgrounds/" # directory where background images are
CAR_NAME = "VWUP" # current car model

# number of renders taken per view of the car (per key in 'shots')
n_foreign = 6 # foreign-object test data
m_foreign = 25 # foreign-object train data
n_dirty = 3 # dirty test data
m_dirty = 6 # dirty train data
n_hairy = 3 # hairy test data
m_hairy = 6 # hairy train data

# number of full dirty or hairy cars
dirty_cars = 17
hairy_cars = 50



'''
---------------------------  SCRIPT HERE (DON'T CHANGE)  ------------------
'''

# make all particles that will be spawned invisible at the start
foreign_objects = bm.getObjsInCollection( 'OBJS' )
dirt_objects = bm.getObjsInCollection( 'DIRT' )
all_messes = foreign_objects + dirt_objects + ["hairy"] # note this is an efficient method for concatonating lists: https://stackoverflow.com/questions/12088089/python-list-concatenation-efficiency
bm.makeINvisible( foreign_objects )
bm.makeINvisible ( dirt_objects )
# for parallelism on HPC, in job script file J 1-N where N is the length of all_objects+1 (for hairy sub-job)
array_index_count = 0
array_index = int(os.environ['PBS_ARRAY_INDEX'])



for mess_name in all_messes:
    FILE_NAME = f'{mess_name}_{CAR_NAME}'

    ######################################################
    # FOREIGN OBJECT
    ######################################################

    if mess_name in foreign_objects:
        # current count of renders in output folder, so files are not overwritten
        TRAIN_DIR = f'{output_str}/train/foreign-object'
        TEST_DIR = f'{output_str}/test/foreign-object'
        if (os.path.isdir(TEST_DIR) == True):
            test_count = len([name for name in os.listdir( TEST_DIR ) if FILE_NAME in name])
        else:
            test_count = 0
        if (os.path.isdir(TRAIN_DIR) == True):
            train_count = len([name for name in os.listdir( TRAIN_DIR ) if FILE_NAME in name])
        else:
            train_count = 0

        obj = bpy.data.objects[ mess_name ] # blender object
        
        array_index_count += 1
        if array_index_count == array_index:

            for key in shots:
                surface_obj = bpy.data.objects[ key ] # interior surface that particles are spawned on

                # 'TEST' DATA
                for y in range(n_foreign):
                    bm.add_particles(surface_obj, obj)
                    bm.random_cam( shots[key] )
                    bm.randomly_change_background( background_dir )
                    bm.change_colorramp( obj)

                    # the current active camera's collection
                    active_cam_coll = bpy.context.scene.camera.users_collection[0].name

                    # randomly toggle doors open or closed depending on which camera is active
                    if (active_cam_coll in CAMs['camsL']):
                        bm.togglesidecarV2('R')
                    if (active_cam_coll in CAMs['camsR']):
                        bm.togglesidecarV2('L')
                    if (active_cam_coll in CAMs['camsC']):
                        bm.togglesidecarV2('C')

                    #render
                    bpy.context.scene.render.filepath = str( Path(TEST_DIR) / f'{FILE_NAME}_{str(test_count).zfill(6)}.png')
                    bpy.ops.render.render(write_still=True)
                    test_count += 1

                # remove final particle system so that it does not appear in next round
                bm.remove_particle_system(surface_obj)
                print( "Finished generating TEST data for foreign objects." )

                # 'TRAIN' DATA
                for y in range(m_foreign):
                    bm.add_particles(surface_obj, obj)
                    bm.random_cam( shots[key] )
                    bm.randomly_change_background( background_dir )
                    bm.change_colorramp( obj)
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
                bm.remove_particle_system(surface_obj)
                print( "Finished generating TRAIN data for foreign objects." )
        
    ######################################################
    # DIRTY CAR
    ######################################################

    if mess_name in dirt_objects:
        TRAIN_DIR = f'{output_str}/train/dirty'
        TEST_DIR = f'{output_str}/test/dirty'
        if (os.path.isdir(TEST_DIR) == True):
            test_count = len([name for name in os.listdir( TEST_DIR ) if FILE_NAME in name])
        else:
            test_count = 0
        if (os.path.isdir(TRAIN_DIR) == True):
            train_count = len([name for name in os.listdir( TRAIN_DIR ) if FILE_NAME in name])
        else:
            train_count = 0

        obj = bpy.data.objects[ mess_name ]

        array_index_count += 1
        if array_index_count == array_index:

                # 'TEST' DATA
                for z in range(dirty_cars):
                    # 1. Make WHOLE car dirty
                    for key in shots:
                        surface_obj = bpy.data.objects[ key ]
                        bm.add_dirt(surface_obj, obj)

                    # 2. Take renders at different angles, positions and backgrounds    
                    for key in shots:
                        surface_obj = bpy.data.objects[ key ]
                        for y in range(n_dirty):
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
                print( "Finished generating TEST data for dirty car." )

                # 'TRAIN' DATA
                for z in range(dirty_cars):
                    for key in shots:
                        surface_obj = bpy.data.objects[ key ]
                        bm.add_dirt(surface_obj, obj)
                    for key in shots:
                        surface_obj = bpy.data.objects[ key ]
                        for y in range(m_dirty):
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
                print( "Finished generating TRAIN data for dirty car." )

    ######################################################
    # HAIRY CAR
    ######################################################

    if mess_name == "hairy":
        TRAIN_DIR = f'{output_str}/train/hairy'
        TEST_DIR = f'{output_str}/test/hairy'
        if (os.path.isdir(TEST_DIR) == True):
            test_count = len([name for name in os.listdir( TEST_DIR ) if FILE_NAME in name])
        else:
            test_count = 0
        if (os.path.isdir(TRAIN_DIR) == True):
            train_count = len([name for name in os.listdir( TRAIN_DIR ) if FILE_NAME in name])
        else:
            train_count = 0
        obj = bpy.data.objects[ mess_name ]

        array_index_count += 1
        if array_index_count == array_index:

            # 'TEST' DATA
            for z in range(hairy_cars):
                # 1. Make WHOLE car hairy
                for key in shots:
                    surface_obj = bpy.data.objects[ key ]
                    bpy.context.view_layer.objects.active = surface_obj
                    bm.add_hair(surface_obj)

                # 2. Take renders at different angles, positions and backgrounds    
                for key in shots:
                    surface_obj = bpy.data.objects[ key ]
                    for y in range(n_hairy):
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
            print( "Finished generating TEST data for hairy car." )

            # 'TRAIN' DATA
            for z in range(hairy_cars):
                # 1. Make WHOLE car hairy
                for key in shots:
                    surface_obj = bpy.data.objects[ key ]
                    bpy.context.view_layer.objects.active = surface_obj
                    bm.add_hair(surface_obj)

                # 2. Take renders at different angles, positions and backgrounds    
                for key in shots:
                    surface_obj = bpy.data.objects[ key ]
                    for y in range(m_hairy):
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
            print( "Finished generating TRAIN data for hairy car." )