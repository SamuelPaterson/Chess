"""
Storing all information about the current state.
And determining legal moves.
"""


class GameState:
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
        self.history = []  # Keeps a list of move history
        self.moved_pieces = []  # Keeps a list of the piece moved
        self.captured_pieces = []  # Keeps a list of the piece captured

        self.check_mate = False
        self.stale_mate = False

        self.rook00_moved = 0  # Keep track how many times any rook has moved. 00 = top left, 77 = bottom right
        self.rook07_moved = 0
        self.rook70_moved = 0
        self.rook77_moved = 0
        self.w_king_moved = 0  # Keep track how many times either king has moved.
        self.b_king_moved = 0

        self.w_king = (7, 4)  # Kings initial positions
        self.b_king = (0, 4)

    def make_move(self, clicks):  # Handles the movement of all the pieces, and specifies how castling works
        start_row = int(clicks[0][0])
        start_col = int(clicks[0][1])
        end_row = int(clicks[1][0])
        end_col = int(clicks[1][1])
        moved_piece = self.board[start_row][start_col]
        captured_piece = self.board[end_row][end_col]

        self.board[start_row][start_col] = ".."
        if moved_piece == "wP" and end_row == 0:  # Pawn Promotion
            self.board[end_row][end_col] = "wQ"
        elif moved_piece == "bP" and end_row == 7:
            self.board[end_row][end_col] = "bQ"
        else:
            self.board[end_row][end_col] = moved_piece

        if moved_piece == "wK":  # Updating the kings position and if castling it moves the rook.
            self.w_king = (end_row, end_col)
            self.w_king_moved = self.w_king_moved + 1
            if end_col - start_col == 2:  # If the white king castled king side
                self.board[7][7] = ".."
                self.board[7][5] = "wR"
                self.rook77_moved = self.rook77_moved + 1
            if end_col - start_col == -2:  # If the white king castled queen side
                self.board[7][0] = ".."
                self.board[7][3] = "wR"
                self.rook70_moved = self.rook70_moved + 1
        if moved_piece == "bK":
            self.b_king = (end_row, end_col)
            self.b_king_moved = self.b_king_moved + 1
            if end_col - start_col == 2:  # If the black king castled king side
                self.board[0][7] = ".."
                self.board[0][5] = "bR"
                self.rook07_moved = self.rook07_moved + 1
            if end_col - start_col == -2:  # If the black king castled queen side
                self.board[0][0] = ".."
                self.board[0][3] = "bR"
                self.rook00_moved = self.rook00_moved + 1

        if moved_piece[1] == "R":
            if start_row == 0:
                if start_col == 0:
                    self.rook00_moved = self.rook00_moved + 1
                elif start_col == 7:
                    self.rook07_moved = self.rook07_moved + 1
            if start_row == 7:
                if start_col == 0:
                    self.rook70_moved = self.rook70_moved + 1
                elif start_col == 7:
                    self.rook77_moved = self.rook77_moved + 1

        if moved_piece[1] == "P" and abs(start_col - end_col) == 1 and captured_piece == "..":  # If en passant
            if moved_piece[0] == "w":
                self.board[end_row + 1][end_col] = ".."
            if moved_piece[0] == "b":
                self.board[end_row - 1][end_col] = ".."

        self.whites_turn = not self.whites_turn
        self.history.append(clicks)
        self.moved_pieces.append(moved_piece)
        self.captured_pieces.append(captured_piece)

    def undo(self):
        if len(self.history) != 0:  # If there is a move to undo
            last_move = self.history.pop()
            moved_piece = self.moved_pieces.pop()
            captured_piece = self.captured_pieces.pop()
            self.board[last_move[0][0]][last_move[0][1]] = moved_piece
            self.board[last_move[1][0]][last_move[1][1]] = captured_piece  # Move pieces back
            self.whites_turn = not self.whites_turn

            if moved_piece == "wK":  # Updating kings position and undoing castling.
                self.w_king = (last_move[0])
                self.w_king_moved = self.w_king_moved - 1
                if last_move[1][1] - last_move[0][1] == 2:  # If the white king castled king side.
                    self.board[7][7] = "wR"
                    self.board[7][5] = ".."
                    self.rook77_moved = self.rook77_moved - 1
                elif last_move[1][1] - last_move[0][1] == -2:  # If the white king castled queen side.
                    self.board[7][0] = "wR"
                    self.board[7][3] = ".."
                    self.rook70_moved = self.rook70_moved - 1
            if moved_piece == "bK":
                self.b_king = (last_move[0])
                self.b_king_moved = self.b_king_moved - 1
                if last_move[1][1] - last_move[0][1] == 2:  # If the black king castled king side
                    self.board[0][7] = "bR"
                    self.board[0][5] = ".."
                    self.rook07_moved = self.rook07_moved - 1
                if last_move[1][1] - last_move[0][1] == -2:
                    self.board[0][0] = "bR"
                    self.board[0][3] = ".."
                    self.rook00_moved = self.rook00_moved - 1

            if last_move[0][0] == 0:
                if last_move[0][1] == 0:
                    self.rook00_moved = self.rook00_moved - 1
                elif last_move[0][1] == 7:
                    self.rook07_moved = self.rook07_moved - 1
            if last_move[0][0] == 7:
                if last_move[0][1] == 0:
                    self.rook70_moved = self.rook70_moved - 1
                elif last_move[0][1] == 7:
                    self.rook77_moved = self.rook77_moved - 1

            if moved_piece[1] == "P" and abs(last_move[0][1] - last_move[1][1]) == 1 and captured_piece == "..":
                if moved_piece[0] == "w":
                    self.board[last_move[1][0] + 1][last_move[1][1]]= "bP"
                if moved_piece[0] == "b":
                    self.board[last_move[1][0] - 1][last_move[1][1]] = "wP"

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
                        elif (self.whites_turn == True and self.board[y + i][x + i][0] == "b") or (
                                self.whites_turn == False and self.board[y + i][x + i][0] == "w"):
                            moves.append([(y, x), (y + i, x + i)])
                            break
                        else:
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
                        elif (self.whites_turn == True and self.board[y + i][x + i][0] == "b") or (
                                self.whites_turn == False and self.board[y + i][x + i][0] == "w"):
                            moves.append([(y, x), (y + i, x + i)])
                            break
                        else:
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
                        elif (self.whites_turn == True and self.board[y + i][x - i][0] == "b") or (
                                self.whites_turn == False and self.board[y + i][x - i][0] == "w"):
                            moves.append([(y, x), (y + i, x - i)])
                            break
                        else:
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
                        elif (self.whites_turn == True and self.board[y + i][x - i][0] == "b") or (
                                self.whites_turn == False and self.board[y + i][x - i][0] == "w"):
                            moves.append([(y, x), (y + i, x - i)])
                            break
                        else:
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
                        if 0 <= x + c <= 7:
                            if (self.whites_turn == True and self.board[y + r][x + c][0] == "b") or (
                                    self.whites_turn == False and self.board[y + r][x + c][0] == "w") or (
                                    self.board[y + r][x + c] == ".."):
                                moves.append([(y, x), (y + r, x + c)])

    def get_pawn_moves(self, y, x, moves):
        if self.board[y][x][0] == "w":
            self.get_en_passant(y, x, moves, "w")
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
            self.get_en_passant(y, x, moves, "b")
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

    def get_en_passant(self, y, x, moves, colour):
        if len(self.history) != 0:
            last_move = self.history[-1]
            distance_moved = abs(last_move[0][0] - last_move[1][0])
            last_move_col = last_move[0][1]  # Because only looking at pawns start or end column are the same.
            last_piece_moved = self.moved_pieces[-1]
            if colour == "w" and last_piece_moved == "bP" and y == 3:  # Only row that white can play en passant
                if distance_moved == 2:  # The pawn moved two spaces
                    if last_move_col == (x + 1):  # If black pawn is in next col.
                        moves.append([(y, x), (y - 1, x + 1)])
                    elif last_move_col == (x - 1):
                        moves.append([(y, x), (y - 1, x - 1)])
            if colour == "b" and last_piece_moved == "wP" and y == 4:  # Only row that black can play en passant
                if distance_moved == 2:  # The pawn moved two spaces
                    if last_move_col == (x + 1):  # If white pawn is in next col.
                        moves.append([(y, x), (y + 1, x + 1)])
                    elif last_move_col == (x - 1):
                        moves.append([(y, x), (y + 1, x - 1)])

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
                break
            elif not self.whites_turn and (move[1] == self.b_king):
                not_in_check = False
                break
            else:  # If not in check spaces inbetween king and rook are not under attack
                if move[1] == (0, 3):
                    castle00 = False
                if move[1] == (0, 5):
                    castle07 = False
                if move[1] == (7, 3):
                    castle70 = False
                if move[1] == (7, 5):
                    castle77 = False
        if castle00 and not_in_check and (self.rook00_moved == 0) and (self.b_king_moved == 0):
            self.get_00castle(moves)
        if castle07 and not_in_check and (self.rook07_moved == 0) and (self.b_king_moved == 0):
            self.get_07castle(moves)
        if castle70 and not_in_check and (self.rook70_moved == 0) and (self.w_king_moved ==0):
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
        self.get_castle_moves(moves)  # Gets all castling moves and append to moves
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
            else:
                self.stale_mate = True
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

    def get_piece_moves(self, click, legal_moves):  # Input 1 selected piece and gives a list of possible final pos.
        piece_moves = []
        for move in legal_moves:
            if move[0] == click:
                piece_moves.append(move[1])
        return piece_moves
