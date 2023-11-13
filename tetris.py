import time
import os
from random import choice
import keyboard
import text_colors


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


class Piece:
    """Shapes holds the shape (ie "I") and the coordinates of it's rotation around the origin 0, 0"""

    shapes = {
        "I": {
            0: [[0, -2], [0, -1], [0, 0], [0, 1]],
            1: [[-1, 0], [0, 0], [1, 0], [2, 0]],
            2: [[1, -2], [1, -1], [1, 0], [1, 1]],
            3: [[-1, -1], [0, -1], [1, -1], [2, -1]],
        },
        "J": {
            0: [[-1, -2], [0, -2], [0, -1], [0, 0]],
            1: [[-1, -1], [0, -1], [1, -1], [-1, 0]],
            2: [[0, -2], [0, -1], [0, 0], [1, 0]],
            3: [[-1, -1], [0, -1], [1, -1], [1, -2]],
        },
        "L": {
            0: [[0, -2], [0, -1], [0, 0], [-1, 0]],
            1: [[-1, -1], [0, -1], [1, -1], [1, 0]],
            2: [[0, -2], [0, -1], [0, 0], [1, -2]],
            3: [[-1, -1], [0, -1], [1, -1], [-1, -2]],
        },
        "O": {
            0: [[-1, -1], [0, -1], [0, 0], [-1, 0]],
            1: [[-1, -1], [0, -1], [0, 0], [-1, 0]],
            2: [[-1, -1], [0, -1], [0, 0], [-1, 0]],
            3: [[-1, -1], [0, -1], [0, 0], [-1, 0]],
        },
        "S": {
            0: [[0, -2], [0, -1], [-1, -1], [-1, 0]],
            1: [[-1, -1], [0, -1], [0, 0], [1, 0]],
            2: [[1, -2], [1, -1], [0, -1], [0, 0]],
            3: [[-1, -2], [0, -2], [0, -1], [1, -1]],
        },
        "T": {
            0: [[0, -2], [0, -1], [0, 0], [-1, -1]],
            1: [[-1, -1], [0, -1], [1, -1], [0, 0]],
            2: [[0, -2], [0, -1], [0, 0], [1, -1]],
            3: [[-1, -1], [0, -1], [1, -1], [0, -2]],
        },
        "Z": {
            0: [[-1, -2], [-1, -1], [0, -1], [0, 0]],
            1: [[-1, 0], [0, 0], [0, -1], [1, -1]],
            2: [[0, -2], [0, -1], [1, -1], [1, 0]],
            3: [[-1, -1], [0, -1], [0, -2], [1, -2]],
        },
    }

    def __init__(self):
        self.shape = None
        self.local_coords = None
        self.row = 0  # right
        self.col = 0  # down
        self.rotation = 0
        self.set_random_piece()

    def set_random_piece(self):
        self.shape = choice("IJLOSTZ")

    def set_piece(self, shape: str):
        self.shape = shape.upper()

    def get_coords(self):
        """get translated and rotated coordinates for the piece."""
        return [
            [coord[0] + self.row, coord[1] + self.col]
            for coord in self.shapes[self.shape][self.rotation]
        ]

    # def _get_rotated_coords(self):
    #     rotated_coords = [coord.copy() for coord in self.local_coords]
    #     for _ in range(self.rotation):
    #         for coord in rotated_coords:
    #             row, col = coord
    #             # 90° clockwise rotation: (row,col) becomes (-col, row)
    #             if (self.rotation >= 0):
    #                 coord[0], coord[1] = col, -row
    #     return rotated_coords

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
        cloned_piece = Piece()
        cloned_piece.shape = self.shape
        cloned_piece.row = self.row
        cloned_piece.col = self.col
        cloned_piece.rotation = self.rotation
        return cloned_piece


class Matrix:
    EMPTY_SPACE = " "
    LR_BORDER = "|"
    TOP_BORDER = "_"
    BOTTOM_BORDER = "\u0305"  # overbar
    WIDTH = 10
    HEIGHT = 16
    piece_colors = {
        "I": text_colors.CYAN,
        "J": text_colors.BLUE,
        "L": text_colors.WHITE,
        "O": text_colors.YELLOW,
        "S": text_colors.GREEN,
        "T": text_colors.MAGENTA,
        "Z": text_colors.RED,
    }
    wall_kicks = {
        "JLTSZ" : {
            (0, 1): ((0, 0), (0, -1), (1, -1), (-2, 0), (-2, -1)),
            (1, 0): ((0, 0), (0, 1), (-1, 1), (2, 0), (2, 1)),
            (1, 2): ((0, 0), (0, 1), (-1, 1), (2, 0), (2, 1)),
            (2, 1): ((0, 0), (0, -1), (1, -1), (-2, 0), (-2, -1)),
            (2, 3): ((0, 0), (0, 1), (1, 1), (-2, 0), (-2, 1)),
            (3, 2): ((0, 0), (0, -1), (-1, -1), (2, 0), (2, -1)),
            (3, 0): ((0, 0), (0, -1), (-1, -1), (2, 0), (2, -1)),
            (0, 3): ((0, 0), (0, 1), (1, 1), (-2, 0), (-2, 1)),
        },
        "I" : {
            (0, 1): ((0, 0), (0, -2), (0, 1), (-1, -2), (2, 1)),
            (1, 0): ((0, 0), (0, 2), (0, -1), (1, 2), (-2, -1)),
            (1, 2): ((0, 0), (0, -1), (0, 2), (2, -1), (-1, 2)),
            (2, 1): ((0, 0), (0, 1), (0, -2), (-2, 1), (1, -2)),
            (2, 3): ((0, 0), (0, 2), (0, -1), (1, 2), (-2, -1)),
            (3, 2): ((0, 0), (0, -2), (0, 1), (-1, -2), (2, 1)),
            (3, 0): ((0, 0), (0, 1), (0, -2), (-2, 1), (1, -2)),
            (0, 3): ((0, 0), (0, -1), (0, 2), (2, -1), (-1, 2)),
        }
    }
    def __init__(self):
        self.matrix = [
            [Matrix.EMPTY_SPACE] * Matrix.WIDTH for _ in range(Matrix.HEIGHT)
        ]
        self.stack = {
            "I": [],
            "J": [],
            "L": [],
            "O": [],
            "S": [],
            "T": [],
            "Z": [],
        }

        self.top_of_stack = [Matrix.HEIGHT] * Matrix.WIDTH

        self.piece = None
        self.spawn_piece()
        self.game_over = False
        self.sleep_ms = 1000

    def run(self):
        while self.game_over is not True:
            self.listen_for_keys()
            self.step()

    def listen_for_keys(self):
        end_time = round(time.time() * 1000) + self.sleep_ms
        while round(time.time() * 1000) < end_time:
            time.sleep(self.sleep_ms / 1000)

    def __str__(self):
        mat_chrs = []
        mat_chrs += [Matrix.TOP_BORDER * (Matrix.WIDTH + 2), ("\n")]
        for row in range(Matrix.HEIGHT):
            mat_chrs.append(Matrix.LR_BORDER)
            for char in self.matrix[row]:
                if char in Piece.shapes:
                    mat_chrs += [self.piece_colors[char], char, text_colors.ENDC]
                else:
                    mat_chrs.append(char)
            mat_chrs += [Matrix.LR_BORDER, "\n"]
        mat_chrs += ["\u0305" * (Matrix.WIDTH + 2), "\n"]  # \u0305 == overbar
        return "".join(mat_chrs)

    def step(self):
        self.remove_piece()
        self.piece.shift_row_col(1, 0)
        if self.is_inside_top_of_stack(self.piece):
            self.piece.shift_row_col(-1, 0)
            self.add_piece_to_stack(self.piece)
            self.add_piece_to_matrix(self.piece)
            # self.handle_tetris()
            self.spawn_piece()
        self.add_piece()
        if self.game_over is not True:
            self.draw_screen()

    def add_piece_to_matrix(self, piece: Piece):
        for coord in piece.get_coords():
            self.matrix[coord[0]][coord[1]] = piece.shape

    def add_piece_to_stack(self, piece: Piece):
        for coord in piece.get_coords():
            self.stack[piece.shape].append(coord)
        self.update_top_of_stack()

    def update_top_of_stack(self):
        for coords in self.stack.values():
            for coord in coords:
                existing = self.top_of_stack[coord[1]]
                new = coord[0]
                self.top_of_stack[coord[1]] = min(new, existing)

    def is_inside_top_of_stack(self, piece: Piece):
        for coord in piece.get_coords():
            if self.top_of_stack[coord[1]] == coord[0]:
                return True
        return False

    def is_inside_stack(self, piece: Piece):
        """if intersection of coords and stack is not empty, True"""
        for coord in piece.get_coords():
            for stack_coords in self.stack.values():
                if coord in stack_coords:
                    return True
        return False

    def draw_screen(self):
        clear_screen()
        print(self)

    def remove_piece(self):
        for coord in self.piece.get_coords():
            if coord[0] in range(Matrix.HEIGHT) and coord[1] in range(Matrix.WIDTH):
                self.matrix[coord[0]][coord[1]] = Matrix.EMPTY_SPACE

    def add_piece(self):
        for coord in self.piece.get_coords():
            if coord[0] in range(Matrix.HEIGHT) and coord[1] in range(Matrix.WIDTH):
                self.matrix[coord[0]][coord[1]] = self.piece.shape

    def user_rotate_piece(self, direction: str):
        self.remove_piece()
        test_piece = self.piece.clone()
        from_rotation = test_piece.rotation
        test_piece.rotate(direction)
        to_rotation = test_piece.rotation

        if test_piece.shape == "I":
            for kick in Matrix.wall_kicks["I"][(from_rotation, to_rotation)]:
                test_piece.shift_row_col(kick[0], kick[1])
                if not self.is_inside_stack(test_piece) and \
                    not self.is_outside_bounds(test_piece):
                    self.piece = test_piece
                    self.add_piece()
                    self.draw_screen()
                    return
                test_piece.shift_row_col(-kick[0], -kick[1])

        else:
            for kick in Matrix.wall_kicks["JLTSZ"][(from_rotation, to_rotation)]:
                test_piece.shift_row_col(kick[0], kick[1])
                if not self.is_inside_stack(test_piece) and \
                    not self.is_outside_bounds(test_piece):
                    self.piece = test_piece
                    self.add_piece()
                    self.draw_screen()
                    return
                test_piece.shift_row_col(-kick[0], -kick[1])
        self.add_piece()
        self.draw_screen()

    def user_move_piece(self, row, col):
        self.remove_piece()
        self.piece.shift_row_col(row, col)
        if self.is_inside_stack(self.piece) or self.is_outside_bounds(self.piece):
            self.piece.shift_row_col(-row, -col)
            return
        self.add_piece()
        self.draw_screen()

    def is_outside_bounds(self, piece):
        for coord in piece.get_coords():
            if coord[0] not in range(Matrix.HEIGHT) or coord[1] not in range(
                Matrix.WIDTH
            ):
                return True
        return False

    def spawn_piece(self):
        """
        if piece part of stack, move up one
        if piece still part of stack, move up one
        if still inside top of stack, end game.
        """
        self.piece = Piece()
        self.piece.set_row_col(2, Matrix.WIDTH // 2)
        if self.is_inside_stack(self.piece):
            self.piece.shift_row_col(1, 0)
        if self.is_inside_stack(self.piece):
            self.piece.shift_row_col(1, 0)
        if self.is_inside_stack(self.piece):
            self.end_game()
        self.add_piece()

    def end_game(self):
        print("GAME_OVER")
        self.game_over = True

    def check_for_tetrises(self):
        pass


if __name__ == "__main__":
    matrix = Matrix()
    matrix.sleep_ms = 1000

    keyboard.add_hotkey("d", lambda: matrix.user_move_piece(0, 1))
    keyboard.add_hotkey("a", lambda: matrix.user_move_piece(0, -1))
    keyboard.add_hotkey("s", lambda: matrix.user_move_piece(1, 0))
    keyboard.add_hotkey("q", lambda: matrix.user_rotate_piece("COUNTER_CLOCKWISE"))
    keyboard.add_hotkey("e", lambda: matrix.user_rotate_piece("CLOCKWISE"))
    keyboard.add_hotkey("x", matrix.end_game)
    matrix.run()
    keyboard.unhook_all()
