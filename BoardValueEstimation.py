MAX_NUMBER_OF_MOVES_TILL_GAME_ENDS = 100 #if the game finishes this number of halfmoves without a result, then the game is declared a draw
CP_THRESH = 400#if any player gains more than this advantage, we assume that they would win if the base policies were played against each other
INTERPOLATE_VALUE_ESTIMATE = True #if true, then use a linear interpolation to guess the value of the board state if sigma_1 were to play against sigma_2. Otherwise, a hard threshold rule is used (where positions which do not reach the threshold are scored as 0.5).

from Player import *

#the evaluators used to compute the cp score
board_evaluator_white = Player(50,"white",0.000000001,"evaluator",2)
board_evaluator_black = Player(50,"black",0.000000001,"evaluator",2)

def score_final_boardpos(player,boardstate):
    '''
    :param player: player whose perspective we are scoring from.
    :param boardstate: current board state
    :return: the value of the game if sigma_1,sigma_2 played against each other from this position (float), whether the game has finished (bool). The value should be from the perspective of player.
    We use some conservative approximations (described in the paper) to avoid having to simulate the entire game to estimate the value (however this is still tractable to do).
    '''

    if len(boardstate.move_stack) > MAX_NUMBER_OF_MOVES_TILL_GAME_ENDS:
        return 0.5, True #max num moves done

    if boardstate.is_game_over(): #game has finished
        score = boardstate.result().split("-")
        if len(score[0])>1:
            return 0.5, True#draw
        if player.color == "white":
            return int(score[0]), True
        elif player.color == "black":
            return int(score[1]), True

    #game has not finished, see if cp thresh is exceeded

    #get cp score from player's perspective
    current_evaluator = board_evaluator_white
    if board_evaluator_black.is_turn(boardstate):
        current_evaluator = board_evaluator_black
    cpest = current_evaluator.get_cp_estimate(boardstate)
    #flip evaluation so from player perspective
    if not player.is_turn(boardstate):
        cpest = -cpest
    if INTERPOLATE_VALUE_ESTIMATE:
        #linearly interpolate a value estimate
        val_estimate = (cpest/CP_THRESH+1)/2
        if val_estimate >1:
            val_estimate = 1
        if val_estimate < 0:
            val_estimate = 0
        return val_estimate,False
    else:
        if cpest >= CP_THRESH:
            return 1, False
        if cpest <= -CP_THRESH:
            return 0, False
        return 0.5, False #no decisive winner, assume draw

