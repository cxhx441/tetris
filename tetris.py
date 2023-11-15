import time
import os
from random import choice
import keyboard
import text_colors


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


class Piece:
    """
    Shapes holds the shape (ie "I") and the coordinates of it's rotation around the origin 0, 0
    0, 1, 2, 3 are the rotations. increments are clockwise.
    """

    shapes = {
        "I": {
            0: ((0, -2), (0, -1), (0, 0), (0, 1)),
            1: ((-1, 0), (0, 0), (1, 0), (2, 0)),
            2: ((1, -2), (1, -1), (1, 0), (1, 1)),
            3: ((-1, -1), (0, -1), (1, -1), (2, -1)),
        },
        "J": {
            0: ((-1, -2), (0, -2), (0, -1), (0, 0)),
            1: ((-1, -1), (0, -1), (1, -1), (-1, 0)),
            2: ((0, -2), (0, -1), (0, 0), (1, 0)),
            3: ((-1, -1), (0, -1), (1, -1), (1, -2)),
        },
        "L": {
            0: ((0, -2), (0, -1), (0, 0), (-1, 0)),
            1: ((-1, -1), (0, -1), (1, -1), (1, 0)),
            2: ((0, -2), (0, -1), (0, 0), (1, -2)),
            3: ((-1, -1), (0, -1), (1, -1), (-1, -2)),
        },
        "O": {
            0: ((-1, -1), (0, -1), (0, 0), (-1, 0)),
            1: ((-1, -1), (0, -1), (0, 0), (-1, 0)),
            2: ((-1, -1), (0, -1), (0, 0), (-1, 0)),
            3: ((-1, -1), (0, -1), (0, 0), (-1, 0)),
        },
        "S": {
            0: ((0, -2), (0, -1), (-1, -1), (-1, 0)),
            1: ((-1, -1), (0, -1), (0, 0), (1, 0)),
            2: ((1, -2), (1, -1), (0, -1), (0, 0)),
            3: ((-1, -2), (0, -2), (0, -1), (1, -1)),
        },
        "T": {
            0: ((0, -2), (0, -1), (0, 0), (-1, -1)),
            1: ((-1, -1), (0, -1), (1, -1), (0, 0)),
            2: ((0, -2), (0, -1), (0, 0), (1, -1)),
            3: ((-1, -1), (0, -1), (1, -1), (0, -2)),
        },
        "Z": {
            0: ((-1, -2), (-1, -1), (0, -1), (0, 0)),
            1: ((-1, 0), (0, 0), (0, -1), (1, -1)),
            2: ((0, -2), (0, -1), (1, -1), (1, 0)),
            3: ((-1, -1), (0, -1), (0, -2), (1, -2)),
        },
    }

    @staticmethod
    def get_random_piece():
        """ return a piece object with random shape. """
        return Piece(choice("IJLOSTZ"))

    def __init__(self, shape: str):
        self.shape = shape
        self.local_coords = None
        self.row = 0  # right
        self.col = 0  # down
        self.rotation = 0

    def get_coords(self):
        """get translated and rotated coordinates for the piece."""
        return [
            [coord[0] + self.row, coord[1] + self.col]
            for coord in self.shapes[self.shape][self.rotation]
        ]

    def rotate(self, direction):
        """
        Rotation right or left by 90 degrees.
        direction must be "CLOCKWISE" or "COUNTER_CLOCKWISE".
        """
        if direction == "CLOCKWISE":
            self.rotation += 1
            self.rotation %= 4
        elif direction == "COUNTER_CLOCKWISE":
            self.rotation -= 1
            if self.rotation == -1:
                self.rotation = 3

    def set_row_col(self, row, col):
        """set piece from current location to x, y"""
        self.row = row
        self.col = col

    def shift_row_col(self, row, col):
        """Shift piece from origin by x, y"""
        self.row += row
        self.col += col

    def clone(self):
        """ clone the piece. this is to avoid issues with deep copy. """
        cloned_piece = Piece("I") # shape input doesn't matter
        cloned_piece.shape = self.shape
        cloned_piece.row = self.row
        cloned_piece.col = self.col
        cloned_piece.rotation = self.rotation
        return cloned_piece


class Playfield:
    """ The space where the live piece and stack lives. """
    EMPTY = " "
    LR_BORDER = "|"
    TOP_BORDER = "_"
    BOTTOM_BORDER = "\u0305"  # overbar
    WIDTH = 10
    HEIGHT = 16
    PIECE_COLORS = {
        "I": text_colors.CYAN,
        "J": text_colors.BLUE,
        "L": text_colors.WHITE,
        "O": text_colors.YELLOW,
        "S": text_colors.GREEN,
        "T": text_colors.MAGENTA,
        "Z": text_colors.RED,
    }
    WALL_KICKS = {
        "JLTSZ": {
            (0, 1): ((0, 0), (0, -1), (1, -1), (-2, 0), (-2, -1)),
            (1, 0): ((0, 0), (0, 1), (-1, 1), (2, 0), (2, 1)),
            (1, 2): ((0, 0), (0, 1), (-1, 1), (2, 0), (2, 1)),
            (2, 1): ((0, 0), (0, -1), (1, -1), (-2, 0), (-2, -1)),
            (2, 3): ((0, 0), (0, 1), (1, 1), (-2, 0), (-2, 1)),
            (3, 2): ((0, 0), (0, -1), (-1, -1), (2, 0), (2, -1)),
            (3, 0): ((0, 0), (0, -1), (-1, -1), (2, 0), (2, -1)),
            (0, 3): ((0, 0), (0, 1), (1, 1), (-2, 0), (-2, 1)),
        },
        "I": {
            (0, 1): ((0, 0), (0, -2), (0, 1), (-1, -2), (2, 1)),
            (1, 0): ((0, 0), (0, 2), (0, -1), (1, 2), (-2, -1)),
            (1, 2): ((0, 0), (0, -1), (0, 2), (2, -1), (-1, 2)),
            (2, 1): ((0, 0), (0, 1), (0, -2), (-2, 1), (1, -2)),
            (2, 3): ((0, 0), (0, 2), (0, -1), (1, 2), (-2, -1)),
            (3, 2): ((0, 0), (0, -2), (0, 1), (-1, -2), (2, 1)),
            (3, 0): ((0, 0), (0, 1), (0, -2), (-2, 1), (1, -2)),
            (0, 3): ((0, 0), (0, -1), (0, 2), (2, -1), (-1, 2)),
        },
    }

    def __init__(self):
        self.matrix = [
            [Playfield.EMPTY] * Playfield.WIDTH for _ in range(Playfield.HEIGHT)
        ]
        self.stack = {}

    def __str__(self):
        mat_chrs = []
        mat_chrs += [Playfield.TOP_BORDER * (Playfield.WIDTH + 2), ("\n")]
        for row in range(Playfield.HEIGHT):
            mat_chrs.append(Playfield.LR_BORDER)
            for char in self.matrix[row]:
                if char in Piece.shapes:
                    mat_chrs += [self.PIECE_COLORS[char], char, text_colors.ENDC]
                else:
                    mat_chrs.append(char)
            mat_chrs += [Playfield.LR_BORDER, "\n"]
        mat_chrs += ["\u0305" * (Playfield.WIDTH + 2), "\n"]  # \u0305 == overbar
        return "".join(mat_chrs)

    def handle_tetris(self):
        """ Remove rows where all colums filled in. Update stack. """

        # get rows to elimate
        elim = []
        for r_idx, row in enumerate(self.matrix):
            filled = 0
            for el in row:
                if el != Playfield.EMPTY:
                    filled += 1
            if filled == Playfield.WIDTH:
                elim.append(r_idx)

        # remove rows from matrix and stack
        for r_idx in elim:
            for c_idx in range(Playfield.WIDTH):
                del self.stack[(r_idx, c_idx)]
            del self.matrix[r_idx]
            self.matrix.insert(0, [Playfield.EMPTY] * Playfield.WIDTH)

            to_be_removed = []
            to_be_added = []
            for coord, shape in self.stack.items():
                if coord[0] < r_idx:
                    to_be_removed.append(coord)
                    to_be_added.append(((coord[0] + 1, coord[1]), shape))

            for coord in to_be_removed:
                del self.stack[coord]
            for el in to_be_added:
                coord = el[0]
                shape = el[1]
                self.stack[coord] = shape


    def add_piece_to_stack(self, piece: Piece):
        """ add coords of piece to stack. """
        for coord in piece.get_coords():
            self.stack[tuple(coord)] = piece.shape

    def is_inside_stack(self, piece: Piece):
        """if intersection of coords and stack is not empty, True"""
        for coord in piece.get_coords():
            if tuple(coord) in self.stack:
                return True
        return False

    def remove_piece(self, piece: Piece):
        """ remove coords of piece matrix. """
        for coord in piece.get_coords():
            if coord[0] in range(Playfield.HEIGHT) and coord[1] in range(
                Playfield.WIDTH
            ):
                self.matrix[coord[0]][coord[1]] = Playfield.EMPTY

    def add_piece(self, piece):
        """ add coords of piece matrix. """
        for coord in piece.get_coords():
            if coord[0] in range(Playfield.HEIGHT) and coord[1] in range(
                Playfield.WIDTH
            ):
                self.matrix[coord[0]][coord[1]] = piece.shape

    def is_outside_bounds(self, piece):
        """ check if piece is outside border. """
        for coord in piece.get_coords():
            if coord[0] not in range(Playfield.HEIGHT) or coord[1] not in range(
                Playfield.WIDTH
            ):
                return True
        return False


class App:
    """ class for handling the app. """
    def __init__(self):
        self.pf = Playfield()
        self.piece = None
        self.spawn_piece()
        self.sleep_ms = 1000
        self.game_over = False

    def user_rotate_piece(self, direction: str):
        """ rotate the piece in the specified direction. """
        self.pf.remove_piece(self.piece)
        test_piece = self.piece.clone()
        from_rotation = test_piece.rotation
        test_piece.rotate(direction)
        to_rotation = test_piece.rotation

        if test_piece.shape == "I":
            for kick in Playfield.WALL_KICKS["I"][(from_rotation, to_rotation)]:
                test_piece.shift_row_col(kick[0], kick[1])
                if not self.pf.is_inside_stack(
                    test_piece
                ) and not self.pf.is_outside_bounds(test_piece):
                    self.piece = test_piece
                    self.pf.add_piece(self.piece)
                    self.draw_screen()
                    return
                test_piece.shift_row_col(-kick[0], -kick[1])

        else:
            for kick in Playfield.WALL_KICKS["JLTSZ"][(from_rotation, to_rotation)]:
                test_piece.shift_row_col(kick[0], kick[1])
                if not self.pf.is_inside_stack(
                    test_piece
                ) and not self.pf.is_outside_bounds(test_piece):
                    self.piece = test_piece
                    self.pf.add_piece(self.piece)
                    self.draw_screen()
                    return
                test_piece.shift_row_col(-kick[0], -kick[1])
        self.pf.add_piece(self.piece)
        self.draw_screen()

    def draw_screen(self):
        """ draw the screen """
        clear_screen()
        print(self.pf)

    def user_move_piece(self, row, col):
        """ move piece by specified rows and cols. """
        self.pf.remove_piece(self.piece)
        self.piece.shift_row_col(row, col)
        if self.pf.is_inside_stack(self.piece) or self.pf.is_outside_bounds(
            self.piece
        ):
            self.piece.shift_row_col(-row, -col)
            return
        self.pf.add_piece(self.piece)
        self.draw_screen()

    def user_hard_drop_piece(self):
        """ send the current piece to the top of the stack. """
        self.pf.remove_piece(self.piece)
        while not self.pf.is_inside_stack(
            self.piece
        ) and not self.pf.is_outside_bounds(self.piece):
            self.piece.shift_row_col(1, 0)
        self.piece.shift_row_col(-1, 0)
        self.pf.add_piece(self.piece)
        self.draw_screen()

    def step(self):
        """move the piece down or add it to the stack if it can't go down. handle tetriss."""
        self.pf.remove_piece(self.piece)
        self.piece.shift_row_col(1, 0)
        if self.pf.is_inside_stack(self.piece) or self.pf.is_outside_bounds(
            self.piece
        ):
            self.piece.shift_row_col(-1, 0)
            self.pf.add_piece_to_stack(self.piece)
            self.pf.add_piece(self.piece)
            self.pf.handle_tetris()
            self.spawn_piece()
        self.pf.add_piece(self.piece)
        if self.game_over is not True:
            self.draw_screen()

    def run(self):
        """run the instance."""
        while self.game_over is not True:
            self.listen_for_keys()
            self.step()

    def listen_for_keys(self):
        """listen for input keys for specified amount of time."""
        end_time = round(time.time() * 1000) + self.sleep_ms
        while round(time.time() * 1000) < end_time:
            time.sleep(self.sleep_ms / 1000)

    def spawn_piece(self):
        """get new random piece and add it to the playfield, if fails, end game."""
        self.piece = Piece.get_random_piece()
        self.piece.set_row_col(2, Playfield.WIDTH // 2)
        if self.pf.is_inside_stack(self.piece):
            self.piece.shift_row_col(-1, 0)
        if self.pf.is_inside_stack(self.piece):
            self.piece.shift_row_col(-1, 0)
        if self.pf.is_inside_stack(self.piece):
            self.end_game()
        self.pf.add_piece(self.piece)

    def end_game(self):
        """tell user game is over and set game over flag."""
        print("GAME_OVER")
        self.game_over = True


if __name__ == "__main__":
    app = App()
    keyboard.add_hotkey("d", lambda: app.user_move_piece(0, 1))
    keyboard.add_hotkey("a", lambda: app.user_move_piece(0, -1))
    keyboard.add_hotkey("s", lambda: app.user_move_piece(1, 0))
    keyboard.add_hotkey("space", app.user_hard_drop_piece)
    keyboard.add_hotkey("q", lambda: app.user_rotate_piece("COUNTER_CLOCKWISE"))
    keyboard.add_hotkey("e", lambda: app.user_rotate_piece("CLOCKWISE"))
    keyboard.add_hotkey("x", app.end_game)
    app.run()
    keyboard.unhook_all()
