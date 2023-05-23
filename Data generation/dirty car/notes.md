**Notes on dirty car TRAIN job**
- By 16 hours, it generated around 1500-1600 images per obj. This is only for the brown car and means around 18 dirty cars.
- I have removed dashboard and rearshelf from shots as I do not have pics of these in my validation dataset and they are less common to get dirty.
- I have reduced n from 9 to 3 so there are fewer renders per shot
- This means a total of 546 images per car (in this car per car colour) as opposed to 2,106.
- This means I should be able to run 3 cars within 16 hours next time. 
- However, given I have enough images for the brown car I'm only re-running it for black and cream.


**Notes on dirty car TEST data**
- I reran for driverseat without changing the counting part of the script, so it started at count 0, overwriting all my previous images!
- This is OK for the testing dataset, but I need to be careful next time.
