import bpy
from random import randint
from pathlib import Path

def remove_particle_system(surface_obj):
    surface_obj.modifiers.remove(surface_obj.modifiers["random_obj"])
    
    
def add_particles(surface_obj, obj):
    '''
    Adds a specific object at a random location on a surface object.
    '''
    if len(surface_obj.particle_systems) != 0:
        remove_particle_system(surface_obj)
    surface_obj.modifiers.new("random_obj", type='PARTICLE_SYSTEM')
    part = surface_obj.particle_systems[0]
    part.seed = randint(0, 100000000)
    settings = part.settings
    settings.count = 1
    settings.particle_size = 0.1
    settings.render_type = 'OBJECT'
    settings.instance_object = obj
    settings.type = 'HAIR'
    settings.use_advanced_hair = True
    settings.use_rotations = True
    settings.rotation_mode = 'GLOB_X'
    settings.rotation_factor_random = 0.5
    #settings.phase_factor_random = 1
    settings.distribution = 'RAND'
    settings.hair_length = 10  
    return 

def change_camera(camera_name):
     bpy.context.scene.camera = bpy.data.objects[ camera_name ]
     
    

'''
---------------------------  SCRIPT HERE  -------------------------------
'''



obj_name = 'KnitCap'

obj = bpy.data.objects[ obj_name ]
output_path = Path("C:/Users/hanna/OneDrive - Imperial College London/Year 4 work/Master's/Car interior/Data generation V4")

shots = {
    'PassengerSeat' : 'CAM-PassengerSeat1',
    'RearSeats' : 'CAM-RearSeats1',
    'PassengerCarpet' : 'CAM-PassengerCarpet1',
    'Dashboard' : 'CAM-Dashboard1',
    'DriverCarpet' : 'CAM-DriverCarpet1',
    'RearCarpetL' : 'CAM-RearCarpetL1',
    'RearCarpetR' : 'CAM-RearCarpetR1',
    'RearShelf' : 'CAM-RearShelf1',
}


count = 0

for key in shots:
    # update surface_obj and camera
    surface_obj = bpy.data.objects[ key ]
    bpy.context.scene.camera = bpy.data.objects[ shots[key] ]
     

    for y in range(20):
        # add random object to scene
        add_particles(surface_obj, obj)
        
        # Update file path and render
        bpy.context.scene.render.filepath = str( output_path / obj_name / f'{str(count).zfill(6)}.png')
        bpy.ops.render.render(write_still=True)
        count += 1
        
    # remove final particle system so that it does not appear in next round
    remove_particle_system(surface_obj)