import time
import os
from random import choice
import keyboard
import text_colors
import copy


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

class Piece:
    shape = None
    def __init__(self):
        self.local_coords = [[0, 0], [0, 0], [0, 0], [0, 0]]
        self.x = 0 # right
        self.y = 0 # down
        self.rotation = 0

    def get_coords(self):
        """ get translated and rotated coordinates for the piece. """
        rotated_coords = self._get_rotated_coords()
        translated_coords = [[coord[0]+self.x, coord[1]+self.y] for coord in rotated_coords ]
        return translated_coords

    def _get_rotated_coords(self):
        rotated_coords = [coord.copy() for coord in self.local_coords]
        for _ in range(abs(self.rotation)):
            for coord in rotated_coords:
                x, y = coord
                if self.rotation >= 0: # 90° clockwise rotation: (x,y) becomes (y,−x)
                    coord[0], coord[1] = y, -x
                elif self.rotation < 0: # 90° counterclockwise rotation: (x,y) becomes (−y,x)
                    coord[0], coord[1] = -y, x
        return rotated_coords

    def rotate(self, direction):
        """
        Rotation right or left by 90 degrees.
        direction must be "CLOCKWISE" or "COUNTER_CLOCKWISE".
        """
        if direction == "CLOCKWISE":
            self.rotation += 1
            self.rotation %= 3
        elif direction == "COUNTER_CLOCKWISE":
            self.rotation -= 1
            self.rotation = -1 * (abs(self.rotation) % 4)

    def set_x_y(self, x, y):
        """ set piece from current location to x, y """
        self.x = x
        self.y = y

    def shift_x_y(self, x, y):
        """ Shift piece from origin by x, y """
        self.x += x
        self.y += y



class I_Piece(Piece):
    Piece.shape = "I"
    def __init__(self):
        Piece.__init__(self)
        self.coords = [[0, -2], [0, -1], [0, 0], [0, 1]]

class J_Piece(Piece):
    Piece.shape = "J"
    def __init__(self):
        Piece.__init__(self)
        self.coords = [[-1, -2], [0, -2], [0, -1], [0, 0]]

class L_Piece(Piece):
    Piece.shape = "L"
    def __init__(self):
        Piece.__init__(self)
        self.coords = [[0, -2], [0, -1], [0, 0], [-1, 0]]

class O_Piece(Piece):
    Piece.shape = "O"
    def __init__(self):
        Piece.__init__(self)
        self.coords = [[-1, -1], [0, -1], [0, 0], [-1, 0]]

class S_Piece(Piece):
    Piece.shape = "S"
    def __init__(self):
        Piece.__init__(self)
        self.coords = [[0, -2], [0, -1], [-1, -1], [-1, 0]]

class T_Piece(Piece):
    Piece.shape = "T"
    def __init__(self):
        Piece.__init__(self)
        self.coords = [[0, -2], [0, -1], [0, 0], [-1, -1]]

class Z_Piece(Piece):
    Piece.shape = "Z"
    def __init__(self):
        Piece.__init__(self)
        self.coords = [[-1, -2], [-1, -1], [0, -1], [0, 0]]


class Matrix:
    EMPTY_SPACE = " "
    LR_BORDER = "|"
    TOP_BORDER = "_"
    BOTTOM_BORDER = "\u0305" # overbar
    WIDTH = 10
    HEIGHT = 16
    pieces = {
        "I": ((2, 3), (2, 4), (2, 5), (2, 6)),
        "J": ((1, 3), (2, 3), (2, 4), (2, 5)),
        "L": ((1, 3), (2, 3), (2, 4), (2, 5)),
        "O": ((1, 4), (2, 4), (1, 5), (2, 5)),
        "S": ((2, 3), (2, 4), (1, 4), (1, 5)),
        "T": ((2, 3), (2, 4), (1, 4), (2, 5)),
        "Z": ((1, 3), (1, 4), (2, 4), (2, 5)),
    }
    piece_colors = {
        "I": text_colors.CYAN,
        "J": text_colors.BLUE,
        "L": text_colors.WHITE,
        "O": text_colors.YELLOW,
        "S": text_colors.GREEN,
        "T": text_colors.MAGENTA,
        "Z": text_colors.RED,
    }

    def __init__(self):
        self.matrix = [
            [Matrix.EMPTY_SPACE] * Matrix.WIDTH for _ in range(Matrix.HEIGHT)
        ]
        self.stack = {
            "I": list(),
            "J": list(),
            "L": list(),
            "O": list(),
            "S": list(),
            "T": list(),
            "Z": list(),
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

        for r in range(Matrix.HEIGHT):
            mat_chrs.append(Matrix.LR_BORDER)

            for c in self.matrix[r]:
                if c in Matrix.pieces.keys():
                    mat_chrs += [self.piece_colors[c], c, text_colors.ENDC]
                else:
                    mat_chrs.append(c)

            mat_chrs += [Matrix.LR_BORDER, "\n"]

        mat_chrs += ["\u0305" * (Matrix.WIDTH + 2), "\n"]  # \u0305 == overbar

        return "".join(mat_chrs)

    def step(self):
        temp_moved_piece = self.get_temp_moved_piece("DOWN")
        if self.is_inside_top_of_stack(temp_moved_piece):
            self.add_piece_to_stack(self.piece)
            # self.handle_tetris()
            self.spawn_piece()
        else:
            self.move_piece("DOWN")

        if self.game_over is not True:
            self.draw_screen()

    def add_piece_to_stack(self, piece):
        for coord in piece["coords"]:
            self.stack[piece["shape"]].append(coord)
        self.update_top_of_stack()

    def update_top_of_stack(self):
        for coords in self.stack.values():
            for coord in coords:
                existing = self.top_of_stack[coord[1]]
                new = coord[0]
                self.top_of_stack[coord[1]] = min(new, existing)

    def is_inside_top_of_stack(self, piece):
        for coord in piece["coords"]:
            # if coord == top of stack, return true
            if self.top_of_stack[coord[1]] == coord[0]:
                return True
        return False

    def is_inside_stack(self, piece):
        for coord in piece["coords"]:
            for stack_coords in self.stack.values():
                if coord in stack_coords:
                    return True
        return False

    def draw_screen(self):
        clear_screen()
        print(self)

    def remove_piece(self):
        for coord in self.piece["coords"]:
            if coord[0] in range(Matrix.HEIGHT) and coord[1] in range(Matrix.WIDTH):
                self.matrix[coord[0]][coord[1]] = Matrix.EMPTY_SPACE

    def add_piece(self):
        for coord in self.piece["coords"]:
            if coord[0] in range(Matrix.HEIGHT) and coord[1] in range(Matrix.WIDTH):
                self.matrix[coord[0]][coord[1]] = self.piece["shape"]

    def move_piece(self, direction):
        self.remove_piece()
        for coord in self.piece["coords"]:
            if direction == "DOWN":
                coord[0] += 1
            elif direction == "UP":
                coord[0] -= 1
            elif direction == "LEFT":
                coord[1] -= 1
            elif direction == "RIGHT":
                coord[1] += 1
        self.add_piece()

    def user_rotate_piece(self, direction):
        """
        90° clockwise rotation: (x,y) becomes (y,−x)
        90° counterclockwise rotation: (x,y) becomes (−y,x)
        """
        self.remove_piece()
        min_x, min_y = float("inf"), float("inf"),
        max_x, max_y = -float("inf"), -float("inf")
        temp_piece = copy.deepcopy(self.piece)
        for coord in temp_piece["coords"]:
            min_x = min(min_x, coord[0])
            min_y = min(min_y, coord[1])
            max_x = max(max_x, coord[0])
            max_y = max(max_y, coord[1])
        mid_x, mid_y = (max_x-min_x // 2), (max_x-min_x // 2)

        if direction == "CLOCKWISE":
            for coord in temp_piece["coords"]:
                x, y = coord
                x, y = x-mid_x-1, y-mid_y-1
                x, y = y, -x
                x, y = x + mid_x+1, y + mid_y+1
                coord[0], coord[1] = x, y
        elif direction == "COUNTER_CLOCKWISE":
            for coord in temp_piece["coords"]:
                x, y = coord
                x, y = x-mid_x-1, y-mid_y-1
                x, y = -y, x
                x, y = x + mid_x+1, y + mid_y+1
                coord[0], coord[1] = x, y

        self.piece = temp_piece
        self.add_piece()
        self.draw_screen()


    def user_move_piece(self, direction):
        temp_moved_piece = self.get_temp_moved_piece(direction)
        if self.is_inside_stack(temp_moved_piece) or self.is_outside_bounds(
            temp_moved_piece
        ):
            return
        self.move_piece(direction)
        self.draw_screen()

    def is_outside_bounds(self, piece):
        for coord in piece["coords"]:
            if coord[0] not in range(Matrix.HEIGHT) or coord[1] not in range(
                Matrix.WIDTH
            ):
                return True
        return False

    def get_temp_moved_piece(self, direction):
        temp_moved_piece = copy.deepcopy(self.piece)
        for coord in temp_moved_piece["coords"]:
            if direction == "DOWN":
                coord[0] += 1
            elif direction == "UP":
                coord[0] -= 1
            elif direction == "LEFT":
                coord[1] -= 1
            elif direction == "RIGHT":
                coord[1] += 1

        # for coord in new_piece:
        #     if coord[1] not in range(Matrix.WIDTH):
        #         new_piece = self.piece
        #         break

        return temp_moved_piece

    def spawn_piece(self):
        self.piece = self.get_rand_piece()
        # if piece part of stack, move up one
        if self.is_inside_stack(self.piece):
            for coord in self.piece["coords"]:
                coord[0] -= 1
        # if piece still part of stack, move up one
        if self.is_inside_stack(self.piece):
            for coord in self.piece["coords"]:
                coord[0] -= 1
        # if still inside top of stack, end game.
        if self.is_inside_stack(self.piece):
            self.end_game()

        for coord in self.piece["coords"]:
            if coord[0] in range(Matrix.HEIGHT) and coord[1] in range(Matrix.WIDTH):
                self.matrix[coord[0]][coord[1]] = self.piece["shape"]

    def end_game(self):
        print("GAME_OVER")
        self.game_over = True

    def get_rand_piece(self):
        rand_piece = choice(list(self.pieces.keys()))
        return {
            "shape": rand_piece,
            "coords": [[x[0], x[1]] for x in self.pieces[rand_piece]],
        }

    def check_for_tetrises(self):
        pass


if __name__ == "__main__":
    matrix = Matrix()
    matrix.sleep_ms = 1000

    keyboard.add_hotkey("d", lambda: matrix.user_move_piece("RIGHT"))
    keyboard.add_hotkey("a", lambda: matrix.user_move_piece("LEFT"))
    keyboard.add_hotkey("s", lambda: matrix.user_move_piece("DOWN"))
    keyboard.add_hotkey("q", lambda: matrix.user_rotate_piece("COUNTER_CLOCKWISE"))
    keyboard.add_hotkey("e", lambda: matrix.user_rotate_piece("CLOCKWISE"))
    keyboard.add_hotkey("x", matrix.end_game)
    matrix.run()
    keyboard.unkook_all()

