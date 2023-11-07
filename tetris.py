import time
import os
from random import choice
import text_colors


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


class Matrix:
    EMPTY_SPACE = " "
    LR_BORDER = "|"
    TOP_BORDER = "_"
    BOTTOM_BORDER = "\u0305"
    BASE_SLEEP = 0.25
    WIDTH = 10
    HEIGHT = 16

    def __init__(self):
        self.matrix = [
            [Matrix.EMPTY_SPACE] * Matrix.WIDTH for _ in range(Matrix.HEIGHT)
        ]
        self.ground = set()
        self.piece = None
        self.pieces = {
            "I": ((2, 3), (2, 4), (2, 5), (2, 6)),
            "J": ((1, 3), (2, 3), (2, 4), (2, 5)),
            "L": ((1, 3), (2, 3), (2, 4), (2, 5)),
            "O": ((1, 4), (2, 4), (1, 5), (2, 5)),
            "S": ((2, 3), (2, 4), (1, 4), (1, 5)),
            "T": ((2, 3), (2, 4), (1, 4), (2, 5)),
            "Z": ((1, 3), (1, 4), (2, 4), (2, 5)),
        }
        self.piece_colors = {
            "I": text_colors.CYAN,
            "J": text_colors.BLUE,
            "L": text_colors.WHITE,
            "O": text_colors.YELLOW,
            "S": text_colors.GREEN,
            "T": text_colors.MAGENTA,
            "Z": text_colors.RED,
        }

    def __str__(self):
        mat_chrs = []

        mat_chrs += [Matrix.TOP_BORDER * (Matrix.WIDTH + 2), ("\n")]

        for r in range(Matrix.HEIGHT):
            mat_chrs.append(Matrix.LR_BORDER)

            for c in self.matrix[r]:
                if c in self.pieces.keys():
                    mat_chrs += [self.piece_colors[c], c, text_colors.ENDC]
                else:
                    mat_chrs.append(c)

            mat_chrs += [Matrix.LR_BORDER, "\n"]

        mat_chrs += ["\u0305" * (Matrix.WIDTH + 2), "\n"]  # \u0305 == overbar

        return "".join(mat_chrs)

    def step(self):
        if self.piece is None:
            self.spawn_piece()
        elif self.piece is not None:
            # if piece is touching ground, add_to_ground (add_to_ground will then check for tetris)
            self.move_piece_in_matrix("DOWN", force=True)
        clear_screen()
        print(self)
        time.sleep(Matrix.BASE_SLEEP)

    def move_piece_in_matrix(self, direction, force=False):
        for coord in self.piece["coords"]:
            if coord[0] in range(Matrix.HEIGHT) and coord[1] in range(Matrix.WIDTH):
                self.matrix[coord[0]][
                    coord[1]
                ] = Matrix.EMPTY_SPACE  # remove old piece position from matrix

        if force is True:
            for coord in self.piece["coords"]:
                if direction == "DOWN":
                    coord[0] += 1
                elif direction == "UP":
                    coord[0] -= 1
                elif direction == "LEFT":
                    coord[1] -= 1
                elif direction == "RIGHT":
                    coord[1] += 1

        elif force is False:
            new_piece = self.piece.copy()

            for coord in new_piece:
                if direction == "DOWN":
                    coord[0] += 1
                elif direction == "UP":
                    coord[0] -= 1
                elif direction == "LEFT":
                    coord[1] -= 1
                elif direction == "RIGHT":
                    coord[1] += 1

            for coord in new_piece:
                if coord[1] not in range(Matrix.WIDTH):
                    new_piece = self.piece
                    break

            self.piece = new_piece

        # update matrix
        for coord in self.piece["coords"]:
            if coord[0] in range(Matrix.HEIGHT) and coord[1] in range(Matrix.WIDTH):
                self.matrix[coord[0]][coord[1]] = self.piece["shape"]

    def spawn_piece(self):
        self.piece = self.get_rand_piece()
        ## TEMP! JUST MAKE IT SHOW
        for coord in self.piece["coords"]:
            if coord[0] in range(Matrix.HEIGHT) and coord[1] in range(Matrix.WIDTH):
                self.matrix[coord[0]][coord[1]] = self.piece["shape"]
        # if piece part of ground, move up one
        # if piece still part of ground, move up one
        # if piece completely off screen, end game.

    def get_rand_piece(self):
        rand_piece = choice(list(self.pieces.keys()))
        return {
            "shape": rand_piece,
            "coords": [[x[0], x[1]] for x in self.pieces[rand_piece]],
        }

    def add_to_ground(self):
        # add piece to ground, null piece.
        # check for tetrises
        pass

    def check_for_tetrises(self):
        pass


if __name__ == "__main__":
    matrix = Matrix()

    for i in range(5):
        matrix.step()
    #     matrix.move_piece_in_matrix("RIGHT")
