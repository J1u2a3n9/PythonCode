from copy import deepcopy
from numpy import inf
import timeit

from .base_agent import Agent, Move
from ..player import other_player


class AlphaBetaAgent(Agent):
    def __init__(self, player):
        super().__init__(player)
        self.u_table = {}
        self.h_table = {}
        self.states_visited = 0

    def next_move(self, board):
        start = timeit.default_timer()

        self.h_table = {}
        move = self.abminimax(board, max(9 - board.num_to_win, 3), self.player, -inf, inf)[0]
            
        end = timeit.default_timer()
        self.time += (end-start)
        self.num_moves += 1

        return move

    def abminimax(self, board, depth, player, alpha, beta):
        hash = board.hash
        if hash in self.u_table:
            return self.u_table[hash]

        self.states_visited += 1       
        valid_moves = self.valid_moves(board, player)

        #terminal cases
        if board.winner is not None:
            return -1, 1 if board.winner == self.player else -1, -1
        if len(valid_moves) == 0 or depth == 0:
            return -1, 0

        #default result that keeps track of the best so far
        if player == self.player:
            best_result = -1, -inf
        else:
            best_result = -1, inf

        #gets dictionary of moves and their heuristics, using a cache
        moves_dict = {}
        for move in valid_moves:
            board.set_cell(move.player, move.row, move.col)
            temp_hash = board.hash
            if temp_hash not in self.h_table:
                h = board.heuristic(player)
                self.h_table[temp_hash] = h
            moves_dict[move] = self.h_table[temp_hash]
            board.set_cell(-1, move.row, move.col)

        #sorts the dictionary in descending order. moves with the highest 
        #heuristic value come first
        sorted_valid_moves = sorted(moves_dict.items(), key = lambda i: i[1], reverse = True)
        
        #analyze each move
        for move, heuristic in sorted_valid_moves:
            board.set_cell(move.player, move.row, move.col)
            result = move, self.abminimax(board, depth-1, other_player(player), alpha, beta)[1]
            board.set_cell(-1, move.row, move.col)
            if player == self.player:
                best_result = max(best_result, result, key = lambda i: i[1])
                alpha = max(alpha, best_result[1])
                if alpha >= beta:
                    break
            else:
                best_result = min(best_result, result, key = lambda i: i[1])
                beta = min(beta, best_result[1])
                if alpha >= beta:
                    break
        
        self.u_table[hash] = best_result
        return best_result

    #overriden method from base_agent to account for player
    def valid_moves(self, board, player):
        valid_moves = []
        for i, j in board.empty_cells:
            valid_moves.append(Move(player, i, j))

        return valid_moves

   
