#IMPORTS
import os
import glob

#FUNCTIONS
def encrypt(string):
    chartable,newstring = {"a":"14","b":"15","c":"20","d":"21","e":"22","f":"23","g":"24","h":"25","i":"30","j":"31","k":"32","l":"33","m":"34","n":"35","o":"40","p":"41","q":"42","r":"43","s":"44","t":"45","u":"50","v":"51","w":"52","x":"53","y":"54","z":"55","0":"00","1":"01","2":"02","3":"03","4":"04","5":"05","6":"10","7":"11","8":"12","9":"13",":.":":."," ":"  ","|":"n"},""
    for char in string:
        try:
            newstring += chartable[char]
        except:
            newstring += "&" + char
    return newstring

#MAINLOOP
directory = input("Enter Directory Path: ")
for file in glob.glob(os.path.join(directory, '*.txt')):
    with open(file, 'r') as f:
        lst = f.readlines()
        str_ = ""
        for i in lst:
            str_ += i.replace("\n","|")
    with open(file.split(".")[0]+".eos","w") as f:
        f.write(encrypt(str_))
