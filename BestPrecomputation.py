
from BoardValueEstimation import *

def get_moving_player(p1,p2,board):
    '''

    :param p1: Player 1
    :param p2: Player 2
    :param board: board object
    :return: the player whose current turn it is to  move.
    '''
    if p1.isturn(board):
        return p1
    return p2


def get_best_precompval(pre,player,opposition, boardstate, lambda_penalty):
    '''
    :param pre: strong precomputed strategy
    :param player: precomputing player
    :param opposition: opposing player
    :param boardstate: current board state
    :param lambda_penalty: precomputing penalty term
    :return: value of best precomputation strategy for player starting from board state boardstate, set containing precomputed positions.
    '''
    precompstatechoices = {}
    val = get_best_precompval_recursively(pre,player,opposition, boardstate, 1, lambda_penalty ,precompstatechoices)
    precompset = reconstruct_precomp(pre,player,opposition,boardstate,precompstatechoices)
    return val, precompset


def get_best_precompval_recursively(pre,player,opposition, boardstate, currentprob, lambda_penalty, precompstatechoices):
    '''

    :param pre: strong precomputed strategy
    :param player: precomputing player
    :param opposition: opposing player
    :param boardstate: current board state
    :param currentprob: probability of current history
    :param lambda_penalty: precomputing penalty term
    :param precompstatechoices: set maintaining states which should be precomputed for recursive subproblems
    :return:
    '''
    end_value, game_finished = score_final_boardpos(player, boardstate)
    if currentprob < lambda_penalty:
        #lambda cutoff, no point in memorizing
        return currentprob*end_value

    if game_finished:#game has ended
        return currentprob * end_value

    noprecomp_val = currentprob * end_value #the value if we stopped precomputing at this point
    precomp_val = 0 #initialize the value if we continue to precomp.

    movingplayer = None
    #determine who moving player is
    if player.is_turn(boardstate):
        movingplayer=pre
        precomp_val = -lambda_penalty # Cost of memorizing this history.
    else:
        movingplayer=opposition
    moves, probs = movingplayer.get_move_distribution(boardstate)
    #branch out across possible moves
    for i in range(len(moves)):
        move = moves[i]
        prob = probs[i]
        boardstate.push(move)
        #add value from each branch to precomp_val
        precomp_val += get_best_precompval_recursively(pre,player,opposition, boardstate, currentprob* prob, lambda_penalty, precompstatechoices)
        boardstate.pop()
    if player.is_turn(boardstate):
        if precomp_val > noprecomp_val:
            #if better to precomp here, then add state to precomp set
            precompstatechoices[boardstate.fen()] = True
    return max(precomp_val,noprecomp_val)

#if(player.isturn((boardstate))):
    #    #if player's turn, calculate value if we stopped precomputing here
    #    noprecomp_val = currentprob*end_value
    #else:
    #    #if not player's turn, give a dummy value to force recursion to next level
    #    noprecomp_val = -100000000

def reconstruct_precomp(pre,player,opposition,boardstate,precompstatechoices):
    '''

    :param pre: strong precomputed strategy
    :param player: precomputing player
    :param opposition: opposing player
    :param boardstate: starting board state
    :param precompstatechoices: set maintaining states which should be precomputed for recursive subproblems
    :return: a set containing precomputed states for a precomputation strategy which starts at boardstate
    '''
    ret = {}
    reconstruct_precomp_recursively(pre,player,opposition,boardstate,precompstatechoices,ret)
    return ret

def reconstruct_precomp_recursively(pre,player,opposition,boardstate,precompstatechoices,ret):
    '''

     :param pre: strong precomputed strategy
    :param player: precomputing player
    :param opposition: opposing player
    :param boardstate: current board state
    :param precompstatechoices: set maintaining states which should be precomputed for recursive subproblems
    :param ret: set maintaining precomputed states
    :return: a set consisting of all precomputed states for the strategy starting at boardstate
    '''
    if player.is_turn(boardstate):
        movingplayer=pre
        if(boardstate.fen() in precompstatechoices):
            ret[boardstate.fen()] = True
        else:
            return
    else:
        movingplayer=opposition
    moves, probs = movingplayer.get_move_distribution(boardstate)
    for i in range(len(moves)):
        move = moves[i]
        boardstate.push(move)
        reconstruct_precomp_recursively(pre,player,opposition,boardstate,precompstatechoices,ret)
        boardstate.pop()

