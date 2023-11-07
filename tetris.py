import time
import os
from random import choice


def clear_screen():
    os.system('cls' if os.name=='nt' else 'clear')

class Matrix:
    EMPTY_SPACE = " "
    FULL_SPACE = "O"
    LR_BORDER = "|"
    TOP_BORDER = "_"
    BOTTOM_BORDER = '\u0305'
    BASE_SLEEP = 1
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.matrix = [[Matrix.EMPTY_SPACE]*width for _ in range(height)]
        self.ground = set()
        self.piece = None
        self.pieces ={
            "I": ((0, -2), (0, -1), (0, 0), (0, 1)),
            "J": ((-1, -1), (0, -1), (0, 0), (0, 1)),
            "L": ((0, -2), (0, -1), (0, 0), (-1, 0)),
            "O": ((-1, -1), (0, -1), (1, 0), (-1, 0)),
            "S": ((0, -1), (0, 0), (-1, 0), (-1, 1)),
            "T": ((-1, 0), (0, -1), (0, 0), (0, 1)),
            "Z": ((-1, -1), (-1, 0), (0, 0), (0, 1)),
        }

    def __str__(self):
        mat_chrs = []

        mat_chrs += [Matrix.TOP_BORDER*(self.width+2), ("\n")]

        for r in range(self.height):
            mat_chrs.append(Matrix.LR_BORDER)

            for c in self.matrix[r]:
                mat_chrs.append(c)

            mat_chrs += [Matrix.LR_BORDER, "\n"]

        mat_chrs += ['\u0305'*(self.width+2), "\n"] # \u0305 == overbar

        return "".join(mat_chrs)


    def step(self):
        if self.piece is None:
            self.drop_piece()
        elif self.piece is not None:
            # if piece is touching ground, add_to_ground (add_to_ground will then check for tetris)
            self.move_piece_in_matrix("DOWN", force=True)
        clear_screen()
        print(self)
        time.sleep(1)

    def move_piece_in_matrix(self, direction, force=False):
        for coord in self.piece:
            if coord[0] in range(self.height) and coord[1] in range(self.width):
                self.matrix[coord[0]][coord[1]] = Matrix.EMPTY_SPACE # remove old piece position from matrix

        if force is True:
            for coord in self.piece:
                if direction == "DOWN": coord[0] += 1
                elif direction == "UP": coord[0] -= 1
                elif direction == "LEFT": coord[1] -= 1
                elif direction == "RIGHT": coord[1] += 1

        elif force is False:
            new_piece = self.piece.copy()

            for coord in new_piece:
                if direction == "DOWN": coord[0] += 1
                elif direction == "UP": coord[0] -= 1
                elif direction == "LEFT": coord[1] -= 1
                elif direction == "RIGHT": coord[1] += 1

            for coord in new_piece:
                if coord[1] not in range(self.width):
                    new_piece = self.piece
                    break

            self.piece = new_piece

        # update matrix
        for coord in self.piece:
            if coord[0] in range(self.height) and coord[1] in range(self.width):
                self.matrix[coord[0]][coord[1]] = Matrix.FULL_SPACE



    def drop_piece(self):
        self.piece = self.get_rand_piece()
        self.move_piece_to_middle()

    def get_rand_piece(self):
        rand_piece = choice(list(self.pieces.keys()))
        return [[x[0], x[1]] for x in self.pieces[rand_piece]]

    def move_piece_to_middle(self):
        for coord in self.piece: # move to middle
            coord[1] += self.width // 2


    def add_to_ground(self):
        # add piece to ground, null piece.
        # check for tetrises
        pass

    def check_for_tetrises(self):
        pass


if __name__ == "__main__":
    matrix = Matrix(10, 16)
    for i in range(7):
        matrix.step()
        matrix.move_piece_in_matrix("RIGHT")


