import bpy
from random import randint
from math import radians

def random_vertex_selection():
    bpy.ops.object.mode_set(mode = 'OBJECT')
    obj = bpy.data.objects['Passenger Seat']
    bpy.ops.object.mode_set(mode = 'EDIT') 
    bpy.ops.mesh.select_mode(type="VERT")
    bpy.ops.mesh.select_all(action = 'DESELECT')
    bpy.ops.object.mode_set(mode = 'EDIT')
    
    print( len(obj.data.vertices) )
    
    #obj.data.vertices[randint(1, len(obj.data.vertices))].select = True
    #bpy.ops.object.mode_set(mode = 'EDIT') 
    

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

def add_obj(obj, vertex):
    '''
    Adds a specific object at a specific location.
    '''
    name = f'Cube 2'
    new_obj = bpy.data.objects.new(name=name, object_data=obj.data)
    new_obj.location = (vertex[0], vertex[1], vertex[2])
    angleX = randint(-10, 10)
    angleY = randint(-10, 10)
    angleZ = randint(-45, 45)
    new_obj.rotation_euler = (radians(angleX), radians(angleY), radians(angleZ))
    #scale = uniform(0.6, 3) # make this random
    #new_obj.scale = (scale, scale, scale)
    bpy.data.collections['Objs'].objects.link(new_obj)
    return

all_surface_objs = [
    # NB: Commented out when might struggle 'seeing' objects placed here
    'PassengerSeat',
    'DriverSeat',
    'RearSeats',
    'PassengerCarpet',
    'CenterConsole',
    'CenterConsolePocket',
    #'RearShelf',
    'DriverCarpet',
    'PassengerCarpet',
    #'RearCarpet',
    #'Floor', <-place on carpet instead of floor
    #'PlasticTrim', <- don't think it's common to leave on vertical surface XD
    #'Dashboard',
    #'InsideFrontDoors',
    #'InsideRearDoors',
]
    
surface_obj = bpy.data.objects['PassengerSeat']
obj = bpy.data.objects['KnitCap']

#add_obj(obj, [-0.44531, -0.235686, 0.48691] )

add_particles(surface_obj, obj)

locations =  [
    [-0.44531, -0.235686, 0.48691],
]
