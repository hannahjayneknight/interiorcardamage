import glob

train_path = '../Data/train'
test_path = '../Data/test'

train_count=len(glob.glob(train_path+'/**/*.png'))
f = open("train_count.txt", "x")
f.write( str(train_count) )
f.close()

test_count=len(glob.glob(test_path+'/**/*.png'))
f = open("test_count.txt", "x")
f.write( str(test_count) )
f.close()