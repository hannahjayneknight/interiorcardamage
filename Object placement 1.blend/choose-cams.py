import bpy
from random import randint
from pathlib import Path
from os import listdir


def random_cam( CAMcollection ):
    '''
        Choose a random camera from a camera collection and activate it.
    '''
    #select your collection by name (in this case the collection named "Collection")
    col = bpy.data.collections[ CAMcollection ]

    objNum = len(col.objects)

    #Generate random number 
    randomIndex = random.randint(0,objNum - 1) 
    #use the random number to call a random object in the collection
    cam = col.objects[randomIndex]

    # activate camera
    bpy.context.scene.camera = bpy.data.objects[ cam.name ]
    
    
def activate_all_cams(CAMcollection, output_path, obj_name, renderNum):
    '''
        Loops through all the cameras in CAMcollection and renders a shot 
        with each of them.
        
        CAMcollection is the name of the camera collection (string). 
    '''
    for cam in bpy.data.collections[ CAMcollection ].all_objects:
        # activate camera
        bpy.context.scene.camera = bpy.data.objects[ cam.name ]
        
        #render
        bpy.context.scene.render.filepath = str( output_path / obj_name / f'{cam.name}{str(renderNum).zfill(6)}.png')
        bpy.ops.render.render(write_still=True)
        
def randomly_change_background():
    directory = "C:/Users/hanna/OneDrive - Imperial College London/Year 4 work/Master's/Car interior/Backgrounds/"
    background_images = listdir(directory)
    background_images = listdir(directory)
    randomIndex = randint(0, len(background_images)-1)
    background = bpy.data.images.load(str(directory + background_images[randomIndex]))
    bpy.data.materials['Background'].node_tree.nodes['Image Texture'].image = background

        
def random_cam2( CAMcollection ):
    '''
        Choose a random camera from a camera collection and activate it.
        
        Updates the position of the background plane so it is in view of the new camera.
    '''
    col = bpy.data.collections[ CAMcollection ]
    objNum = len(col.objects)
    randomIndex = randint(0,objNum - 1)
    cam = col.objects[randomIndex]
    bpy.context.scene.camera = bpy.data.objects[ cam.name ]
    bpy.data.objects[ "Plane" ].constraints["Child Of"].target = bpy.data.objects[ cam.name ]
    randomly_change_background()
    
    
def random_cam3( CAMcollectionarr ):
    '''
        Choose a random camera from an array of camera collections and activate the camera.
        
        Updates the position of the background plane so it is in view of the new camera.
    '''
    #choose collection from arr
    randomIndex1 = randint(0,len(CAMcollectionarr) - 1)
    CAMcollection = CAMcollectionarr[ randomIndex1 ]
    #choose random camera from collection
    col = bpy.data.collections[ CAMcollection ]
    randomIndex2 = randint(0,len(col.objects) - 1)
    cam = col.objects[randomIndex2]
    bpy.context.scene.camera = bpy.data.objects[ cam.name ]
    bpy.data.objects[ "Plane" ].constraints["Child Of"].target = bpy.data.objects[ cam.name ]
    randomly_change_background()
    
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






shots = {
    'PassengerSeat' : 'CAMs-PassengerSeat',
    'RearSeats' : 'CAMs-RearSeats',
    'PassengerCarpet' : 'CAMs-PassengerCarpet',
    'Dashboard' : 'CAMs-Dashboard',
    'DriverCarpet' : 'CAMs-DriverCarpet',
    'RearCarpetL' : 'CAMs-RearCarpetL',
    'RearCarpetR' : 'CAMs-RearCarpetR',
    'RearShelf' : 'CAMs-RearShelf',
}

shots2 = {
    'PassengerSeat' : [ 'CAMs-PassengerSeat' ],
    'RearSeats' : [ 'CAMs-RearSeatsR' ], 
    'PassengerCarpet' : [ 'CAMs-PassengerCarpet' ],
    'Dashboard' : [ 'CAMs-DashboardL', 'CAMs-DashboardC', 'CAMs-DashboardR' ],
    'DriverCarpet' : [ 'CAMs-DriverCarpet' ],
    'RearCarpetL' : [ 'CAMs-RearCarpetL' ],
    'RearCarpetR' : [ 'CAMs-RearCarpetR' ],
    'RearShelf' : [ 'CAMs-RearShelfL', 'CAMs-RearShelfC', 'CAMs-RearShelfR' ],
}
        

    

active_cam_coll = bpy.context.scene.camera.users_collection[0].name
CAMs = getallCAMs()
if (active_cam_coll in CAMs['camsL']):
    print("Left cam")
        
if (active_cam_coll in CAMs['camsR']):
    print("Right cam")
    
if (active_cam_coll in CAMs['camsC']):
    print("Centre cam")


''' -------------------OLD-------------------------'''
#random_cam2('CAMs-RearSeats')
#print(CAMs)

#random_cam3( shots2[ 'RearSeats'] )

#for key in shots2:
#    random_cam3( shots[key] )