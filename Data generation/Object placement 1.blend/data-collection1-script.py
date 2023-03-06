import bpy
import math
import random
import time
from mathutils import Euler, Color
from pathlib import Path

def randomly_rotate_object(obj_to_change): # use this for the camera later
    """ Applies a random rotation to an object.
    """
    random_rot = (random.random()*2*math.pi, random.random()*2*math.pi, random.random()*2*math.pi)
    obj_to_change.rotation_euler = Euler(random_rot, 'XYZ')
    
def randomly_change_colour(material_to_change):
    """ Changes the Principled BSDF colour of a material to a random colour. 
    """
    color = Color()
    hue = random.random()
    color.hsv = (hue, 1, 1)
    rgba = [color.r, color.g, color.b, 1]
    material_to_change.node_tree.nodes['Principled BSDF'].inputs[0].default_value = rgba
   

# Scene collections (cars) to render
cars = ['car_1', 'car_2']
obj_count = len(cars)

# Number of images to generate of each object for each split of the dataset
# Example: ('train', 100) means generate 100 images of each 'A', 'B' & 'C' resulting in 300 training images
obj_renders_per_split = [('train', 3), ('val', 2), ('test', 1)] # test with a small number before increasing the size of the dataset!

# Output path
output_path = Path("C:/Users/hanna/OneDrive - Imperial College London/Year 4 work/Master's/Car interior/Data generation")


# For each dataset split (train/val/test), multiply the number of renders per object by 
# the number of objects (3, since we have A, B and C). Then compute the sum.
# This will be the total number of renders performed.
total_render_count = sum([obj_count*r[1] for r in obj_renders_per_split])

# Set all objects to be hidden
for name in cars:
    bpy.data.collections[name].hide_render = True
    
# Track the starting image index for each object loop
start_idx = 0

# Keep track of start time in seconds
start_time = time.time()

# Loop through each split of the dataset
for split_name, renders_per_object in obj_renders_per_split:
    print(f'Starting split: {split_name} ︱Total renders: {renders_per_object*obj_count}')
    print('=============================================')
    
    # Loop through the objects by name
    for car in cars:
        print(f'Starting object: {split_name}/{car}')
        print('=============================================')
        
        # Get the next object and make it visible
        car_to_render = bpy.data.collections[car]
        car_to_render.hide_render = False
        car_num = car.split("_")[1]
        

        # Loop through all image renders for this object
        for i in range(start_idx, start_idx + renders_per_object):
            # Change car here
                        
            # Change colour of car seats
            obj_name = "Passenger Seat" + str(car_num);
            obj = bpy.context.scene.objects[obj_name]
            randomly_change_colour(obj.material_slots[0].material)
            
            # Log status
            print(f'Rendering image {i+1} of {total_render_count}')
            seconds_per_render = (time.time()-start_time) / (i+1)
            seconds_remaining = seconds_per_render*(total_render_count-i-1)
            print(f'Estimated time remaining: {time.strftime("%H:%M:%S", time.gmtime(seconds_remaining))}')
            
            # Update file path and render
            bpy.context.scene.render.filepath = str(output_path / split_name / car / f'{str(i).zfill(6)}.png')
            bpy.ops.render.render(write_still=True)

            
        # Hide the object, we're done with it
        car_to_render.hide_render = True
        
        # Update the starting image index
        start_idx += renders_per_object
        
        
# Set all objects to be visible in rendering
for name in cars:
    bpy.data.collections[name].hide_render = False