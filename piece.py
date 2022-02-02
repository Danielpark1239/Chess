import pygame

boardSqCenters = [120, 200, 280, 360, 440, 520, 600, 680]
screen_width = 1000
screen_length = 800

# Set up piece images
pygame.init()
pygame.display.set_mode((screen_width, screen_length))
WR = pygame.image.load("BoardWR.png").convert_alpha()
WR = pygame.transform.smoothscale(WR, (54, 59))
BR = pygame.image.load("BoardBR.png").convert_alpha()
BR = pygame.transform.smoothscale(BR, (54, 59))
WN = pygame.image.load("BoardWN.png").convert_alpha()
WN = pygame.transform.smoothscale(WN, (55, 60))
BN = pygame.image.load("BoardBN.png").convert_alpha()
BN = pygame.transform.smoothscale(BN, (55, 60))
WB = pygame.image.load("BoardWB.png").convert_alpha()
WB = pygame.transform.smoothscale(WB, (60, 60))
BB = pygame.image.load("BoardBB.png").convert_alpha()
BB = pygame.transform.smoothscale(BB, (60, 60))
WQ= pygame.image.load("BoardWQ.png").convert_alpha()
WQ = pygame.transform.smoothscale(WQ, (60, 58))
BQ = pygame.image.load("BoardBQ.png").convert_alpha()
BQ = pygame.transform.smoothscale(BQ, (60, 58))
WK = pygame.image.load("BoardWK.png").convert_alpha()
WK = pygame.transform.smoothscale(WK, (60, 60))
BK = pygame.image.load("BoardBK.png").convert_alpha()
BK = pygame.transform.smoothscale(BK, (60, 60))
WP = pygame.image.load("BoardWP.png").convert_alpha()
WP = pygame.transform.smoothscale(WP, (45,60))
BP = pygame.image.load("BoardBP.png").convert_alpha()
BP = pygame.transform.smoothscale(BP, (45,60))

# Define piece class
class Piece(pygame.sprite.Sprite):
    # This class represents a piece, derived from the Sprite class in pygame
    # the pieces have type R, N, B, K, Q, P, uppercase if white and 
    # lowercase for black
    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def updateRect(self, x, y):
        self.rect = pygame.Rect((x-self.image.get_width()/2, y-self.image.get_height()/2), 
        (self.image.get_width(),self.image.get_height()))

    # returns a boolean, True if the piece is white and False for black
    def isWhite(piece):
        return piece.type.isupper()
    
    def getType(piece):
        return piece.type

    def __init__(self, x, y, type):
        pygame.sprite.Sprite.__init__(self)
        self.type = type
        self.x = x
        self.y = y

        match type:
            case "P":
                self.image = WP
            case "R":
                self.image = WR
            case "N":
                self.image = WN
            case "B":
                self.image = WB
            case "Q":
                self.image = WQ
            case "K":
                self.image = WK
            case "p":
                self.image = BP
            case "r":
                self.image = BR
            case "n":
                self.image = BN
            case "b":
                self.image = BB
            case "q":
                self.image = BQ
            case "k":
                self.image = BK

        self.rect = pygame.Rect(boardSqCenters[x]-self.image.get_width()/2, boardSqCenters[y]-self.image.get_height()/2, self.image.get_width(),self.image.get_height())
    