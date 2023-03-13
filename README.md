# Interior Car Damage

Note: All blender files and renders (data) is exported to my OneDrive account since pushing them would exceed the GitHub limit and be blocked.

## Data Generation

### ```testing```
This was an initial test to get used to Imperial's HPC, make sure blender would run on the HPC and output into the desired folder.

### ```renaming```
Whenever I need to walk through a folder and rename the images (eg because I am merging folders).

### ```Object placement 1.blend```
All the python scripts in my ```Object placement 1.blend``` file. This was the first file I worked on for object placemement on my own laptop, so there are a lot of drafts as I figure out how I want the script to run.

### ```ObjPlacement```
Folder with code for object placement that has been uploaded and run on the HPC. All files have 27 objects in and randomly spawn them within the car and change the object's colour where appropriate. It chooses a random camera angle and background.


### ```LitterPlacement```

### ```SpawningMess```

### Queued jobs

| filename               | car interior | output path            | starting count | HPC settings |
|----------              |--------------|-------------           |----------------| ----------------|
| ```submitObjPlacement.pbs``` | Dark         | "../Data/DarkInterior" | 0              | #PBS -l walltime=04:00:00 #PBS -l select=1:ncpus=1:mem=24gb:ngpus=1:gpu_type=RTX6000
| ```submitObjPlacement2.pbs``` | Dark        | "../Data2/DarkInterior"| 0             | #PBS -l walltime=04:30:00 #PBS -l select=4:ncpus=1:mem=24gb:ngpus=8:gpu_type=RTX6000 #PBS -J 1-27 **(ie trying threading)**
| ```submitObjPlacement-cream.pbs``` | Cream | "../Data/CreamInterior" | 0 | #PBS -l walltime=121:30:00 #PBS -l select=1:ncpus=1:mem=24gb:ngpus=1:gpu_type=RTX6000 **(ie trying no threading, 1 gpu, but a really long walltime)**
| ```submitObjPlacement-brown.pbs``` | Brown | "../Data/Brown" | 0 | [to be decided]

NB: I think the -t command when running a blender file from the command line refers to the number of CPUs, not GPUs.

## Model building