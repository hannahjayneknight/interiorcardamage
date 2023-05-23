import os

output_str = "../Data/test" # ../Data/train or test
obj_name = "KnitCap"

DIR = str( output_str + "/" + obj_name )
FILE_NAME = str(obj_name + "_")
count = len([name for name in os.listdir( DIR ) if FILE_NAME in name])
print( count )