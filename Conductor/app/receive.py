messages = GET('/log').split("\n")[:-1]
bindex = 0
DISPLAY(messages[bindex])
while True:
    if B2() == 0:
        break
    elif B1() == 0:
        if bindex < len(messages)-1:
            bindex = bindex + 1
        else:
            bindex = 0
        DISPLAY(messages[bindex])
    elif B0() == 0:
        SEND({"log":messages[bindex]})
    utime.sleep(0.5)
