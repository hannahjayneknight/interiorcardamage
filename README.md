# Interior Car Damage

Note: All blender files and renders (data) is exported to my OneDrive account since pushing them would exceed the GitHub limit and be blocked.

## Data Generation

## Model building
- The "Data" folder contains folders for each object, "dirty", "hairy" and "clear" for the Volvo.
    - "VWUP_Data" conatins the same data for this car.
- The "foreign_vs_clear" folder contains only "foreign-object" and "clear" for the Volvo.
- The "mess_vs_clear" folder contains a "mess" folder (including foreign objects, dirt and hair) a "clear" folder for the Volvo.
    - Do the same but with data from the VW too?


### Notes 
- I think the -t command when running a blender file from the command line refers to the number of CPUs, not GPUs???
- 1 thread for 16 hours gets 2.5 objects fully rendered (2nd attempt at cream interior)
- select=4:ncpus=1:mem=24gb:ngpus=8 and 1 threads for 4.5 hours gets you around 9 renders for every object (1st attempt at threading). BUT you have to wait around a week for the program to be queued. Not this job quit because I set it to 32 threads thinking this equated to the number of gpus (but it must be no.cpus as it said limit was 1).
- Blender recommends 8-core CPU, 32GB RAM. 
- Scene initialisation and saving the image takes the most ammount of time and uses the CPU not the GPU, therefore, potentially more time can be saved by increasing the number of CPUs rather than the number of GPUs.
- ```submitObjPlacement2.pbs``` **worked very well!!!** This means it was the number of CPUs, not the number of GPUs, that was the limited factor. I wil continue to use this method going forward.
    - Note: Due to job limited sizes, I can only queue one script like this at a time.
