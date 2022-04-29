"""
Handles all graphics and user input.
"""
import pygame as pg
from engine import *

# Define board and spaces sizes
width = height = 512
square_size = width / 8

'''
Initialize dictionary of images
'''
images = {}


def load_images():
    pieces = ["bR", "bN", "bB", "bQ", "bK", "bP", "wR", "wN", "wB", "wQ", "wK", "wP"]
    for piece in pieces:
        images[piece] = pg.transform.scale(pg.image.load("images/" + piece + ".png"), (square_size, square_size))


'''
User input and updating graphics
'''


def main():
    pg.init()
    screen = pg.display.set_mode((width, height))
    clock = pg.time.Clock()
    gs = GameState()
    load_images()
    run = True
    clicked_square = ()  # Last user click
    clicks = []  # Tracks the past 2 clicks
    test = []
    start_square = ()
    end_square = ()
    legal_moves = gs.all_check_checker()  # List of all legal moves after checking for checks
    while run == True:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                run = False

            elif e.type == pg.MOUSEBUTTONDOWN:  # Mouse Inputs
                location = pg.mouse.get_pos()
                x = int(location[0] // square_size)
                y = int(location[1] // square_size)
                if clicked_square == (y, x):
                    clicked_square = ()
                    clicks = []
                else:
                    clicked_square = (y, x)
                    clicks.append(clicked_square)
                if len(clicks) == 2:
                    if clicks in legal_moves:
                        gs.make_move(clicks)
                        legal_moves = gs.all_check_checker()
                    clicks = []

            elif e.type == pg.KEYDOWN:  # Key inputs
                if e.key == pg.K_LEFT:  # Undo Currently not working
                    gs.undo()
                    legal_moves = gs.all_check_checker()

        draw_game(screen, gs)
        clock.tick(60)
        pg.display.flip()


'''
All graphics (might want to split up)
'''

def draw_game(screen, gs):
    dark_squares = [47, 130, 255]  # RGB Colour for the dark squares.
    for x in range(8):
        for y in range(8):
            if x % 2 == 0:  # Logic to colour the squares.
                if y % 2 == 0:
                    pg.draw.rect(screen, pg.Color("white"),
                                 pg.Rect(x * square_size, y * square_size, square_size, square_size))
                else:
                    pg.draw.rect(screen, pg.Color(dark_squares),
                                 pg.Rect(x * square_size, y * square_size, square_size, square_size))
            else:
                if y % 2 == 0:
                    pg.draw.rect(screen, pg.Color(dark_squares),
                                 pg.Rect(x * square_size, y * square_size, square_size, square_size))
                else:
                    pg.draw.rect(screen, pg.Color("white"),
                                 pg.Rect(x * square_size, y * square_size, square_size, square_size))
            # Drawing the pieces
            piece = gs.board[y][x]
            if piece != "..":
                screen.blit(images[piece], (x * square_size, y * square_size))


if __name__ == "__main__":
    main()
