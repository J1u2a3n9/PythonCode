from copy import deepcopy
import timeit

from .base_agent import Agent, Move
from ..player import other_player


class DFSAgent(Agent):
    def __init__(self, player):
        super().__init__(player)
        self.states_visited = 0

    def next_move(self, board):
        start = timeit.default_timer()

        valid_moves = super().valid_moves(board)

        #dictionary that pairs each move with its utility: e.g. {Move: 1}
        move_results = {}

        #main loop for the initial state
        for move in valid_moves:
            move_results[move] = self.minimax(board, move, self.player)
            
        end = timeit.default_timer()
        self._time += (end-start)
        self._num_moves += 1

        #gets the dictionary entry with the highest value. As some
        #moves might share the utility of 1, max returns the first
        #key that has the highest value. In a blank board, this is 0,0
        return max(move_results, key=move_results.get)


    def minimax(self, board, move, player):
        #creates a copy of the board and makes the move 
        new_board = deepcopy(board)
        new_board.set_celda(move.player, move.row, move.col)
        self.states_visited += 1

        #swap players
        player = other_player(player)

        valid_moves = self.valid_moves(new_board, player)

        #Check if state is terminal and return utility if it is
        if(new_board.winner is not None):
            return 1 if new_board.winner == self.player else -1
        if(valid_moves is None or len(valid_moves) == 0):
            return 0

        move_results = {}

        for move in valid_moves:
            move_results[move] = self.minimax(new_board, move, player)

        #if player is the agent, get the max
        if player == self.player:
            return max(move_results.values())
        
        #else get the min
        return min(move_results.values())

    #overriden method from base_agent to account for player
    def valid_moves(self, board, player):
        valid_moves = []
        for i, j in board.empty_cells:
            valid_moves.append(Move(player, i, j))

        return valid_moves
        