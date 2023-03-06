import bpy

# bpy.data.cameras.remove(bpy.data.cameras['camera']) # remove camera

def add_camera():

    cam_data = bpy.data.cameras.new( 'camera' )
    cam = bpy.data.objects.new( 'camera', cam_data )
    bpy.context.collection.objects.link( cam )
    cam.location()