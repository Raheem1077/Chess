"""
This is our main driver file. It will be responsible for handling user input and displaying the current GameState object
"""

import pygame as p
from Chess import ChessEngine

WIDTH = HEIGHT = 512 # 400 is another option
DIMENSION = 8 # dimensions of a chess board are 8x8
SQ_SIZE = HEIGHT//DIMENSION
MAX_FPS = 15 # for animations later on
IMAGES = {}

'''
Initialize a global dictionary of images. This will be called exactly once in the main
'''

def loadImages():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bQ', 'bK']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
    # Note : we can access an image by saying 'IMAGES['wp']'


'''
The main driver for our code. This will handle user input and updating the graphics
'''

def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    loadImages() # only do this once, before the while loop
    running = True
    sqSelected = () # no square is selected, keep track of the last click of the user (tuple: (row, col))
    playerClicks = [] # keep track of player clicks (two tuples: [6, 4], [4, 4])
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() #(x, y) location of mouse
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if sqSelected == (row, col): #the user clicked the same square twice
                    sqSelected = () #deselected
                    playerClicks = [] #clear player clicks
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected) # append for both 1st and 2nd clicks
                if len(playerClicks) == 2: #after the 2nd click
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessNotation())
                    gs.makeMove(move)
                    sqSelected = () #reset user clicks
                    playerClicks = []


        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()
'''
Responsible for all the graphics within a current game state.
'''
def drawGameState(screen, gs):
    drawBoard(screen) #draw squares on the board
    # add in pieces highlighting or move suggestions (later)
    drawPieces(screen, gs.board) # draw pieces on top those squares

'''
Draw the square on the board. The top left square is always light.
'''
def drawBoard(screen):
    colors = [p.Color("white"), (70,165,60)]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c)%2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


'''
Draw the square on the board using the current GameState.board
'''
def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--": # not empty square
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

if __name__ == "__main__":
    main()
    print(IMAGES)