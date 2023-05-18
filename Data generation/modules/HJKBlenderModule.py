import bpy
import random
from pathlib import Path
from os import listdir
from mathutils import Euler, Color
import os

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

def randomly_change_background( directory ):
    #directory = "../Backgrounds/"
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

def shots():
    '''
    A dict for where particles spawn and their corresponding cameras.
    '''
    shots = {
        'PassengerSeat' : [ 'CAMs-PassengerSeat' ],
        'RearSeats' : [ 'CAMs-RearSeatsR' ],
        'PassengerCarpet' : [ 'CAMs-PassengerCarpet' ],
        'Dashboard' : [ 'CAMs-DashboardL', 'CAMs-DashboardC', 'CAMs-DashboardR' ],
        'DriverCarpet' : [ 'CAMs-DriverCarpet' ],
        'RearCarpetL' : [ 'CAMs-RearCarpetL' ],
        'RearCarpetR' : [ 'CAMs-RearCarpetR' ],
        'RearShelf' : [ 'CAMs-RearShelfL', 'CAMs-RearShelfC', 'CAMs-RearShelfR' ],
        'DriverSeat': [ 'CAMs-DriverSeat' ],
    }
    return shots

def shots_test():
    shots_test = {
        'RearCarpetR' : [ 'CAMs-RearCarpetR' ],
        'RearShelf' : [ 'CAMs-RearShelfL', 'CAMs-RearShelfC', 'CAMs-RearShelfR' ],
    }
    return shots_test

def shots_test2():
    shots_test2 = {
        'RearCarpetR' : [ 'CAMs-RearCarpetR' ]
    }
    return shots_test2

def change_car_colour(colour, dir):
    car_nodes = {
        'FrontSeatMat': 'FrontSeatBaseColour',
        'RearSeatsMat': 'RearSeatsBaseColour',
        'RearShelfMat': 'RearShelfBaseColour',
        'DoorPanelFront': 'DoorPanelFrontBaseColour',
        'DoorPanelRear': 'DoorPanelRearBaseColour',
        'CenterConsole': 'CenterConsoleBaseColour',
        'Steeringwheel': 'SteeringwheelBaseColour',
        'Dashboard': 'DashboardBaseColour',
    }
    images = {
        'FrontSeatBaseColour' : 
            {
                'brown':r'/Seats/Front/Front_Seat_Base_Color Brown.png',
                'black':r'/Seats/Front/Front_Seat_Base_Color black.png',
                'cream':r'/Seats/Front/Front_Seat_Base_Color Tan.png' 
            },
        'RearSeatsBaseColour':
            {
                'brown':r'/Seats/Rear/Rear Seats_Base_Color Brown.png',
                'black':r'/Seats/Rear/Rear Seats_Base_Color Black.png',
                'cream':r'/Seats/Rear/Rear Seats_Base_Color Tan.png' 
            },
        'RearShelfBaseColour':
            {
                'brown':r'/Shell/Shell_Base_Color BlueBrown.png',
                'black':r'/Shell/Shell_Base_Color Black.png',
                'cream':r'/Shell/Shell_Base_Color Tan.png' 
            },
        'DoorPanelFrontBaseColour':
            {
                'brown':r'/DoorPanels/Front/DoorPanelFront_Base_Color Brown.png',
                'black':r'/DoorPanels/Front/DoorPanelFront_Base_Color Black.png',
                'cream':r'/DoorPanels/Front/DoorPanelFront_Base_Color Tan.png'
            },
        'DoorPanelRearBaseColour':
            {
                'brown':r'/DoorPanels/Rear/DoorPanelRear_Base_Color Brown.png',
                'black':r'/DoorPanels/Rear/DoorPanelRear_Base_Color Black.png',
                'cream':r'/DoorPanels/Rear/DoorPanelRear_Base_Color Tan.png'
            },
        'CenterConsoleBaseColour':
            {
                'brown':r'/CenterConsole/CenterConsole_Base_Color Brown.png',
                'black':r'/CenterConsole/CenterConsole_Base_Color Black.png',
                'cream':r'/CenterConsole/CenterConsole_Base_Color Tan.png'
            },
        'SteeringwheelBaseColour':
            {
                'brown':r'/SteeringWheel/Steeringwheel_Base_Color Black.png',
                'black':r'/SteeringWheel/Steeringwheel_Base_Color Black.png',
                'cream':r'/SteeringWheel/Steeringwheel_Base_Color Tan.png'
            },
        'DashboardBaseColour':
            {
                'brown':r'/Dashboard/Dashboard_Base_Color Brown.png',
                'black':r'/Dashboard/Dashboard_Base_Color BlackBlue.png',
                'cream':r'/Dashboard/Dashboard_Base_Color Tan.png'
            }
    }
    for key in car_nodes:
    
        mat = bpy.data.materials[ key ]
        nodes = [n for n in mat.node_tree.nodes if n.type == 'TEX_IMAGE']
        colour_node = [n for n in nodes if n.label == car_nodes[key]]

        #get image
        img_path = images[ car_nodes[key] ][ colour ]
        img_path_short = os.path.basename(os.path.normpath(img_path))
        full_path = dir + img_path 

        if img_path in bpy.data.images:
            image = bpy.data.images[ img_path_short ]
        else:
            image = bpy.data.images.load( full_path )


        #set image node
        colour_node[0].image = image

def add_dirt(surface_obj, obj):
    '''
    Adds dirt at random locations on a surface object.
    '''
    randomly_change_colour( obj.data.materials[0] )
    if len(surface_obj.particle_systems) != 0:
        remove_dirt(surface_obj)
    surface_obj.modifiers.new("dirt", type='PARTICLE_SYSTEM')
    part = surface_obj.particle_systems[0]
    part.seed = int(random.random()*100000000)
    part.vertex_group_density = "scatter"
    settings = part.settings
    settings.count = int(random.random()*1000)
    settings.particle_size = 0.005
    settings.render_type = 'OBJECT'
    settings.instance_object = obj
    settings.type = 'HAIR'
    settings.use_advanced_hair = True
    settings.use_rotations = True
    settings.rotation_mode = 'NOR_TAN'
    settings.rotation_factor_random = 1
    settings.size_random = 1
    settings.phase_factor_random = 1
    settings.distribution = 'JIT'
    settings.use_even_distribution = False
    settings.hair_length = random.random()*50 
    settings.emit_from = 'FACE'
    return  


def randomly_change_colour(material_to_change):
    """ Changes the Principled BSDF colour of a material to a random colour. 
    """
    color = Color()
    hue = random.random()
    color.hsv = (hue, 1, 1)
    rgba = [color.r, color.g, color.b, 1]
    material_to_change.node_tree.nodes['Principled BSDF'].inputs[0].default_value = rgba
    
def remove_dirt(surface_obj):
    surface_obj.modifiers.remove(surface_obj.modifiers["dirt"])


def add_hair(surface_obj):
    '''
    Adds hair at random locations on a surface object.
    '''
    randomly_change_colour( bpy.data.materials["Hair"] )
    
    if len(surface_obj.particle_systems) != 0:
        remove_hair(surface_obj)
    surface_obj.modifiers.new("hair", type='PARTICLE_SYSTEM')
    part = surface_obj.particle_systems[0]
    part.seed = int(random.random()*100000000)
    part.vertex_group_density = "scatter"
    settings = part.settings
    settings.count = int(random.random()*100)
    settings.hair_length = 0.001#random.random()*0.001
    settings.material_slot = 'Hair'
    settings.type = 'HAIR'
    settings.use_advanced_hair = True
    settings.render_type = 'PATH'
    settings.emit_from = 'FACE'
    settings.tangent_factor = 0.01
    settings.normal_factor = 0
    settings.child_type = 'INTERPOLATED'
    settings.rendered_child_count = int(random.random()*100)
    settings.kink = 'WAVE'
    settings.kink_amplitude = random.random()*0.01
    settings.tangent_phase = random.random()
    settings.child_size_random = 1   
    settings.root_radius = 0.01
    settings.tip_radius = 0.01
    return 

def remove_hair(surface_obj):
    surface_obj.modifiers.remove(surface_obj.modifiers["hair"])

  