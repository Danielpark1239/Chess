# import and initalize pygame
from re import X
from turtle import xcor
import pygame
import pygame_menu
from piece import Piece
from board import Board
import moves
from stockfish import Stockfish
pygame.init()

# set up the screen
screen_width = 500
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Chess")

# Main menu
menu = pygame_menu.Menu(
    title = 'Play Chess', 
    width = screen_width, 
    height = screen_height,
    theme = pygame_menu.themes.THEME_DARK
)

menu.add.button('Quit', pygame_menu.events.EXIT)
menu.mainloop(screen)


#640x640 board
#0:180 | 180:260; 260:340; 340:420; 420:500; 500:580; 580:660; 660:740; 
#740:820 | 820:1000 (Square widths)
#0:80 | 80:160; 160:240; 240:320; 320:400; 400:480; 480:560; 560:640;
#640:720 | 720:800 (Square heights)

# Create pygame Rect objects for each square
boardSqWidth = 80
boardSqHeight = 80
boardSqWidths = [80, 160, 240, 320, 400, 480, 560, 640]
boardSqHeights = [80, 160, 240, 320, 400, 480, 560, 640]
boardSqCenters = [120, 200, 280, 360, 440, 520, 600, 680]
lightBlue = (115,151,173,255)
lightGray = (212,224,229,255)

boardSq = []
for i in range(8):
    column = []
    for j in range(8):
        column.append(pygame.Rect(boardSqWidths[i],
        boardSqHeights[j], boardSqWidth, boardSqHeight))
    boardSq.append(column)

# Starting board
chessBoard = Board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

# A list that contains all pieces
boardPieces = pygame.sprite.Group(chessBoard.getPieces())

# determines if the x, y coordinate is in a square of the board.
# Returns the rect of the square, or None if no square can be found.
def squareCollision(x, y):
    for i in range(8):
        for j in range(8):
            if boardSq[i][j].collidepoint(x, y):
                return boardSq[i][j]
    return None

# determines if the x, coordinate is in a square of the board.
# Returns the indexes of the square. Else returns None.
def squareIndex(x, y):
    for i in range(8):
        for j in range(8):
            if boardSq[i][j].collidepoint(x, y):
                return [i, j]
    return None


running = True
heldPiece = None
heldPieceX = 0
heldPieceY = 0
heldPieceGroup = None
while running:
    for event in pygame.event.get():
        # while testing: if you press a key, the program quits
        if event.type == pygame.KEYDOWN:
            running = False
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mousePos = pygame.mouse.get_pos()
            mousePosX = mousePos[0]
            mousePosY = mousePos[1]

            if heldPiece == None:
                # iterate through each piece and check if the mouse
                # cursor intersects its rect
                currentSprites = boardPieces.sprites()
                for i in range(len(currentSprites)):
                    if (currentSprites[i].rect.collidepoint(
                    mousePosX, mousePosY)):
                        heldPiece = currentSprites[i]
                        heldPieceGroup = pygame.sprite.GroupSingle(heldPiece)
                        boardPieces.remove(currentSprites[i])

                # store the coords of the held piece
                heldPieceIndices = squareIndex(mousePosX, mousePosY)
                heldPieceX = heldPieceIndices[0]
                heldPieceY = heldPieceIndices[1]

            # if you're holding a piece, play a move if possible    
            else:
                # highlight the possible moves of the held piece
                #legalMoves = moves.listLegalMoves(heldPieceX, 
                #heldPieceY, chessBoard)
                #
                # TO-DO

                # if you try to make a move when it isn't your turn, 
                # return the piece to its original place 
                if chessBoard.squares[heldPieceX][heldPieceY].getColor()\
                != chessBoard.getTurn():
                    heldPiece.updateRect(boardSqWidths[heldPieceX] + 40, 
                    boardSqHeights[heldPieceY] + 40)
                    boardPieces.add(heldPiece)
                    heldPiece = None
                    heldPieceGroup = None
                    break
                    

                squareRect = squareCollision(mousePosX, mousePosY)
                if squareRect != None:
                    # get x and y indexes of the destination square
                    indices = squareIndex(mousePosX, mousePosY)
                    destX = indices[0]
                    destY = indices[1]

                    # if the move is legal, make the move and update
                    # the board
                    if moves.isMoveLegal(heldPieceX, heldPieceY, 
                    destX, destY, chessBoard) == True:
                        # update board and pieces
                        temp = chessBoard.squares[heldPieceX][heldPieceY]
                        chessBoard.squares[heldPieceX][heldPieceY] = " "
                        chessBoard.squares[destX][destY] = temp
                        chessBoard.squares[destX][destY].updateCoords(destX, destY)
                            
                        # update pygame sprites and groups
                        currentSprites = boardPieces.sprites()

                        for i in range(len(currentSprites)):
                            if pygame.sprite.collide_rect(
                            currentSprites[i], heldPiece):
                                currentSprites[i].image = None
                                currentSprites[i].rect = None
                                currentSprites[i].kill()

                        heldPiece.updateRect(squareRect.left + 40, 
                        squareRect.top + 40)
                        boardPieces.add(heldPiece)
                        heldPiece = None
                        heldPieceGroup = None

                        # increment board variables
                        if chessBoard.getTurn() == "w":
                            chessBoard.turn = "b"
                        else:
                            chessBoard.turn = "w"
                        
                        chessBoard.fullMoves += 1

        if event.type == pygame.MOUSEMOTION:
            if heldPiece != None:
                (x, y) = pygame.mouse.get_pos()
                if ((x > 80 and x < 720) and (y > 80 and y < 720)):
                    heldPiece.updateRect(x, y)


    # Clear old background
    screen.fill((32, 32, 32))
    for i in range(8):
        for j in range(8):
            if i % 2 == j % 2:
                pygame.draw.rect(screen, lightGray, boardSq[i][j])
            else:
                pygame.draw.rect(screen, lightBlue, boardSq[i][j])

    # Draw all pieces
    boardPieces.draw(screen)
    if heldPieceGroup != None:
        heldPieceGroup.draw(screen)

    # Update positions of pieces
    boardPieces.update()
    if heldPiece != None:
        heldPieceGroup.update() 
    
    # Refresh screen
    pygame.display.flip()

pygame.quit()

# to-do:

# if you pick up a piece and it has no legal moves, click anywhere and 
# put it back in its original place

# if you pick up a piece and try to make an illegal move, put it back 
# as well

# if you pick up a piece and you don't want to move it, make sure you
# can put it back on its original square


# add the ability to play as black or white
# add the ability to highlight squares and work on gui
    # work on checks, en passant, checkmate etc
# implement stockfish for the computer, and add a feature to set its 
# difficulty level at the beginning
# implement a time system, a resign button and a draw button

