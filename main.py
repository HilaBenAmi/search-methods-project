import os.path
import sys
import time

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

from IDAstar import IDAStarSolver
from NPuzzle import Board


## TODO - need to refactor later.. this is from Saar
def run_solver(solver):
    start = time.time()
    actual_cost = solver.solve()
    end = time.time()
    elapsed_time = end - start
    sr = pd.Series(solver.history.values(), index=solver.history.keys())
    desc = sr.describe()
    res_dict = {
        'Actual Cost': actual_cost,
        'Elapsed Time': elapsed_time,
        'Expanded Nodes': solver.nodes_expanded,
        'Duplicate Visits': sr[(sr > 1)].sum(),
        **{f'{f_n} Visits'.title(): val for f_n, val in desc.items()}
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
    print(f"Estimated cost = {board.manhattan}")

    print("\n##### IDA* - MANHATTAN #####")
    heuristic = 'manhattan'
    board.set_f(heuristic)
    ida_solver = IDAStarSolver(board, heuristic)
    ida_res = run_solver(ida_solver)

    df = pd.DataFrame(columns=ida_res.keys())
    df.loc[seed] = ida_res
    df.to_csv(os.path.join(fld, f'ida_{seed}_{heuristic}.csv'))

    print("\n##### IDA* - HAMMING #####")
    heuristic = 'hamming'
    board.set_f(heuristic)
    ida_solver = IDAStarSolver(board, heuristic)
    ida_res = run_solver(ida_solver)

    df = pd.DataFrame(columns=ida_res.keys())
    df.loc[seed] = ida_res
    df.to_csv(os.path.join(fld, f'ida_{seed}_{heuristic}.csv'))
