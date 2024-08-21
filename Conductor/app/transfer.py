bindex,lst,acc=0,[line.split(":.")[1] for line in GET("/online").split("\n")],ACCOUNT()
for item in lst:
    if acc in item:
        lst.remove(item)
if len(lst)==0:ERROR(419)
DISPLAY(lst[bindex])
while True:
    if B2()==0:break
    elif B1()==0:
        if bindex<len(lst)-1:bindex=bindex+1
        else:bindex=0
        DISPLAY(lst[bindex])
    elif B0()==0:
        target=lst[bindex];break
account,bindex=GET(f"/account?v=0&u={acc}").split("\n\n"),0
money,amounts,presets=account[0],account[2].split("\n"),[]
for amount in amounts:
    if float(amount)<=float(money):presets.append(amount)
if len(presets)==0:ERROR(419)
DISPLAY(presets[bindex])
while True:
    if B2()==0:break
    elif B1()==0:
        if bindex<len(presets)-1:bindex=bindex+1
        else:bindex=0
        DISPLAY(presets[bindex])
    elif B0()==0:
        SEND({"transfer":acc+","+target+","+presets[bindex]});break
    utime.sleep(0.5)
