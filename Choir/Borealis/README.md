# What is Borealis?
Borealis is a network designed to automate parallel processing and multi-computer control, running in the background of Windows computers to allow the devices connected to be used as normal while their computing power is used to complete the tasks they are given. Essentially, this computer is currently a _Choir_ device, which will run the commands of the _Conductor_ device when it receives them. 

# Why is this computer connected to the Borealis network?
This computer is connected to the network because a _Choir_ download device was plugged into your computer, connecting it to the network. This may have been by you, a work collegue or a friend who has permission to utilise your computer in order to run an algorithm across multiple computers at one time, which will speed up its execution. This is the intended use of this program and in this case you should not tamper with these files. However, if you have not willingly connected your computer to Borealis and you have not given anyone else permission to do so, a "bad actor" may have control of your device. This means they are illegally using your device for malicious purposes and could have stolen your passwords and even could be spying on you at this very moment. In this case, you will need to remove the software from your computer.

# How do I remove the Choir software?
1. Go into task manager (**Ctrl+Shift+Esc**) and type in "_python_"
  - This should bring up a process called "python" which will have the python logo, which you should close
2. Go into the run dialogue (**Windows+R**) and type in "_shell:startup_" before pressing OK
  - This should bring up the Startup directory (**C:\Users\<Username>\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup**)
3. Next, press _View_, then at the bottom of the dropdown _Show_, then click _Hidden Items_ if it isn't already ticked
  - This should reveal a file named **borealis.lnk**. Delete this.
4. Finally, delete the directory this README.md file is stored in
  - It should be called **C:\Users\Public\Borealis**

If something goes wrong with this process, email me at [*lindenlabsofficial@gmail.com*](lindenlabsofficial@gmail.com) and I will try to respond within 1 buisness day, or search for your specific problem on google.
