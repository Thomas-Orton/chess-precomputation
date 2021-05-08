
import time
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from BestPrecomputation import *

''''
This code runs the experiment in the paper (modulo the specific randomness parameters and precomputation penalty term): For each randomness parameter r, fix an opponent with randomness r, and compute the best precomputation strategy against the opposition.
The size of the best precomputation set, and the value of the precomputation strategy from the perspective of the precomputation player ignoring the precomputation penalty (more positive is better)
is plotted against log(randomness factor).

Plots are saved in the results folder, and are updated every time a new datapoint is computed. 

The relative strength of each player (time per move), randomness parameters, and precomputation penalty can be changed in the code.
'''

def make_experiment_plots(precomputation_oracle,precomputing_player,opposition_player,lambda_penalty,result_name):
    #initialize all oracles to play with low randomness
    precomputing_player.set_randomness(0.000001)
    opposition_player.set_randomness(0.000001)
    precomputation_oracle.set_randomness(0.000001)
    #populate the randomness values we want to test
    randomness_factors = [0.1]
    while randomness_factors[-1] < 1000:
        randomness_factors.append(randomness_factors[-1] * 2)
    x_axis = []
    precomp_size = []
    precomp_val = []
    for r in randomness_factors:
        #set the opposition player randomness
        opposition_player.set_randomness(r)
        print("computing for opposing player randomness factor=", r)
        t = time.time()
        #get best precomputation value, and best precomputation set
        val, precompset = get_best_precompval(precomputation_oracle, precomputing_player, opposition_player, chess.Board(), lambda_penalty)
        print("-----------------finished in time:", time.time() - t)
        print('net strategy value excluding precomputation penalty',val + lambda_penalty * len(precompset))
        print('precomputation set size',len(precompset))
        x_axis.append(np.log10(r))
        precomp_size.append(len(precompset))
        # compute precomputation value ignoring lambda penalty
        precomp_val.append(val + lambda_penalty * len(precompset))
        # save data
        np.savetxt('Results/'+result_name+'.txt', (x_axis, precomp_val, precomp_size), delimiter=',')
        #make plot
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(
            go.Scatter(x=x_axis, y=precomp_val, name="precomputation value"),
            secondary_y=False,
        )

        fig.add_trace(
            go.Scatter(x=x_axis, y=precomp_size, name="precomputation set size"),
            secondary_y=True,
        )

        # Add figure title
        fig.update_layout(
            title_text="Precomputation Strength as a Function of Randomization"
        )

        # Set x-axis title
        fig.update_xaxes(title_text="log10(randomness)")

        fig.write_html('Results/'+result_name+".html",auto_open = False)



# Experiment 1: white as precomputing player

#initialize players: white and black as stockfish with 10ms per move and randomness factor close to 0
#strong precomputation strategy with 50ms per move, randomnessfactor close to 0
p1 = Player(ms = 10, color = "white", randomnessfactor = 0.000001, playername="whitesigma", num_moves_considered=2)
p2 = Player(ms = 10, color = "black", randomnessfactor = 0.000001, playername="blacksigma", num_moves_considered=2)
pre_white = Player(ms = 50, color = "white", randomnessfactor = 0.000001, playername="presigma", num_moves_considered=2)
pre_black = Player(ms = 50, color = "black", randomnessfactor = 0.000001, playername="presigma", num_moves_considered=2)
lambda_penalty = 0.0001
make_experiment_plots(pre_white,p1,p2,lambda_penalty,'Experiment1_white_precomputing_against_randomizing_black')
make_experiment_plots(pre_black,p2,p1,lambda_penalty,'Experiment1_black_precomputing_against_randomizing_white')
