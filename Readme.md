
# About

1. This is the accompanying git repo for the paper "Modeling Precomputation In Games Played Under Computational Constraints" appearing in IJCAI 2021, which includes the source code to replicate the experiments as well as the technical appendix.

# Getting Started Steps

1. Go to https://stockfishchess.org/, download the correct stockfish binary for the operating system, and save as sf.exe in this directory.

2. Install python library dependencies: python-chess, numpy, plotly.

# Experiments

1. Experiment 1 replicates the plots in Figure 1 of the paper (modulo specific parameter values; the general shape of the plots should be the same).

2. Note: numerical results can vary across runs and machines because of variable execution times of the stockfish engine.

# Customization

1. Experiment 1 allows changing parameters like precomputation penalty, time per move, randomness of strategy etc.

2. As described in the paper, some heuristic methods are used to conservatively estimate the value of the game if sigma_1 and sigma_2 play against each other from a certain state.
These heuristic parameters can be tweaked at the top of the file BoardValueEstimation. Alternatively, one can re-write the function score_final_boardpos to sample simulations of
sigma_1 playing against sigma_2 in order to compute this value more precisely. This will increase runtime (can be mitigated by caching results) but give more precise results as opposed to being a heuristic approximation.
Note this heuristic is not accurate when sigma_1 and sigma_2 have different relative strengths (e.g. one has more computation time than the other).

3. Each Player accepts a collection of parameters which can be used to customize the strategy behaviour:
    1. ms: the number of milliseconds used per move computation
    2. randomnessfactor: how randomly the player plays (see paper for precise definition)
    3. num_moves_considered: The player policy will only choose between the top num_moves_considered moves for each state. In the paper this is 2, but this value can be increased.


# License

1. GPL 3.0 License
