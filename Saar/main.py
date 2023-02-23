import os.path
import sys
import time

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

from IDAstar import IDAStarSolver

from NPuzzle import Board
from RBFS import RBFSSolver


# Give a Solver, run it and export its statistics
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
    if len(sys.argv) != 3:
        print('Usage: [Seed] [Save_Directory]')

    else:
        _, seed, fld = sys.argv
        seed = int(seed)
        np.random.seed(seed)

        sample = Board(size=3)
        print(f'Board is: {sample}')
        print(f"Estimated cost = {sample.manhattan}")

        fig, axs = plt.subplots(ncols=2, figsize=(20, 12), sharey=True)
        for ax in axs:
            ax.set_yscale('log')

        fig.suptitle('Comparing states visits', fontsize=24)

        print("\n##### IDA* - MANHATTAN #####")
        ida_solver = IDAStarSolver(sample, heuristic='manhattan')
        res = run_solver(ida_solver)

        df = pd.DataFrame(columns=res.keys())
        df.loc[seed] = res
        df.to_csv(os.path.join(fld, f'ida_{seed}.csv'))

        axs[1].plot(ida_solver.history.keys(), ida_solver.history.values())
        axs[1].tick_params(
            axis='x',
            which='both',
            bottom=False,
            labelbottom=False)
        axs[1].set_xlabel(f"{int(res['Count Visits'])} unique states", fontsize=16)
        axs[1].set_ylabel('Visits Count', fontsize=16)
        axs[1].set_title('IDA*', fontsize=20)
        axs[1].axhline(res['Mean Visits'], color='r', linestyle=':')

        print("\n##### RBFS - MANHATTAN #####")
        rbfs_solver = RBFSSolver(sample, heuristic='manhattan')
        rbfs_res = run_solver(rbfs_solver)

        df = pd.DataFrame(columns=rbfs_res.keys())
        df.loc[seed] = rbfs_res
        df.to_csv(os.path.join(fld, f'rbfs_{seed}.csv'))

        axs[0].plot(rbfs_solver.history.keys(), rbfs_solver.history.values())
        axs[0].tick_params(
            axis='x',
            which='both',
            bottom=False,
            labelbottom=False)
        axs[0].set_xlabel(f"{int(rbfs_res['Count Visits'])} unique states", fontsize=16)
        axs[0].set_ylabel('Visits Count', fontsize=16)
        axs[0].set_title('RBFS', fontsize=20)
        axs[0].axhline(rbfs_res['Mean Visits'], color='r', linestyle=':')

        plt.savefig(os.path.join(fld, f'{seed}.png'))

        df = pd.DataFrame({'Visits': list(ida_solver.history.values()) + list(rbfs_solver.history.values()),
                           'Algorithm': ['IDA*'] * len(ida_solver.history) + ['RBFS'] * len(rbfs_solver.history)})
        sns.displot(data=df, x='Visits', hue='Algorithm', stat='probability',
                    log_scale=True, bins=range(6),
                    multiple='dodge', element='bars',
                    common_norm=False)
        plt.savefig(os.path.join(fld, f'{seed}_hist.png'))
