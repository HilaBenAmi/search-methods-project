import os.path
import sys
from time import time

import matplotlib.pyplot as plt
# import seaborn as sns
import numpy as np
import pandas as pd

from IDAstar import IDAStarSolver
from AStar import AStarSolver
from NPuzzle import Board


## TODO - need to refactor later.. this is from Saar
def run_solver(solver):
    s_time = time()
    actual_cost = solver.solve()
    e_time = time()
    nodes_counts = pd.Series(solver.history.values(), index=solver.history.keys())
    desc = nodes_counts.describe()
    res_dict = {
        'Actual Cost': actual_cost,
        'Elapsed Time': round(e_time - s_time, 6),
        'Expanded Nodes': solver.nodes_expanded,
        'Duplicate Visits': nodes_counts[nodes_counts > 1].sum(),
        **{f'{percentile} Visits'.title(): val for percentile, val in desc.items()}
    }
    for k, v in res_dict.items():
        print(k, v, sep=' = ')

    return res_dict


def run_solver_and_save_results(solver, board, seed, heuristic, dir_path, solver_name='Astar'):
    board.set_f(heuristic)
    print(f"Estimated cost = {heuristic} of initial board: {getattr(board, heuristic)}")
    res = run_solver(solver)
    df = pd.DataFrame(columns=res.keys())
    df.loc[seed] = res
    df.to_csv(os.path.join(dir_path, f'{solver_name}_{seed}_{heuristic}.csv'))


if __name__ == '__main__':
    seed = 1
    fld = 'outputs'
    seed = int(seed)
    np.random.seed(seed)

    board = Board(size=3)
    print(f'Board is: {board}')

    dir_path = os.path.join(fld)
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)

    print("\n##### A* - MANHATTAN #####")
    heuristic = 'manhattan'
    a_solver_manhattan = AStarSolver(board, heuristic)
    run_solver_and_save_results(a_solver_manhattan, board, seed, heuristic, dir_path, solver_name='Astar')

    print("\n##### A* - HAMMING #####")
    heuristic = 'hamming'
    a_solver_hamming = AStarSolver(board, heuristic)
    run_solver_and_save_results(a_solver_hamming, board, seed, heuristic, dir_path, solver_name='Astar')

    print("\n##### IDA* - MANHATTAN #####")
    heuristic = 'manhattan'
    ida_solver_manhattan = IDAStarSolver(board, heuristic)
    run_solver_and_save_results(ida_solver_manhattan, board, seed, heuristic, dir_path, solver_name='IDAstar')

    print("\n##### IDA* - HAMMING #####")
    heuristic = 'hamming'
    ida_solver_hamming = IDAStarSolver(board, heuristic)
    run_solver_and_save_results(ida_solver_hamming, board, seed, heuristic, dir_path, solver_name='IDAstar')
