# This module is designed to handle player moves.

# make a board class!!!!!!!

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

class moves:
    def __init__(self, pieceType, board):
        self.pieceType = pieceType
        self.board = board
    
    def legalMoves(self):
        self.board




