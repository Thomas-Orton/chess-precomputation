from pystockfishlocal import *
import numpy as np


mainEngine = Engine()
#####

##### utils

def softmax(x, coeff):
    vals = np.asarray(x)
    mx = np.max(vals)
    vals -= mx
    scoreMatExp = np.exp(coeff* np.asarray(vals))
    return scoreMatExp / scoreMatExp.sum(0)
##

class Player:
    def __init__(self, ms, color, randomnessfactor, playername, num_moves_considered):
        self.assignedDistributions = {}
        self.assignedCPs = {}
        self.ms = ms
        self.color = color
        self.randomnessfactor = randomnessfactor
        self.playername = playername
        self.num_moves_considered = num_moves_considered

    def get_string_id(self):
        return self.playername + "|"+self.color+"|"+str(self.randomnessfactor)

    def get_move_distribution(self, board):
        '''
        returns a distribution over moves; caches choices to improve speed.
        '''
        assert (self.is_turn(board))
        fen = board.fen()
        if fen in self.assignedDistributions:
            return self.assignedDistributions[fen]
        else:
            if(fen) in self.assignedCPs:
                moves, values = self.assignedCPs[fen]
            else:
                mainEngine.clear_hash() #essential to ensure calculations for different players don't interfere, since they're all done on one stockfish instance
                mainEngine.set_fen_position(fen)
                moves, values = mainEngine.get_best_moves(k=self.num_moves_considered, mspermove = self.ms)
                self.assignedCPs[fen] = [moves, values]
            if(len(moves) > 0):
                distribution = softmax(values, 1 / self.randomnessfactor)
            else:
                distribution = []
            self.assignedDistributions[fen] = [moves, distribution]
            return [moves,distribution]

    def get_cp_estimate(self,board):
        '''
        gets cp estimate of board state relative to player.
        '''
        assert(self.is_turn(board))
        self.get_move_distribution(board)
        moves, cps = self.assignedCPs[board.fen()]
        if len(cps) > 0:
            mx = np.max(cps)
            return mx
        return None

    def is_turn(self, board):
        '''
        :return: True if player's turn to move.
        '''
        if (self.color == "white" and board.turn == True) or (self.color == "black" and board.turn == False):
            return True
        return False

    def set_randomness(self,r):
        self.randomnessfactor = r
        self.assignedDistributions = {}

    def set_ms(self,ms):
        self.ms = ms
        self.assignedDistributions = {}
        self.assignedCPs = {}



###########

