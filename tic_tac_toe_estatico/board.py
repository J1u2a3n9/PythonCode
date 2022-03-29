import numpy as np
from numpy import inf
import random
from .player import Player, player_names, other_player
from tic_tac_toe.agents.base_agent import Move

class CeldaState:
    empty = -1
    X = Player.X
    O = Player.O
    global texts
    global texts_two

    all_states = Player.all_players + [empty]

    celda_char = {
        empty: " ",
        X: player_names[X],
        O: player_names[O],
    }



class Board(object):
    texts="row_num must be between 0 and"
    texts_two="col_num must be between 0 and"
    def __init__(self, size=3, num_to_win=None):
        num_to_win = num_to_win or size
        if num_to_win > size:
            raise ValueError("num_to_win cannot be larger than size.")

        self.size = size
        self.num_to_win = num_to_win
        self.usable_board = CeldaState.empty * np.ones(shape=(size, size),dtype=np.int8)
        self.matrix = self.create_matrix()
        self.hash = self.initialize_hash()

    def row(self, row_num):
        if row_num < 0 or row_num >= self.size:
            raise ValueError(texts+{}.format(self.size))
        return self.usable_board[row_num, :]

    def col(self, col_num):
        if col_num < 0 or col_num >= self.size:
            raise ValueError(texts_two+{}.format(
                self.size))
        return self.usable_board[:, col_num]

    def cell(self, row_num, col_num):
        if row_num < 0 or row_num >= self.size:
            raise ValueError(texts+{}.format(self.size))
        if col_num < 0 or col_num >= self.size:
            raise ValueError(texts_two+ {}.format(self.size))
        return self.usable_board[row_num, col_num]
        

    def main_diagonal(self, offset=0):
        return np.diagonal(self.usable_board, offset=offset)

    def secondary_diagonal(self, offset=0):
        n = self.size - 1
        row_start = max(offset, 0)
        row_stop = min(n + offset, n)
        start = n * row_start + n + offset
        stop = n * row_stop + n + offset + 1
        step = n
        return self.usable_board.ravel()[start:stop:step]

    def set_cell(self, state, row_num, col_num):
        if state not in CeldaState.all_states:
            raise ValueError("Cell state cannot be {}.".format(state))

        if row_num < 0 or row_num >= self.size:
            raise ValueError(texts+{}.format(self.size))

        if col_num < 0 or col_num >= self.size:
            raise ValueError("col_num must be between 0 and {}.".format(self.size))

        index = (row_num * self.size) + col_num
        current_state = self.cell(row_num, col_num)

        if current_state != CeldaState.empty:
            old_bit = self.matrix[index][current_state]
            self.hash ^= old_bit

        if state != CeldaState.empty:
            bitstring = self.matrix[index][state]
            self.hash ^= bitstring

        self.usable_board[row_num, col_num] = state

        return self

    def heuristic(self, player):
        def line_count(line):
            conseq_x = 0
            max_conseq_x = 0
            range_x = 0
            max_range_x = 0
            num_x_r = 0
            max_num_x_r = 0

            conseq_o = 0
            max_conseq_o = 0            
            range_o = 0            
            max_range_o = 0            
            num_o_r = 0            
            max_num_o_r = 0
            for i in range(0, len(line)):
                if line[i] == other_player(player):
                    conseq_o += 1
                    range_o += 1
                    num_o_r += 1

                    max_conseq_x = max(conseq_x, max_conseq_x)
                    conseq_x = 0

                    max_range_x = max(range_x, max_range_x)
                    range_x = 0

                    max_num_x_r = max(num_x_r, max_num_x_r)
                    num_x_r = 0
                elif line[i] == player:
                    conseq_x += 1
                    range_x += 1
                    num_x_r += 1

                    max_conseq_o = max(conseq_o, max_conseq_o)
                    conseq_o = 0

                    max_range_o = max(range_o, max_range_o)
                    range_o = 0

                    max_num_o_r = max(num_o_r, max_num_o_r)
                    num_o_r = 0
                else:
                    range_o += 1
                    max_conseq_o = max(conseq_o, max_conseq_o)
                    conseq_o = 0

                    range_x += 1
                    max_conseq_x = max(conseq_x, max_conseq_x)
                    conseq_x = 0

            max_conseq_x = max(conseq_x, max_conseq_x)
            max_num_x_r = max(num_x_r, max_num_x_r)
            max_range_x = max(range_x, max_range_x)

            max_conseq_o = max(conseq_o, max_conseq_o)
            max_num_o_r = max(num_o_r, max_num_o_r)
            max_range_o = max(range_o, max_range_o)

            if max_conseq_x == self.num_to_win:
                return 10000
            elif max_conseq_o == self.num_to_win:
                return -10000
            
            if max_range_x >= self.num_to_win:
                if max_num_x_r == self.num_to_win - 1:
                    return 1000
                return max_num_x_r
            if max_range_o >= self.num_to_win:
                if max_num_o_r == self.num_to_win - 1:
                    return -5000
                return 0 - max_num_o_r
            
            return 0

        value = 0
        for l in self.all_lines:
            value += line_count(l)

        return value
    
    def randomize(self):
        def rand_move(player):
            return Move(player, random.randint(0,9), random.randint(0,9))

        moves = random.randint(0,8)
        moves = moves / 2
        player = Player.X

        while moves > 0:
            valid_moves = []
            for i, j in self.empty_cells:
                valid_moves.append(Move(player, i, j))

            move = rand_move(player)
            while move not in valid_moves:
                move = rand_move(player)

            assert self.cell(move.row, move.col) == CeldaState.empty
            self.set_cell(move.player, move.row, move.col)

            if(player == Player.O):
                moves -= 1
            player = other_player(player)

    def create_matrix(self):
        #usable_board config matrix, given random values. 
        #2(X, O) by 9(num of tiles) large
        #index X is 0 and O is 1
        array = [[random.getrandbits(32) for i in range(2)] for j in range(self.size * self.size)]

        return array

    def initialize_hash(self):
        h = 0
        for i in range(self.size * self.size):
            if self.cell(int(i/self.size),i%self.size) != CeldaState.empty:
                j = self.cell(int(i/self.size),i%self.size)
                h ^= self.matrix[i][j]
        return h

    @property
    def hash(self):
        return self.hash

    @property
    def size(self):
        return self.size

    @property
    def num_to_win(self):
        return self.num_to_win

    @property
    def diagonals(self):
        max_offset = self.size - self.num_to_win
        offsets = range(-max_offset, max_offset + 1)

        main_diagonals = [self.main_diagonal(offset) for offset in offsets]
        secondary_diagonals = [self.secondary_diagonal(offset)
                               for offset in offsets]
        return main_diagonals + secondary_diagonals

    @property
    def rows(self):
        return [self.row(i) for i in range(self.size)]

    @property
    def cols(self):
        return [self.col(i) for i in range(self.size)]

    @property
    def all_lines(self):
        return self.diagonals + self.rows + self.cols

    @property
    def empty_cells(self):
        return [(i, j)
                for i in range(self.size)
                for j in range(self.size)
                if self.cell(i, j) == CeldaState.empty]

    @property
    def winner(self):
        def line_winner(line):
            # scan through the line, counting the current longest sequence of
            # equal elements
            # when the length of the current sequence is sufficient for a win
            # and the current sequence is one of the players, return
            current_state = line[0]
            
            current_length = 1
            for i in range(1, len(line)):
                if current_state == line[i]:
                    current_length += 1
                else:
                    current_state = line[i]
                    current_length = 1

                if (current_length == self.num_to_win
                        and current_state in Player.all_players):
                    return current_state

            return None

        for l in self.all_lines:
            line_winner = line_winner(l)
            if line_winner is not None:
                return line_winner

        return None

    def __repr__(self):
        def row_to_str(enumerated_row):
            i, row = enumerated_row
            return "{: >2}   ".format(i) \
                   + " │ ".join(map(lambda c: CeldaState.celda_char[c], row)) \
                   + " "

        row_separator = "\n    " + "┼".join(["───"] * self.size) + "\n"
        all_rows = row_separator.join(map(row_to_str, enumerate(self.rows)))
        header = "    " + " ".join(map(lambda i: " {: <2}".format(i),
                                       range(self.size)))
        #print(self.heuristic(Player.X))
        return header + "\n\n" + all_rows
