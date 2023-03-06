import bpy
import random
from pathlib import Path
from os import listdir
from mathutils import Euler, Color

'''
---------------------------  FUNCTIONS  --------------------------------
''' 

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
    part.seed = int(random.random()*100000000)
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
     
def random_cam( CAMcollectionarr ):
    '''
        Choose a random camera from an array of camera collections and activate the camera.
        
        Updates the position of the background plane so it is in view of the new camera.
    '''
    #choose collection from arr
    randomIndex1 = int(random.random()*(len(CAMcollectionarr) - 1))
    CAMcollection = CAMcollectionarr[ randomIndex1 ]
    #choose random camera from collection
    col = bpy.data.collections[ CAMcollection ]
    randomIndex2 = int(random.random()*(len(col.objects) - 1))
    cam = col.objects[randomIndex2]
    bpy.context.scene.camera = bpy.data.objects[ cam.name ]
    bpy.data.objects[ "Plane" ].constraints["Child Of"].target = bpy.data.objects[ cam.name ]

def randomly_change_background():
    directory = "../Backgrounds/"
    background_images = listdir(directory)
    background_images = listdir(directory)
    randomIndex = int(random.random()*(len(background_images)-1))
    background = bpy.data.images.load(str(directory + background_images[randomIndex]))
    bpy.data.materials['Background'].node_tree.nodes['Image Texture'].image = background
    
def makevisible( arr ):
    '''
    Makes everything in the arr visible when viewing and rendering.
    '''
    for obj in arr:
        obj = bpy.context.scene.objects[ obj ]
        obj.hide_render = False
        obj.hide_viewport = False
        obj.hide_set(False)
        
def makeINvisible( arr ):
    '''
    Makes everything in the arr invisible when viewing and rendering.
    '''
    for obj in arr:
        obj = bpy.context.scene.objects[ obj ]
        obj.hide_render = True
        obj.hide_viewport = True
        obj.hide_set(True)
        
def random_bool():
    '''
    Generates a 0 or 1 randomly using the random.random() function (so we avoid using
    the slow random.randint() function).
    '''
    my_random_float = random.random()
    if my_random_float > .5:
        my_rand_int = 1
    else:
        my_rand_int = 0
    return my_rand_int
    
def togglesidecar( side ):
    # left/ driver side of car
    L = [
            'InsideFrontDoorsL',
            'InsideRearDoorsL',
            'Door Front HandleL',
            'Door Rear HandleL',
            'DoorFrontL',
            'DoorRearL',
            'FrontDoorGlassL',
            'RearDoorGlassL',
            'MirrorTurnsignal ReflectorL',
            'MIrrorTurnSignal GlassL',
            'MIrrorL',
    ]

    # right/ passenger side of the car
    R =  [
            'InsideFrontDoorsR',
            'InsideRearDoorsR',
            'Door Front HandleR',
            'Door Rear HandleR',
            'DoorFrontR',
            'DoorRearR',
            'FrontDoorGlassR',
            'RearDoorGlassR',
            'MirrorTurnsignal ReflectorR',
            'MIrrorTurnSignal GlassR',
            'MIrrorR',
    ]
    # Set all objects to be hidden
    makeINvisible(L)
    makeINvisible(R)
    
    # Set all objects on desired side to be visible
    if (side=='L'):
        if (random_bool() == 1):
            makevisible(L)
    if (side=='R'):
        if (random_bool() == 1):
            makevisible(R)
    # if camera in the centre, we make both sides visible
    if (side=='C'):
        if (random_bool() == 1):
            makevisible(L)
        if (random_bool() == 1):
            makevisible(R)

def getallCAMs():
    '''
    Returns a dictionary with all cameras and what view of the car they hold (left, right or centre 
    
    where left is the driver side). 
    '''
    CAMs = {
        'camsL' : [],
        'camsR' : [],
        'camsC' : []
    }
    
    for cam_coll in bpy.data.collections['CAMsLEFT'].children:
        CAMs[ 'camsL' ].append(cam_coll.name)
        
    for cam_coll in bpy.data.collections['CAMsRIGHT'].children:
        CAMs[ 'camsR' ].append(cam_coll.name)
        
    for cam_coll in bpy.data.collections['CAMsCENTRE'].children:
        CAMs[ 'camsC' ].append(cam_coll.name)
        
    return CAMs

def getallObjs():
    '''
    Returns an array with all the random objects in the collection "Objs" which will spawn 
    in the car. 
    '''
    objs = []
    for object in bpy.data.collections['OBJS'].objects:
        objs.append(object.name)
    return objs

def change_colorramp( obj ):
    """ Changes the 'color' value of an object's ColorRamp. 
    """
    if "ColorRamp" in obj.active_material.node_tree.nodes:
        colorramp = obj.active_material.node_tree.nodes["ColorRamp"]
        #if (colorramp
        
        color = Color()
        H = random.random()
        S = random.random()
        V = random.random()
        color.hsv = (H, S, V)
        rgba = [color.r, color.g, color.b, 1]
        colorramp.color_ramp.elements[1].color = rgba
  

'''
---------------------------  FOR REFERENCE  -----------------------------
'''  

#where particles spawn and their corresponding cameras
shots = {
    'PassengerSeat' : [ 'CAMs-PassengerSeat' ],
    'RearSeats' : [ 'CAMs-RearSeatsR' ], 
    'PassengerCarpet' : [ 'CAMs-PassengerCarpet' ],
    'Dashboard' : [ 'CAMs-DashboardL', 'CAMs-DashboardC', 'CAMs-DashboardR' ],
    'DriverCarpet' : [ 'CAMs-DriverCarpet' ],
    'RearCarpetL' : [ 'CAMs-RearCarpetL' ],
    'RearCarpetR' : [ 'CAMs-RearCarpetR' ],
    'RearShelf' : [ 'CAMs-RearShelfL', 'CAMs-RearShelfC', 'CAMs-RearShelfR' ],
}


#camera dictionary
CAMs = getallCAMs()


'''
---------------------------  SCRIPT HERE  -------------------------------
'''



all_objects = getallObjs()
# make all objects invisible at the start
makeINvisible( all_objects )


output_path = Path("../Data/DarkInterior")


for obj_name in all_objects:
    # reset count for each object
    count = 0
    # loop through all objects
    obj = bpy.data.objects[ obj_name ]

    for key in shots:
        # update surface_obj
        surface_obj = bpy.data.objects[ key ]     

        for y in range(25):
            # add random object to scene
            add_particles(surface_obj, obj)
            # change camera angle 
            random_cam( shots[key] )
            # change background
            randomly_change_background()
            # change colour of object
            change_colorramp( obj)
            
            # the current active camera's collection
            active_cam_coll = bpy.context.scene.camera.users_collection[0].name
            
            # randomly toggle doors open or closed depending on which camera is active
            if (active_cam_coll in CAMs['camsL']):
                togglesidecar('R')
                    
            if (active_cam_coll in CAMs['camsR']):
                togglesidecar('L')
                
            if (active_cam_coll in CAMs['camsC']):
                togglesidecar('C')

            # Update file path and render
            bpy.context.scene.render.filepath = str( output_path / obj_name / f'{obj_name}_{str(count).zfill(6)}.png')
            bpy.ops.render.render(write_still=True)
            count += 1
            
        # remove final particle system so that it does not appear in next round
        remove_particle_system(surface_obj)