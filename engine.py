"""
Storing all information about the current state.
And determining legal moves.

Can still castle THROUGH check
Need to add en passent
"""


class GameState():
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["..", "..", "..", "..", "..", "..", "..", ".."],
            ["..", "..", "..", "..", "..", "..", "..", ".."],
            ["..", "..", "..", "..", "..", "..", "..", ".."],
            ["..", "..", "..", "..", "..", "..", "..", ".."],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.whites_turn = True  # If false then its blacks turn
        self.last_move = ()  # Used for Undo. Will eventually be a move log
        self.history = []  # Eventually changing this into full move log so can undo multiple moves.
        self.check_mate = False
        self.stale_mate = False

        self.start_row = ()  # All to do with user inputs
        self.start_col = ()
        self.end_row = ()
        self.end_col = ()
        self.moved_piece = ()
        self.captured_piece = ()

        self.rook00_moved = 0  # Keep track how many times any rook has moved. 00 = top left, 77 = bottom right
        self.rook07_moved = 0
        self.rook70_moved = 0
        self.rook77_moved = 0
        self.w_king_moved = 0  # Keep track how many times either king has moved.
        self.b_king_moved = 0

        self.w_king = (7, 4)  # Kings initial positions
        self.b_king = (0, 4)

    def make_move(self, clicks):  # Handles the movement of all the pieces, and specifies how castling works
        self.start_row = int(clicks[0][0])
        self.start_col = int(clicks[0][1])
        self.end_row = int(clicks[1][0])
        self.end_col = int(clicks[1][1])
        self.moved_piece = self.board[self.start_row][self.start_col]
        self.captured_piece = self.board[self.end_row][self.end_col]
        self.board[self.start_row][self.start_col] = ".."
        if self.moved_piece == "wP" and self.end_row == 0:
            self.board[self.end_row][self.end_col] = "wQ"
        elif self.moved_piece == "bP" and self.end_row == 7:
            self.board[self.end_row][self.end_col] = "bQ"
        else:
            self.board[self.end_row][self.end_col] = self.moved_piece

        self.whites_turn = not self.whites_turn

        if self.moved_piece == "wK":  # Updating the kings position and if castling it moves the rook.
            self.w_king = (self.end_row, self.end_col)
            self.w_king_moved = self.w_king_moved + 1
            if self.end_col - self.start_col == 2:
                self.board[7][7] = ".."
                self.board[7][5] = "wR"
                self.rook77_moved = self.rook77_moved + 1
            if self.end_col - self.start_col == -2:
                self.board[7][0] = ".."
                self.board[7][3] = "wR"
                self.rook70_moved = self.rook70_moved + 1
        if self.moved_piece == "bK":
            self.b_king = (self.end_row, self.end_col)
            self.b_king_moved = self.b_king_moved + 1
            if self.end_col - self.start_col == 2:
                self.board[0][7] = ".."
                self.board[0][5] = "bR"
                self.rook07_moved = self.rook07_moved + 1
            if self.end_col - self.start_col == -2:
                self.board[0][0] = ".."
                self.board[0][3] = "bR"
                self.rook00_moved = self.rook00_moved + 1

        if self.start_row == 0:
            if self.start_col == 0:
                self.rook00_moved = self.rook00_moved + 1
            elif self.start_col == 7:
                self.rook07_moved = self.rook07_moved + 1
        if self.start_row == 7:
            if self.start_col == 0:
                self.rook70_moved = self.rook70_moved + 1
            elif self.start_col == 7:
                self.rook77_moved = self.rook77_moved + 1

        self.last_move = ()
        self.history.append(clicks)  # Append with moves

    def undo(self):
        if len(self.history) != 0:
            self.last_move = self.history.pop()
            self.board[self.start_row][self.start_col] = self.moved_piece
            self.board[self.end_row][self.end_col] = self.captured_piece
            self.whites_turn = not self.whites_turn

            if self.moved_piece == "wK":  # Updating kings position and undoing castling.
                self.w_king = (self.start_row, self.start_col)
                self.w_king_moved = self.w_king_moved - 1
                if self.end_col - self.start_col == 2:
                    self.board[7][7] = "wR"
                    self.board[7][5] = ".."
                    self.rook77_moved = self.rook77_moved - 1
                if self.end_col - self.start_col == -2:
                    self.board[7][0] = "wR"
                    self.board[7][3] = ".."
                    self.rook70_moved = self.rook70_moved - 1
            if self.moved_piece == "bK":
                self.b_king = (self.start_row, self.start_col)
                self.b_king_moved = self.b_king_moved - 1
                if self.end_col - self.start_col == 2:
                    self.board[0][7] = "bR"
                    self.board[0][5] = ".."
                    self.rook07_moved = self.rook07_moved - 1
                if self.end_col - self.start_col == -2:
                    self.board[0][0] = "bR"
                    self.board[0][3] = ".."
                    self.rook00_moved = self.rook00_moved - 1

            if self.start_row == 0:
                if self.start_col == 0:
                    self.rook00_moved = self.rook00_moved - 1
                elif self.start_col == 7:
                    self.rook07_moved = self.rook07_moved - 1
            if self.start_row == 7:
                if self.start_col == 0:
                    self.rook70_moved = self.rook70_moved - 1
                elif self.start_col == 7:
                    self.rook77_moved = self.rook77_moved - 1

    '''For every possible moves (apart from castling) check if it is valid by: Making the move, then generate all 
    possible responses, then seeing if those responses take the king. '''

    def get_all_moves(self):  # Generate a list of all possible moves for each piece.
        moves = []  # In the format [ [(StartY, StartX), (EndY, EndX)], ...]
        for y in range(8):  # Goes through each position and if it's a piece then call relevant function.
            for x in range(8):
                piece_colour = self.board[y][x][0]
                piece_type = self.board[y][x][1]
                if (piece_colour == "w" and self.whites_turn) or (piece_colour == "b" and not self.whites_turn):
                    if piece_type == "R":
                        self.get_rook_moves(y, x, moves)
                    elif piece_type == "N":
                        self.get_knight_moves(y, x, moves)
                    elif piece_type == "B":
                        self.get_bishop_moves(y, x, moves)
                    elif piece_type == "Q":
                        self.get_queen_moves(y, x, moves)
                    elif piece_type == "K":
                        self.get_king_moves(y, x, moves)
                    elif piece_type == "P":
                        self.get_pawn_moves(y, x, moves)
        return moves

    def get_rook_moves(self, y, x, moves):
        for k in range(-7, 8):
            if k > 0:
                if 0 <= y + k <= 7:
                    for i in range(1, k + 1):
                        if self.board[y + i][x] == "..":
                            moves.append([(y, x), (y + i, x)])
                            if (0 <= y + i + 1 <= 7) and (
                                    (self.whites_turn == True and self.board[y + i + 1][x][0] == "b") or (
                                    self.whites_turn == False and self.board[y + i + 1][x][0] == "w")):
                                moves.append([(y, x), (y + i + 1, x)])
                                break
                        elif (self.whites_turn == True and self.board[y + i][x][0] == "b") or (
                                self.whites_turn == False and self.board[y + i][x][0] == "w"):
                            moves.append([(y, x), (y + i, x)])
                            break
                        else:
                            break
                if 0 <= x + k <= 7:
                    for i in range(1, k + 1):
                        if self.board[y][x + i] == "..":
                            moves.append([(y, x), (y, x + i)])
                            if (0 <= x + i + 1 <= 7) and (
                                    (self.whites_turn == True and self.board[y][x + i + 1][0] == "b") or (
                                    self.whites_turn == False and self.board[y][x + i + 1][0] == "w")):
                                moves.append([(y, x), (y, x + i + 1)])
                                break
                        elif (self.whites_turn == True and self.board[y][x + i][0] == "b") or (
                                self.whites_turn == False and self.board[y][x + i][0] == "w"):
                            moves.append([(y, x), (y, x + i)])
                            break
                        else:
                            break
            if k < 0:
                if 0 <= y + k <= 7:
                    for i in range(-1, k - 1, -1):
                        if self.board[y + i][x] == "..":
                            moves.append([(y, x), (y + i, x)])
                            if (0 <= y + i - 1 <= 7) and (
                                    (self.whites_turn == True and self.board[y + i - 1][x][0] == "b") or (
                                    self.whites_turn == False and self.board[y + i - 1][x][0] == "w")):
                                moves.append([(y, x), (y + i - 1, x)])
                                break
                        elif (self.whites_turn == True and self.board[y + i][x][0] == "b") or (
                                self.whites_turn == False and self.board[y + i][x][0] == "w"):
                            moves.append([(y, x), (y + i, x)])
                            break
                        else:
                            break
                if 0 <= x + k <= 7:
                    for i in range(-1, k - 1, -1):
                        if self.board[y][x + i] == "..":
                            moves.append([(y, x), (y, x + i)])
                            if (0 <= x + i - 1 <= 7) and (
                                    (self.whites_turn == True and self.board[y][x + i - 1][0] == "b") or (
                                    self.whites_turn == False and self.board[y][x + i - 1][0] == "w")):
                                moves.append([(y, x), (y, x + i - 1)])
                                break
                        elif (self.whites_turn == True and self.board[y][x + i][0] == "b") or (
                                self.whites_turn == False and self.board[y][x + i][0] == "w"):
                            moves.append([(y, x), (y, x + i)])
                            break
                        else:
                            break

    def get_knight_moves(self, y, x, moves):
        for r in [-2, -1, 1, 2]:
            if abs(r) == 2:
                c = 1
            elif abs(r) == 1:
                c = 2
            if 0 <= y + r <= 7 and 0 <= x + c <= 7:
                if (self.board[y + r][x + c] == "..") or (
                        self.whites_turn == True and self.board[y + r][x + c][0] == "b") or (
                        self.whites_turn == False and self.board[y + r][x + c][0] == "w"):
                    moves.append([(y, x), (y + r, x + c)])
            if 0 <= y + r <= 7 and 0 <= x - c <= 7:
                if (self.board[y + r][x - c] == "..") or (
                        self.whites_turn == True and self.board[y + r][x - c][0] == "b") or (
                        self.whites_turn == False and self.board[y + r][x - c][0] == "w"):
                    moves.append([(y, x), (y + r, x - c)])

    def get_bishop_moves(self, y, x, moves):
        for k in range(-7, 8):
            if 0 <= y + k <= 7 and 0 <= x + k <= 7:
                if k > 0:
                    for i in range(1, k + 1):
                        if self.board[y + i][x + i] == "..":
                            moves.append([(y, x), (y + i, x + i)])
                            if (0 <= x + i + 1 <= 7) and (0 <= y + i + 1 <= 7):
                                if (self.whites_turn == True and self.board[y + i + 1][x + i + 1][0] == "b") or (
                                        self.whites_turn == False and self.board[y + i + 1][x + i + 1][0] == "w"):
                                    moves.append([(y, x), (y + i + 1, x + i + 1)])
                                    break
                        if (self.whites_turn == True and self.board[y + i][x + i][0] == "b") or (
                                self.whites_turn == False and self.board[y + i][x + i][0] == "w"):
                            moves.append([(y, x), (y + i, x + i)])
                            break
                if k < 0:
                    for i in range(-1, k - 1, -1):
                        if self.board[y + i][x + i] == "..":
                            moves.append([(y, x), (y + i, x + i)])
                            if (0 <= x + i - 1 <= 7) and (0 <= y + i - 1 <= 7):
                                if (self.whites_turn == True and self.board[y + i - 1][x + i - 1][0] == "b") or (
                                        self.whites_turn == False and self.board[y + i - 1][x + i - 1][0] == "w"):
                                    moves.append([(y, x), (y + i - 1, x + i - 1)])
                                    break
                        if (self.whites_turn == True and self.board[y + i][x + i][0] == "b") or (
                                self.whites_turn == False and self.board[y + i][x + i][0] == "w"):
                            moves.append([(y, x), (y + i, x + i)])
                            break
            if 0 <= y + k <= 7 and 0 <= x - k <= 7:
                if k > 0:
                    for i in range(1, k + 1):
                        if self.board[y + i][x - i] == "..":
                            moves.append([(y, x), (y + i, x - i)])
                            if (0 <= x - i - 1 <= 7) and (0 <= y + i + 1 <= 7):
                                if (self.whites_turn == True and self.board[y + i + 1][x - i - 1][0] == "b") or (
                                        self.whites_turn == False and self.board[y + i + 1][x - i - 1][0] == "w"):
                                    moves.append([(y, x), (y + i + 1, x - i - 1)])
                                    break
                        if (self.whites_turn == True and self.board[y + i][x - i][0] == "b") or (
                                self.whites_turn == False and self.board[y + i][x - i][0] == "w"):
                            moves.append([(y, x), (y + i, x - i)])
                            break
                if k < 0:
                    for i in range(-1, k - 1, -1):
                        if self.board[y + i][x - i] == "..":
                            moves.append([(y, x), (y + i, x - i)])
                            if (0 <= x - i + 1 <= 7) and (0 <= y - i + 1 <= 7):
                                if (self.whites_turn == True and self.board[y + i - 1][x - i + 1][0] == "b") or (
                                        self.whites_turn == False and self.board[y + i - 1][x - i + 1][0] == "w"):
                                    moves.append([(y, x), (y + i - 1, x - i + 1)])
                                    break
                        if (self.whites_turn == True and self.board[y + i][x - i][0] == "b") or (
                                self.whites_turn == False and self.board[y + i][x - i][0] == "w"):
                            moves.append([(y, x), (y + i, x - i)])
                            break

    def get_queen_moves(self, y, x, moves):  # Just both rook and bishop moves.
        self.get_bishop_moves(y, x, moves)
        self.get_rook_moves(y, x, moves)

    def get_king_moves(self, y, x, moves):
        for r in range(-1, 2):
            if 0 <= y + r <= 7:
                if r == 0:
                    for c in [-1, 1]:
                        if 0 <= x + c <= 7:
                            if (self.whites_turn == True and self.board[y + r][x + c][0] == "b") or (
                                    self.whites_turn == False and self.board[y + r][x + c][0] == "w") or (
                                    self.board[y + r][x + c] == ".."):
                                moves.append([(y, x), (y + r, x + c)])
                else:
                    for c in range(-1, 2):
                        if (self.whites_turn == True and self.board[y + r][x + c][0] == "b") or (
                                self.whites_turn == False and self.board[y + r][x + c][0] == "w") or (
                                self.board[y + r][x + c] == ".."):
                            moves.append([(y, x), (y + r, x + c)])

    def get_pawn_moves(self, y, x, moves):
        if self.board[y][x][0] == "w":
            if 0 <= y - 1 <= 7:
                if self.board[y - 1][x] == "..":
                    moves.append([(y, x), (y - 1, x)])
                    if 0 <= y - 2 <= 7:
                        if self.board[y - 2][x] == ".." and y == 6:
                            moves.append([(y, x), (y - 2, x)])
                if x - 1 >= 0:
                    if self.board[y - 1][x - 1][0] == "b":
                        moves.append([(y, x), (y - 1, x - 1)])
                if x + 1 <= 7:
                    if self.board[y - 1][x + 1][0] == "b":
                        moves.append([(y, x), (y - 1, x + 1)])

        if self.board[y][x][0] == "b":
            if 0 <= y + 1 <= 7:
                if self.board[y + 1][x] == "..":
                    moves.append([(y, x), (y + 1, x)])
                    if 0 <= y + 2 <= 7:
                        if self.board[y + 2][x] == ".." and y == 1:
                            moves.append([(y, x), (y + 2, x)])
                if x - 1 >= 0:
                    if self.board[y + 1][x - 1][0] == "w":
                        moves.append([(y, x), (y + 1, x - 1)])
                if x + 1 <= 7:
                    if self.board[y + 1][x + 1][0] == "w":
                        moves.append([(y, x), (y + 1, x + 1)])

    def get_castle_moves(self, moves):  # Check if King is in check and then if the king would move through check
        opp_moves = self.spaces_attacked()
        castle00 = True
        castle07 = True
        castle70 = True
        castle77 = True
        not_in_check = True
        for move in opp_moves:
            if self.whites_turn and (move[1] == self.w_king):
                not_in_check = False
            elif self.whites_turn == False and (move[1] == self.b_king):
                not_in_check = False
            else:
                if move[1] == (0, 4):
                    castle00 = False
                if move[1] == (0, 6):
                    castle07 = False
                if move[1] == (7, 4):
                    castle70 = False
                if move[1] == (7, 6):
                    castle77 = False
        if castle00 and not_in_check and (self.rook00_moved == 0) and (self.b_king_moved == 0):
            self.get_00castle(moves)
        if castle07 and not_in_check and (self.rook07_moved == 0) and (self.b_king_moved == 0):
            self.get_07castle(moves)
        if castle70 and not_in_check and (self.rook70_moved == 0) and (self.w_king_moved ==0 ):
            self.get_70castle(moves)
        if castle77 and not_in_check and (self.rook77_moved == 0) and (self.w_king_moved == 0):
            self.get_77castle(moves)
        if not not_in_check:
            print("Check")

    def get_00castle(self, moves):
        if (self.board[self.b_king[0]][self.b_king[1] - 1] == "..") and (self.board[self.b_king[0]][self.b_king[1] - 2] == "..") and (self.board[self.b_king[0]][self.b_king[1] - 3] == ".."):
            moves.append([(self.b_king[0], self.b_king[1]), (self.b_king[0], self.b_king[1] - 2)])

    def get_07castle(self, moves):
        if (self.board[self.b_king[0]][self.b_king[1] + 1] == "..") and (self.board[self.b_king[0]][self.b_king[1] + 2] == ".."):
            moves.append([(self.b_king[0], self.b_king[1]), (self.b_king[0], self.b_king[1] + 2)])

    def get_70castle(self, moves):
        if (self.board[self.w_king[0]][self.w_king[1] - 1] == "..") and (self.board[self.w_king[0]][self.w_king[1] - 2] == "..") and (self.board[self.w_king[0]][self.w_king[1] - 3] == ".."):
            moves.append([(self.w_king[0], self.w_king[1]), (self.w_king[0], self.w_king[1] - 2)])

    def get_77castle(self, moves):
        if (self.board[self.w_king[0]][self.w_king[1] + 1] == "..") and (self.board[self.w_king[0]][self.w_king[1] + 2] == ".."):
            moves.append([(self.w_king[0], self.w_king[1]), (self.w_king[0], self.w_king[1] + 2)])


    def all_check_checker(self):
        moves = self.get_all_moves()  # Gets all possible moves
        self.get_castle_moves(moves)  # Gets all castling moves
        for i in range(len(moves) - 1, -1, -1):
            self.make_move(moves[i])  # Makes that move
            self.whites_turn = not self.whites_turn
            if self.get_in_check():  # Gets all responses to the move
                moves.remove(moves[i])  # Removes that move if the responses takes the king
            self.whites_turn = not self.whites_turn
            self.undo()
        if len(moves) == 0:  # If no valid moves to make it's either stalemate or checkmate.
            if self.get_in_check():
                self.check_mate = True
                print("Checkmate")
            else:
                self.stale_mate = True
                print("Stale Mate")
        return moves

    def spaces_attacked(self):  # Generates all opponents moves
        self.whites_turn = not self.whites_turn
        opp_moves = self.get_all_moves()
        self.whites_turn = not self.whites_turn
        return opp_moves

    def get_in_check(self):  # If opponent can take the king (i.e. your in check) then return True
        opp_moves = self.spaces_attacked()
        for move in opp_moves:
            if self.whites_turn and (move[1] == self.w_king):
                return True
            elif self.whites_turn == False and (move[1] == self.b_king):
                return True
        return False

