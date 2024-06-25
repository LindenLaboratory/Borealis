#IMPORTS
import os
import glob

#MAINLOOP
directory = input("Enter Directory Path: ")
for file in glob.glob(os.path.join(directory, '*.txt')):
    with open(file, 'r') as f:
        str_ = "n".join([i.replace("\n","") for i in f.readlines()])
        f.close()
    with open(file,"w") as f:
        f.write(str_)
        f.close()
