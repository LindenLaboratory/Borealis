#IMPORTS
import os
import glob

#MAINLOOP
directory = input("Enter Directory Path: ")
for file in glob.glob(os.path.join(directory, '*.txt')):
    with open(file, 'r') as f:
        lst,str_ = f.readlines(),""
        for i in lst:
            str_ += i.replace("\n","n")
    with open(file.split(".")[0]+".eos","w") as f:
        f.write(str_)
