username = ACCOUNT()
accountinfo = GET(f"/account?v=0&u={username}").split("\n\n")
if len(accountinfo) > 3:
    commands = accountinfo[3].split("\n")
    bindex = 0
    DISPLAY(commands[bindex])
    while True:
        if B2() == 0:
            break
        elif B1() == 0:
            if bindex < len(commands)-1:
                bindex = bindex + 1
            else:
                bindex = 0
            DISPLAY(commands[bindex])
        elif B0() == 0:
            SEND({"command":commands[bindex].replace(".:",":.")})
        utime.sleep(0.5)
else:
    DISPLAY("Add command presets to account to use this app")
    utime.sleep(5)
