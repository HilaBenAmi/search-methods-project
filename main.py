import os.path
import sys
from time import time

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

from IDAstar import IDAStarSolver
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



if __name__ == '__main__':
    # _, seed, fld = sys.argv
    seed = 1
    fld = 'outputs'
    seed = int(seed)
    np.random.seed(seed)

    board = Board(size=3)
    print(f'Board is: {board}')

    print("\n##### IDA* - MANHATTAN #####")
    heuristic = 'manhattan'
    board.set_f(heuristic)
    print(f"Estimated cost = {heuristic} of initial board: {getattr(board, heuristic)}")
    ida_solver = IDAStarSolver(board, heuristic)
    ida_res = run_solver(ida_solver)

    df = pd.DataFrame(columns=ida_res.keys())
    df.loc[seed] = ida_res
    df.to_csv(os.path.join(fld, f'ida_{seed}_{heuristic}.csv'))

    print("\n##### IDA* - HAMMING #####")
    heuristic = 'hamming'
    board.set_f(heuristic)
    print(f"Estimated cost = {heuristic} of initial board: {getattr(board, heuristic)}")
    ida_solver = IDAStarSolver(board, heuristic)
    ida_res = run_solver(ida_solver)

    df = pd.DataFrame(columns=ida_res.keys())
    df.loc[seed] = ida_res
    df.to_csv(os.path.join(fld, f'ida_{seed}_{heuristic}.csv'))
