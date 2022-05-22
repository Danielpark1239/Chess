from pydoc import importfile
from piece import Piece
from FENreader import FENreader

# inherited from FENreader class
# see FENreader.py for instance variables and methods
class Board(FENreader):

    # executes the given move if it's legal, changing the board state
    # if move isn't legal, does nothing
    #def move(self, xFrom, yFrom, xDest, yDest):
    #    piece = self.squares[xFrom, yFrom]
#
    #    if moves.validateMove(xFrom, yFrom, xDest, yDest) == True:
    #        # update piece locations and board state
    #        continue

    # prints out the current board state
    def __str__(self):
        string = ""
        for j in range(8):
            for i in range(8):
                if (self.squares[i][j] != " "):
                    string += ("[%s]" % self.squares[i][j].type)
                else:
                    string += "[ ]"
            string += ("\n")
        return string
    
    # Returns a list of all the pieces on the board
    def getPieces(self):
        pieces = []
        for i in range(8):
            for j in range(8):
                if self.squares[i][j] != " ":
                    pieces.append(self.squares[i][j])
        return pieces

    

    def __init__(self, FENstring):
        FENreader.__init__(self, FENstring)

        # a 2D array; keeps track of where the pieces are on the board
        squares = [[" " for i in range(8)] for j in range(8)]
        for piece in self.pieces: 
            x = piece.getX()
            y = piece.getY()
            squares[x][y] = piece
        self.squares = squares

    # if the move is legal, move the piece to the destination square.
    # def move(self, piece, destSquare):



    

