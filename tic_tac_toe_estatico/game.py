from copy import deepcopy
import time
import timeit

from .board import Board, CeldaState
from .player import Player, player_names


class Game(object):
    def __init__(self, player_x, player_o, size=3, num_to_win=None,starting_board=None):
        self.player_x = player_x
        self.player_o = player_o

        self.current_player = (Player.X, self.player_x)
        self.next_player = (Player.O, self.player_o)

        self.results = open('times.txt','w')

        if starting_board is None:
            self.board = Board(size=size, num_to_win=num_to_win)
        else:
            self.board = starting_board

        self.num_rounds = 0

    def play(self):
        while (self.board.winner is None and len(self.board.empty_cells) > 0):
            self.show_board()
            self.make_next_move() 
            self.current_player, self.next_player = \
                self.next_player, self.current_player
            self.num_rounds = self.num_rounds + 1
        self.show_board()
        
        if self.board.winner is None:
            print("It's a draw!")
            return -1
        else:
            print("Congratulations, {} won!".format(player_names[self.board.winner]))
            return self.board.winner
            

    def show_board(self):
        print(self.board)
        print("")

    def make_next_move(self):
        start = timeit.default_timer()
        move = self.current_player[1].next_move(deepcopy(self.board))
        end = timeit.default_timer()

        print(self.num_rounds, " ",end-start,file=self.results)

        assert move.player == self.current_player[0]
        assert self.board.cell(move.row, move.col) == CellState.EMPTY

        self.board.set_cell(move.player, move.row, move.col)
