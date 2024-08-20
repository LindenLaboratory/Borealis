presets = GET(f"/account?v=0&u={ACCOUNT()}").split("\n\n")[1].split("\n")
bindex = 0
DISPLAY(presets[bindex])
while True:
    if B2() == 0:
        break
    elif B1() == 0:
        if bindex < len(presets)-1:
            bindex = bindex + 1
        else:
            bindex = 0
        DISPLAY(presets[bindex])
    elif B0() == 0:
        SEND({"log":presets[bindex]})
    utime.sleep(0.5)
