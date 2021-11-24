TXT = 'train.txt'
f1 = open(TXT,'a')#open file
import os
import glob
from natsort import natsorted

dir_name = './data/IOC/train/'
# Get list of all files in a given directory sorted by name
list_of_files = sorted( filter( lambda x: os.path.isfile(os.path.join(dir_name, x)),
                        os.listdir(dir_name) ) )
# Iterate over sorted list of files and print the file paths 
# one by one.
for file_path in list_of_files:
     if file_path.endswith(".jpg"):
        f1.write('data/IOC/train/{}'.format(file_path))
        f1.write("\n")
f1.close()#close file 



TXT = 'test.txt'
f1 = open(TXT,'a')#open file
data_listdir = os.listdir("./data/IOC//test/")
data_listdir.sort(key = lambda x: int(x[:-4]))
for file in data_listdir:
    if file.endswith(".png"):
        print()
        f1.write('data/IOC/test/{}'.format(file))
        f1.write("\n")
f1.close()#close file