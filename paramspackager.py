#IMPORTS
import os
import glob

#MAINLOOP
directory = input("Enter Directory Path: ")
for file in glob.glob(os.path.join(directory, '*.txt')):
    with open(file, 'r') as f:
        str = [i.replace("\n","") for i in f.readlines()]
    with open(file.split(".")[0]+".txt","w") as f:
        f.write(str_)
