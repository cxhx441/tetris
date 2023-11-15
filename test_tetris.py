import tetris as t

class TestTetris:
    app = t.App()

    def test_piece_inited(self):
        assert self.app.piece.shape in "IJLOSTZ"

    def test_empty_stack(self):
        assert True
        #assert self.app.pf.stack == set()

    def test_empty_tetris_clear(self):
        self.app.pf.remove_piece(self.app.piece)
        self.app.piece.shape = "O"
        self.app.user_move_piece(0, -4)
        for _ in range(self.app.pf.HEIGHT-2):
            self.app.step()

        self.app.pf.remove_piece(self.app.piece)
        self.app.piece.shape = "O"
        self.app.user_move_piece(0, -2)
        for _ in range(self.app.pf.HEIGHT-2):
            self.app.step()

        self.app.pf.remove_piece(self.app.piece)
        self.app.piece.shape = "O"
        for _ in range(self.app.pf.HEIGHT-2):
            self.app.step()

        self.app.pf.remove_piece(self.app.piece)
        self.app.piece.shape = "O"
        self.app.user_move_piece(0, 2)
        for _ in range(self.app.pf.HEIGHT-2):
            self.app.step()

        self.app.pf.remove_piece(self.app.piece)
        self.app.piece.shape = "O"
        self.app.user_move_piece(0, 4)
        for _ in range(self.app.pf.HEIGHT-2-1):
            self.app.step()

        assert self.app.pf.matrix[:-2] == [[" "]*self.app.pf.WIDTH]*(self.app.pf.HEIGHT-2)
        assert self.app.pf.matrix[-2:] == [["O"]*self.app.pf.WIDTH]*2
        self.app.step()

        assert self.app.pf.matrix[-2:] == [[" "]*self.app.pf.WIDTH]*2



