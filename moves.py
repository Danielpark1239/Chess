# This module is designed to handle player moves.
import piece

# highlight all available moves for the piece:
    # if a piece is blocking the path, cut it short

# have turns: white starts, then black and it alternates:
    # you can only move your color piece on your turn

# implement checks
# implement castling
# implement en passant
# implement checkmate
# implement piece promotion

# implement a clock system in the board module
# also resign and draw buttons

# add sounds
# hook up stockfish and have an AI play against you
# have a setting for starting as black or white
    # when playing as black, rotate the board so the black pieces are 
    # in front of you

# Returns True if the coordinates are within the 8x8 board, False otherwise
def areValidIndices(x, y):
    if (x < 0 or x > 7):
        return False
    if (y < 0 or y > 7):
        return False
    return True

# Returns 0 if the piece can't move to (x2,y2) without being
# blocked by a piece (assuming the dest square is valid)
# Returns 1 if the square is empty
# Returns 2 if an enemy piece can be captured
def isNotBlocked(piece, x2, y2, board) -> int:
    if areValidIndices(x2, y2) == False:
        return 0

    # destination square can't be initial square
    #if (piece.getX() == x2 and piece.getY() == y2):
    #    return 0

    destPiece = board.squares[x2][y2]
    
    if destPiece == " ":
        return 1
    
    if destPiece.getColor() != piece.getColor():
        return 2

    assert(destPiece.getColor() == piece.getColor())
    return 0

# Returns a list of all possible destinations for the piece
# positioned at (x, y)
# doesn't account for king safety, so all moves may not be legal
def listPossibleMoves(x, y, board): 
    assert(areValidIndices(x, y))
    piece = board.squares[x][y]
    legalMoves = []

    # if it isn't the player's turn, return an empty list
    if piece.getColor() != board.getTurn():
        return legalMoves

    result = 0
    match piece.getType():
        # pawn
        case "P":
            if isNotBlocked(piece, x, y-1, board) == 1:
                legalMoves.append([x, y-1])
            if isNotBlocked(piece, x-1, y-1, board) != 0:
                legalMoves.append([x-1, y-1])
            if isNotBlocked(piece, x+1, y-1, board) != 0:
                legalMoves.append([x+1,y-1])

            if piece.canPawnMoveTwo() and isNotBlocked(
            piece, x, y-2, board) == 1:
                legalMoves.append([x, y-2])

        case "p":
            if isNotBlocked(piece, x, y+1, board) == 1:
                legalMoves.append([x, y+1])
            if isNotBlocked(piece, x-1, y+1, board) != 0:
                legalMoves.append([x-1, y+1])
            if isNotBlocked(piece, x+1, y+1, board) != 0:
                legalMoves.append([x+1, y+1])

            if piece.canPawnMoveTwo() and isNotBlocked(
            piece, x, y+2, board) == 1:
                legalMoves.append([x, y+2])
        
        # rook/queen
        case "R"|"r"|"Q"|"q":
            # loop left until blocked
            result = isNotBlocked(piece, x-1, y, board)
            while (result != 0):
                legalMoves.append([x-1, y])
                if result == 2:
                    break
                x = x-1
            result = isNotBlocked(piece, x+1, y, board) #right
            while (result != 0):
                legalMoves.append([x+1, y])
                if result == 2:
                    break
                x = x+1
            result = isNotBlocked(piece, x, y-1, board) #up
            while (result != 0):
                legalMoves.append([x, y-1])
                if result == 2:
                    break
                y = y-1
            result = isNotBlocked(piece, x, y+1, board) #down
            while (result != 0):
                legalMoves.append([x, y+1])
                if result == 2:
                    break
                y = y+1

        # bishop/queen
        case "B"|"b"|"Q"|"q":
            # loop left/up until blocked
            result = isNotBlocked(piece, x-1, y-1, board)
            while (result != 0):
                legalMoves.append([x-1, y-1])
                if result == 2:
                    break
                x = x-1
                y = y-1
            result = isNotBlocked(piece, x+1, y-1, board) # right/up
            while (result != 0):
                legalMoves.append([x+1, y-1])
                if result == 2:
                    break
                x = x+1
                y = y-1
            result = isNotBlocked(piece, x-1, y+1, board) # left/down
            while (result != 0):
                legalMoves.append([x-1, y+1])
                if result == 2:
                    break
                x = x-1
                y = y+1
            result = isNotBlocked(piece, x+1, y+1, board) # right/down
            while (result != 0):
                legalMoves.append([x+1, y+1])
                if result == 2:
                    break
                x = x+1
                y = y+1

        # knight
        case "N"|"n":
            # check all 8 L-shaped paths
            if isNotBlocked(piece, x-1, y-2, board) != 0:
                legalMoves.append([x-1, y-2])
            if isNotBlocked(piece, x+1, y-2, board) != 0:
                legalMoves.append([x+1, y-2])
            if isNotBlocked(piece, x+2, y-1, board) != 0:
                legalMoves.append([x+2, y-1])
            if isNotBlocked(piece, x+2, y+1, board) != 0:
                legalMoves.append([x+2, y+1])
            if isNotBlocked(piece, x+1, y+2, board) != 0:
                legalMoves.append([x+1, y+2])
            if isNotBlocked(piece, x-1, y+2, board) != 0:
                legalMoves.append([x-1, y+2])
            if isNotBlocked(piece, x-2, y+1, board) != 0:
                legalMoves.append([x-2, y+1])
            if isNotBlocked(piece, x-2, y-1, board) != 0:
                legalMoves.append([x-2, y-1])
        # king
        case "K"|"k":
            # check all 8 adjacent squares
            if isNotBlocked(piece, x, y-1, board) != 0:
                legalMoves.append([x, y-1])
            if isNotBlocked(piece, x+1, y-1, board) != 0:
                legalMoves.append([x+1, y-1])
            if isNotBlocked(piece, x+1, y, board) != 0:
                legalMoves.append([x+1, y])
            if isNotBlocked(piece, x+1, y+1, board) != 0:
                legalMoves.append([x+1, y+1])
            if isNotBlocked(piece, x, y+1, board) != 0:
                legalMoves.append([x, y+1])
            if isNotBlocked(piece, x-1, y+1, board) != 0:
                legalMoves.append([x-1, y+1])
            if isNotBlocked(piece, x-1, y, board) != 0:
                legalMoves.append([x-1, y])
            if isNotBlocked(piece, x-1, y-1, board) != 0:
                legalMoves.append([x-1, y-1])        

    return legalMoves

# returns True if moving the piece will cause the king to get attacked,
# False otherwise
def isKingAttacked(piece, board):
    # locate the same-colored king
    pieceColor = piece.getColor()
    kingX = 0
    kingY = 0
    for i in board.getPieces():
        if i.getColor() == pieceColor and (i.getType == "K" or 
        i.getType == "k"):
            kingX = i.getX()
            kingY = i.getY()

    # remove the piece from its square
    pieceX = piece.getX()
    pieceY = piece.getY()
    board.squares[pieceX][pieceY] = " "

    # will the king get attacked?
    # check all possible moves of all enemy pieces
    result = False
    for i in board.getPieces():
        if pieceColor != i.getColor():
            moves = listPossibleMoves(i.getX(), i.getY(), board)
            for j in moves:
                if j == [kingX, kingY]:
                    result = True
                    break

    # replace the piece 
    board.squares[pieceX][pieceY] = piece

    return result

# Returns a list of all legal destinations for the piece
# positioned at (x, y)
def listLegalMoves(x, y, board):
    legalMoves = []

    assert areValidIndices(x,y) == True
    piece = board.squares[x][y]

    if isKingAttacked(piece, board) == True:
        return legalMoves

    return listPossibleMoves(x, y, board)

# given a starting pos (x1, y1) and a destination (x2, y2), determines
# if the move is legal for the current board state
def isMoveLegal(x1, y1, x2, y2, board) -> bool:
    legalMoves = listLegalMoves(x1, y1, board)
    for i in legalMoves:
        if i == [x2, y2]:
            return True
    return False




        




## check which sprite collided (MAY NOT NEED)
                    #currentSprites = boardPieces.sprites()
                    #for i in range(len(currentSprites)):
                    #    if pygame.sprite.collide_rect(
                    #    currentSprites[i], heldPiece):
                    #        # get coords of collided sprite
                    #        spriteX = currentSprites[i].rect.left
                    #        spriteY = currentSprites[i].rect.right
                    #        spriteCoords = squareIndex(spriteX, sprit




