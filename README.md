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

| filename               | car interior | output path            | HPC settings |
|----------              |--------------|-------------           | ----------------|
| ```submitObjPlacement.pbs``` | Dark         | "../Data/DarkInterior" |  #PBS -l walltime=04:00:00 #PBS -l select=1:ncpus=1:mem=24gb:ngpus=1:gpu_type=RTX6000
| ```submitObjPlacement2.pbs``` | Dark        | "../Data2/DarkInterior"|  #PBS -l walltime=04:30:00 #PBS -l select=4:ncpus=1:mem=24gb:ngpus=8:gpu_type=RTX6000 #PBS -J 1-27 **(ie trying threading)**
| ```submitObjPlacement-cream.pbs``` | Cream | "../Data/CreamInterior" |  #PBS -l walltime=121:30:00 #PBS -l select=1:ncpus=1:mem=24gb:ngpus=1:gpu_type=RTX6000 **(ie trying no threading, 1 gpu, but a really long walltime)**
| ```submitObjPlacement2.pbs``` | Dark        | "../Data2/DarkInterior"|  #PBS -l walltime=16:00:00 #PBS -l select=1:ncpus=64:mem=124gb:ngpus=1:gpu_type=RTX6000:cpu_type=rome #PBS -J 1-27 AND -t 64 **(ie 2nd attempt at multi-threading, trying a longer walltime, multiple cpus and 1 gpu)**
| ```submitObjPlacement2-cream.pbs``` | Cream | "../Data/CreamInterior" |  #PBS -l walltime=121:30:00 #PBS -l select=1:ncpus=1:mem=24gb:ngpus=1:gpu_type=RTX6000 **(ie trying no threading, 1 gpu, but a really long walltime)**
| ```submitObjPlacement-brown.pbs``` | Brown | "../Data/Brown" | [to be decided]

### Notes 
- I think the -t command when running a blender file from the command line refers to the number of CPUs, not GPUs???
- 1 thread for 16 hours gets 2.5 objects fully rendered (2nd attempt at cream interior)
- select=4:ncpus=1:mem=24gb:ngpus=8 and 1 threads for 4.5 hours gets you around 9 renders for every object (1st attempt at threading). BUT you have to wait around a week for the program to be queued. Not this job quit because I set it to 32 threads thinking this equated to the number of gpus (but it must be no.cpus as it said limit was 1).
- Blender recommends 8-core CPU, 32GB RAM. 
- Scene initialisation and saving the image takes the most ammount of time and uses the CPU not the GPU, therefore, potentially more time can be saved by increasing the number of CPUs rather than the number of GPUs.
- ```submitObjPlacement2.pbs``` **worked very well!!!** This means it was the number of CPUs, not the number of GPUs, that was the limited factor. I wil continue to use this method going forward.
    - Note: Due to job limited sizes, I can only queue one script like this at a time.


## Model building