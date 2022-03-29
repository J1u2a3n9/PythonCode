import random
import timeit

from .base_agent import Agent


class RandomAgent(Agent):
    def __init__(self, player):
        super().__init__(player)
        self.states_visited = 0

    def next_move(self, board):
        start = timeit.default_timer()
        
        valid_moves = self.valid_moves(board)
        move = random.choice(valid_moves)
        
        end = timeit.default_timer()

        self.time += (end-start)
        self.num_moves += 1
        return move
