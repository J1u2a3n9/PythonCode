from abc import ABC, abstractmethod
from collections import namedtuple

from ..board import *
from ..player import player_names


class Move(namedtuple("Move", ["player", "row", "col"])):
    def __repr__(self):
        return "Move(player={},row={},col={})".format(
            player_names[self.player], self.row, self.col)


class Agent(ABC):

    def __init__(self, player):
        self.player = player
        self.num_moves = 0
        self.time = 0
        self.states_visited = 0

    @abstractmethod
    def next_move(self, board):
        pass

    def valid_moves(self, board):
        valid_moves = []
        for i, j in board.empty_cells:
            valid_moves.append(Move(self.player, i, j))

        return valid_moves

    @property
    def average_runtime(self):
        if self.num_moves == 0:
            return 0

        return self.time / self.num_moves

    @property
    def states_visited(self):
        return self.states_visited
