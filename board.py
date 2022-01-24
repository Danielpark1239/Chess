# import and initalize pygame
from re import X
from turtle import xcor
import pygame
from FENreader import FENreader
pygame.init()

# set up the screen
screen_width = 1000
screen_length = 800
screen = pygame.display.set_mode((screen_width, screen_length))


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

# Starting position
pieces = FENreader("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

# A list that contains all pieces
boardPieces = pygame.sprite.Group(pieces)

# determines if the x, y coordinate is in a square of the board.
# Returns the rect of the square, or None if no square can be found.
def squareCollision(x, y):
    for i in range(8):
        for j in range(8):
            if boardSq[i][j].collidepoint(x, y):
                return boardSq[i][j]
    return None

running = True
heldPiece = None
heldPieceGroup = None
while running:
    # add the concept of turns and captures
    # you can only hold pieces of your color on your turn
    # if you capture or move a piece, your turn ends

    for event in pygame.event.get():
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
            # if you're holding a piece, drop it on a square
            # delete the sprite of the previous piece           
            else:
                squareRect = squareCollision(mousePosX, mousePosY)
                if squareRect != None:
                    heldPiece.updateRect(squareRect.left + 40, 
                    squareRect.top + 40)

                    # add sprite collision
                    # check which sprite collided
                    currentSprites = boardPieces.sprites()
                    for i in range(len(currentSprites)):
                        if pygame.sprite.collide_rect(
                        currentSprites[i], heldPiece):
                            currentSprites[i].image = None
                            currentSprites[i].rect = None
                            currentSprites[i].kill()

                    boardPieces.add(heldPiece)

                    #collidedSprite = pygame.sprite.spritecollide(
                    #heldPiece, boardPieces, False)[0]
                    #if collidedSprite != heldPiece:
                    #    collidedSprite.kill()
                    #    collidedSprite.image = None
                    #    collidedSprite.rect = None

                    heldPiece = None
                    heldPieceGroup = None

                    # sprite collision is a bit wonky right now!
                    # sometimes collision is not detected so the
                    # pieces can overlap

                    # make everything more standardized:
                        # if you click on a square, 

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
# create the board and pieces in the starting position
# add the ability to play as black or white
# add the ability to move pieces, highlight squares and work on gui
    # work on legal moves and checks, en passant, checkmate etc
# implement stockfish for the computer, and add a feature to set its 
# difficulty level at the beginning
# implement a time system, a resign button and a draw button


