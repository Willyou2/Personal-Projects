# Name = William Cen
# 
# Partners = leq, dgajaraw

# Updated Animation Starter Code

from tkinter import *
from random import *
import copy

####################################
# customize these functions
####################################

def init(data):
    data.sPiece = [
        [ False,  True,  True ],
        [  True,  True, False ]
    ]
    data.rows = 15
    data.cols = 10
    data.cellSize = 20
    data.margin = 25
    data.board = []
    data.emptyColor = "blue"
    a = []
    for i in range(data.rows):
        a = []
        for j in range(data.cols):
            a.append(data.emptyColor)
        data.board.append(a)
    data.original = copy.deepcopy(data.board)
    # pre-load a few cells with known colors for testing purposes
    #data.board[0][0] = "red" # top-left is red
    #data.board[0][data.cols-1] = "white" # top-right is white
    #data.board[data.rows-1][0] = "green" # bottom-left is green
    #data.board[data.rows-1][data.cols-1] = "gray" # bottom-right is gray
    data.boxWidth = 5
    #print(data.board)

    # Seven "standard" pieces (tetrominoes)

    iPiece = [
        [  True,  True,  True,  True ]
    ]

    jPiece = [
        [  True, False, False ],
        [  True,  True,  True ]
    ]

    lPiece = [
        [ False, False,  True ],
        [  True,  True,  True ]
    ]

    oPiece = [
        [  True,  True ],
        [  True,  True ]
    ]

    sPiece = [
        [ False,  True,  True ],
        [  True,  True, False ]
    ]

    tPiece = [
        [ False,  True, False ],
        [  True,  True,  True ]
    ]

    zPiece = [
        [  True,  True, False ],
        [ False,  True,  True ]
    ]
    data.tetrisPieces = [ iPiece, jPiece, lPiece, oPiece, sPiece, tPiece, zPiece ]

    data.tetrisPieceColors = [ "red", "yellow", "magenta", "pink", "cyan", "green", "orange" ]
    data.fallingPiece = data.tetrisPieces[0]
    data.fallingPieceColor = data.tetrisPieceColors[0]
    newFallingPiece(data)
    data.fallingPieceRow = 0
    data.fallingPieceCol = data.cols//2 - len(data.fallingPiece[0])//2
    data.gameDone = False #if done, then the game stops running until "r" is pressed
    data.score = 0
    data.paused = False
    
def newFallingPiece(data): #selects a random piece from the list of pieces 
    #Sets random piece and gives its particular color
    randomIndex = randint(0, len(data.tetrisPieces) - 1)
    data.fallingPiece = data.tetrisPieces[randomIndex] 
    data.fallingPieceColor = data.tetrisPieceColors[randomIndex] 
    #Sets starting point for new piece
    data.fallingPieceRow = 0
    data.fallingPieceCol = data.cols//2 - len(data.fallingPiece[0])//2
    

def drawFallingPiece(canvas, data):
    #Draws out the piece by reading the truth value at the indexed location
    for i in range(len(data.fallingPiece)):
        for j in range(len(data.fallingPiece[0])):
            if data.fallingPiece[i][j] == True:
                row = i + data.fallingPieceRow
                col = j + data.fallingPieceCol
                #draws cell with corresponding color
                drawCell(canvas, data, row, col, data.fallingPieceColor) 


def fallingPieceIsLegal(data, row, col):
    #Checks if the piece is in still in the board and not overlapping a piece
    for i in range(len(data.fallingPiece)):
        for j in range(len(data.fallingPiece[0])):
            if data.fallingPiece[i][j] == True and \
            (not 0 <= row or \
            not 0 <= col or \
            not row + len(data.fallingPiece) <= 15 or \
            not col + len(data.fallingPiece[0]) <= 10 or \
            not data.board[row+i][col + j] == data.emptyColor):
                return False
    return True

def rotateFallingPiece(data):
    #Finds new center to place the new piece at
    oldNumRows = len(data.fallingPiece)
    oldNumCols = len(data.fallingPiece[0])
    oldCenterRow = data.fallingPieceRow + oldNumRows//2
    oldCenterCol = data.fallingPieceCol + oldNumCols//2
    newRow = oldCenterRow - len(data.fallingPiece[0])//2
    newCol = oldCenterCol - len(data.fallingPiece)//2
    #oldpiece used to reset the piece if the rotation is illegal
    oldPiece = copy.deepcopy(data.fallingPiece)
    a = []
    for col in range(len(data.fallingPiece[0])):#Rotates Clockwise
        a.append([data.fallingPiece[i][col] \
            for i in range(len(data.fallingPiece)-1,-1,-1)])
    #print(data.fallingPieceRow)
    data.fallingPiece = a
    #Changes the values for the placement of the rotated block if rotation valid
    if fallingPieceIsLegal(data, newRow, newCol):
        data.fallingPieceRow = newRow
        data.fallingPieceCol = newCol
    else:
        data.fallingPiece = oldPiece
    #print(newRow)
    #print(data.fallingPiece)


def moveFallingPiece(data, drow, dcol):
    #print(data.fallingPieceRow + drow, data.fallingPieceCol + dcol)
    #Adds change in row and column to the position if the movement is legal
    if fallingPieceIsLegal(data, data.fallingPieceRow + drow, \
        data.fallingPieceCol + dcol):
        data.fallingPieceRow += drow
        data.fallingPieceCol += dcol

def removeFullRows(data): #Removes a row if it is filled
    isFull = False
    fullRows = []
    newBoard = copy.deepcopy(data.original)
    scoreCount = 0
    for row in range(len(data.board)):
        isFull = True #Sets a truth value to test if the row is filled
        for col in range(len(data.board[0])):
            if data.board[row][col] == data.emptyColor:
                isFull = False
        if isFull:
            #appends list of indexes of filled rows
            fullRows.append(row)
    if len(fullRows) > 0:
        #Recreates the board by adding in every nonfilled row to a blank board
        #Removes a blank row for every add in
        for row in range(len(data.board)):
            if fullRows.count(row) != 0:
                scoreCount += 1
                continue
            newBoard.append(data.board[row])
            newBoard.pop(0)
        data.board = copy.deepcopy(newBoard)
        data.score += scoreCount**2


def gameRestart(data): #Restarts the game if called
    data.board = copy.deepcopy(data.original)
    newFallingPiece(data)
    data.gameDone = False

def keyPressed(event, data):

    if data.gameDone:
        if event.char == "r":
            gameRestart(data)
        else:
            return None
    if event.char == "p": #pauses game
        data.paused = not data.paused            
    if data.paused:
        return None            
    if event.keysym == "Down":
        moveFallingPiece(data, 1, 0)
    elif event.keysym == "Right":
        moveFallingPiece(data, 0, 1)
    elif event.keysym == "Left":
        moveFallingPiece(data, 0, -1)
    elif event.keysym == "Up": #rotates piece
        rotateFallingPiece(data)

def placeFallingPiece(data):
    #When called, it will add the piece to the board and check if a row is filled
    for i in range(len(data.fallingPiece)):
        for j in range(len(data.fallingPiece[0])):
            if data.fallingPiece[i][j]:
                data.board[i+data.fallingPieceRow][j+data.fallingPieceCol] \
                = data.fallingPieceColor
    removeFullRows(data)

def timerFired(data):
    if data.paused:
        return None
    rowBefore = data.fallingPieceRow 
    if data.gameDone:
        return None
    moveFallingPiece(data, +1, 0)
    #if no change in position, then create a new piece and place the old in the board
    if data.fallingPieceRow == rowBefore: 
        placeFallingPiece(data)
        newFallingPiece(data)
    #Checks if the newly created piece is allowed or not. If initial is impossible, then game is done
    if not fallingPieceIsLegal(data, data.fallingPieceRow, data.fallingPieceCol):
        data.gameDone = True

def drawBoard(canvas, data): #Draws board
    for row in range(data.rows):
        for col in range(data.cols):
            drawCell(canvas, data, row, col, data.board[row][col])

def drawCell(canvas, data, cellRow, cellCol, color):
    #using the row and column indices, finds coordinates for drawing
    #Draws given cell
    x0, y0 = data.margin + cellCol*data.cellSize, \
    data.margin + cellRow*data.cellSize
    x1, y1 = x0 + data.cellSize, y0 + data.cellSize
    canvas.create_rectangle(x0, y0, x1, y1, fill = color, width = data.boxWidth)

def redrawAll(canvas, data):
    #Redraws the board and falling piece
    canvas.create_rectangle(0,0, data.width, data.height, fill = "orange")
    drawBoard(canvas, data)
    drawFallingPiece(canvas, data)
    #Represents score in top center
    canvas.create_text(data.width/2, data.margin/2, text = "Score: " + str(data.score), \
        fill = "blue", font = "Helvetica 12 bold")
    if data.gameDone: #This will create finished logo if game is over
        canvas.create_rectangle(0, data.margin + data.cellSize, data.width, \
            data.margin + data.cellSize*2, fill = "black")
        canvas.create_text(data.width/2, data.margin + 1.5*data.cellSize, text = \
            "Game Over", fill = "yellow", font = "Arial 16")

####################################
# use the run function as-is
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 300 # milliseconds
    root = Tk()
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")


def playTetris(rows = 15, cols = 10):
    #begins tetris board and starts the run sequence
    cellSize = 20
    winMargin = 25
    width = 2*winMargin + cols*cellSize
    height = 2*winMargin + rows*cellSize
    run(width, height)
    
playTetris()