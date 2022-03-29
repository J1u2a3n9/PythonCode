from .base_agent import Agent, Move
from ..player import player_names

import timeit


class ConsoleInputAgent(Agent):
    def __init__(self, player):
        super().__init__(player)

    def next_move(self, board):
        def input_move():
            try:
                print("")
                print("{}'s next move".format(player_names[self.player]))
                row = int(input("\trow: "))
                col = int(input("\tcol: "))
                print("")

                return Move(self.player, row, col)
            except ValueError:
                print("Row an col must be integers between 0 and {}".format(
                    board.size))

        start = timeit.default_timer()
        move = input_move()
        valid_moves = self.valid_moves(board)

        while move not in valid_moves:
            print("{} is not valid, try again.".format(move))
            print("Valid moves: " + str(valid_moves))
            move = input_move()

        end = timeit.default_timer()
        
        self._time += (end-start)
        self._num_moves += 1

        return move
