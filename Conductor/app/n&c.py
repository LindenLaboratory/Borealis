#SETUP
DISPLAY("Controls:\nKEY0 = -> & KEY1 = <-");utime.sleep(1.25)
board = [[".","-","-"],["-","-","-"],["-","-","-"]]
#FUNCTIONS
def convertstr(board: list) -> str:
    return "\n".join([" ".join(lst) for lst in board])
def convertxo(xORo: bool) -> str:
    if xORo: return "x"
    else: return "y"
def clear(board: list) -> list:
    return [['-' if item == '.' else item for item in sublist] for sublist in board]
def evaluate(board):
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != '-':
            return True if board[i][0] == 'x' else False
        if board[0][i] == board[1][i] == board[2][i] != '-':
            return True if board[0][i] == 'x' else False
        if board[0][0] == board[1][1] == board[2][2] != '-':
            return True if board[0][0] == 'x' else False
        if board[0][2] == board[1][1] == board[2][0] != '-':
            return True if board[0][2] == 'x' else False
        if all(item != '-' for row in board for item in row):
            return "Draw"
    return None
#MAINLOOP
DISPLAY(convertstr(board))
x,y,xORo,move=0,0,False,False
char = "."
while True:
    if B2() == 0:
        move = True 
        xORo = not xORo
    elif B1() == 0:
        if y == 2 and x == 2:
            y = 0
            x = 0
        elif x == 2:
            x=0
            y+=1
        else:
            x+=1
    elif B0() == 0:
        if x == 0:
            if y == 0 and x == 0:
                y = 2
                x = 2
            elif y > 0:
                x=2
                y-=1
        else:
            x-=1

    board = clear(board)
    print(board)
    square = board[y][x]
    if move:
        board[y][x] = convertxo(xORo)
        move = False
    else:
        if square == "x" or square == "y":
            pass
        else:
            board[y][x] = "."
    result = evaluate(board)
    if result == None:
        DISPLAY(convertstr(board))
    elif result == "Draw":
        DISPLAY("Draw.")
        utime.sleep(1.25)
        break
    else:
        DISPLAY(f"Player '{convertxo(xORo)}' Wins!")
        utime.sleep(1.25)
        break
    utime.sleep(0.25)
