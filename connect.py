#IMPORTS
import select
import sys
import mode as _
import time
#FUNCTIONS
def getparams():
    with open("parameters.txt","w") as f:
        return f.readlines()
def code(num):
    lst = []
    for i in range(num):
        lst.append(input())
    lst.append("params:."+input("params:."))
    return "code:." + "//".join(lst)
def run(cmds):
    comms = cmds
    while True:
        inp = input("/> ")
        if inp == ".esc" or inp == ".exit":
            return False
        elif inp == ".run":
            return cmds
        elif inp == ".del":
            cmds = []
        elif ".code" in inp:
            num = int(inp.split(" ")[-1])
            cmds.append(code(num))
        else:
            cmds.append(inp)