from re import S
from piece import Piece

def FENreader(FENstring) -> list[Piece]:
    squares = []
    files = [0,1,2,3,4,5,6,7]
    for i in range(8):
        squares.append(files)

    # squares is a 2D array of [ranks, [files]]
    counter = 0
    pieces = []
    for i in range(len(FENstring) - 2):
        if counter == 64:
            return pieces

        pieceChar = FENstring[i] # not worried about the full FEN
        match pieceChar:
            case ("r"|"R"|"n"|"N"|"b"|"B"|"k"|"K"|"q"|"Q"|"p"|"P"):
                piece = Piece(counter%8, counter//8, pieceChar)
                pieces.append(piece)
                counter += 1

            case "/":
                assert(counter % 8 == 0)

            case _: #a number
                counter += int(pieceChar)

FENreader("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")




