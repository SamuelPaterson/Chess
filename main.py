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
    images["cross"] = pg.transform.scale(pg.image.load("images/cross.png"), (square_size, square_size))
    images["cross"].set_alpha(170)

'''
Class for all my buttons
'''
class Button:
    def __init__(self, screen, x, y, text, button_width, button_height):
        self.screen = screen
        self.box = pg.Rect(x, y, button_width, button_height)
        self.font = pg.font.SysFont("arial.ttf", 21, False, False)
        self.text_display = self.font.render(text, False, pg.Color('Grey'))
        self.text_location = pg.Rect(0, 0, button_width, button_height).move(button_width / 2 - self.text_display.get_width() / 2, button_height / 2 - self.text_display.get_height() / 2)

    def draw(self):
        pg.draw.rect(self.screen, pg.Color("Black"), self.box)
        self.screen.blit(self.text_display, self.text_location)


'''
User input and updating graphics
'''
def main():
    pg.init()
    screen = pg.display.set_mode((width, height))
    pg.display.set_caption("Chess")
    clock = pg.time.Clock()
    load_images()

    gs = GameState()
    legal_moves = gs.all_check_checker()  # List of all legal moves after checking for checks, for every piece.
    piece_moves = []  # List of all legal moves for the selected piece.
    game_over = False
    start_screen = True

    white_button = Button(screen, 0, 0, "White", square_size, square_size)
    reset_button = Button(screen, 0, 0, "Reset", square_size, square_size)

    clicked_square = ()  # Last user click
    clicks = []  # Tracks the past 2 clicks

    run = True
    while run:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                run = False

            if start_screen:
                start_screen = False
            else:
                if not game_over:
                    if e.type == pg.MOUSEBUTTONDOWN:  # Mouse Inputs
                        location = pg.mouse.get_pos()
                        x = int(location[0] // square_size)
                        y = int(location[1] // square_size)
                        if clicked_square == (y, x):  # If same square selected reset
                            clicked_square = ()
                            piece_moves = []
                            clicks = []
                        else:
                            clicked_square = (y, x)
                            clicks.append(clicked_square)
                        if len(clicks) == 1:  # Player selects a piece
                            piece_moves = gs.get_piece_moves(clicked_square,
                                                             legal_moves)  # A list of all legal pos for selected piece
                            if len(piece_moves) == 0:  # AKA No legal moves for that piece
                                clicks = []
                        elif len(clicks) == 2:  # Player makes a move.
                            if clicks in legal_moves:  # Checks if its legal.
                                gs.make_move(clicks)
                                legal_moves = gs.all_check_checker()
                            clicks = []
                            piece_moves = []

                    elif e.type == pg.KEYDOWN:  # Key inputs
                        if e.key == pg.K_LEFT:  # Undo Currently not working
                            gs.undo()
                            legal_moves = gs.all_check_checker()
                    draw_game(screen, gs, piece_moves)
                elif game_over:
                    draw_game(screen, gs, piece_moves)
                    reset_button.draw()

        if gs.check_mate or gs.stale_mate:
            game_over = True
            game_ended(gs.check_mate, gs.whites_turn, screen)

        clock.tick(60)
        pg.display.flip()


'''
All graphics (might want to split up)
'''


def draw_game(screen, gs, piece_moves):
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
            piece = gs.board[y][x]  # Drawing the pieces
            if piece != "..":
                screen.blit(images[piece], (x * square_size, y * square_size))
    for move in piece_moves:
        y = move[1]
        x = move[0]
        screen.blit(images["cross"], (y * square_size, x * square_size))


def game_ended(check_mate, whites_turn, screen):  # Draws post game scenarios
    font = pg.font.SysFont("arial.ttf", 55, False, False)
    if check_mate:
        if whites_turn:
            text = "Checkmate! Black Wins!"
        else:
            text = "Checkmate! White Wins!"
    else:
        text = "Stalemate"
    text_display = font.render(text, False, pg.Color('Grey'))
    text_location = pg.Rect(0, 0, width, height).move(width/2 - text_display.get_width()/2, height/2 - text_display.get_height()/2)
    pg.draw.rect(screen, pg.Color("Black"), pg.Rect(0, 0.375*height, width, 0.25*height))
    screen.blit(text_display, text_location)

if __name__ == "__main__":
    main()
