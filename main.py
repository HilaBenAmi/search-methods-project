import os.path
import sys
from time import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from IDAstar import IDAStarSolver
from AStar import AStarSolver
from NPuzzle import Board


def run_solver(solver, experiment_name):
    s_time = time()
    actual_cost = solver.solve()
    e_time = time()
    if actual_cost == 'NOT_FOUND':
        print(f"Board was not solved after {round(e_time - s_time, 6)} sec")
    nodes_counts = pd.Series(solver.history.values(), index=solver.history.keys())
    res_dict = {
        'experiment_name': experiment_name,
        'actual_cost': actual_cost,
        'elapsed_time': round(e_time - s_time, 6),
        'expanded_nodes': solver.nodes_expanded,
        'duplicate_visits': nodes_counts[nodes_counts > 1].sum(),
        'count_steps': len(solver.solution),
        'count_unique_nodes': len(nodes_counts)
    }
    for k, v in res_dict.items():
        print(k, v, sep=' = ')

    return res_dict


def run_solver_and_save_results(solver, board, seed, heuristic, dir_path, solver_name='Astar'):
    board.set_f(heuristic)
    print(f"Estimated cost = {heuristic} of initial board: {getattr(board, heuristic)}")
    res = run_solver(solver, experiment_name=f'{solver_name}_{heuristic}')
    df = pd.DataFrame(columns=res.keys())
    df.loc[seed] = res
    # df.to_csv(os.path.join(dir_path, f'{solver_name}_{seed}_{heuristic}.csv'))
    return df


def save_results_stats(all_res_df, found_res=True, ts=time()):
    if found_res:
        df = all_res_df[all_res_df['actual_cost'] != 'NOT_FOUND']
        df = df.astype({'actual_cost': int})
    else:
        df = all_res_df[all_res_df['actual_cost'] == 'NOT_FOUND']
    gb = df.groupby('experiment_name')
    mean_per_exp = gb.mean().add_prefix('mean_')
    std_per_exp = gb.std().add_prefix('std_')
    count_exp = gb.count().rename(columns={'actual_cost': 'count_exp'})[['count_exp']]
    stat_res = pd.concat([count_exp, mean_per_exp, std_per_exp], axis=1)
    stat_res.to_csv(f'stat_results_found={found_res}_{ts}.csv')
    return df


def evaluate_results(file_name):
    ts = time()
    df = pd.read_csv(f'./outputs/{file_name}.csv', index_col=0)

    found_df = save_results_stats(df, found_res=True, ts=ts)
    _ = save_results_stats(df, found_res=False, ts=ts)

    for col in df.columns:
        if col == 'experiment_name':
            continue
        sns.boxplot(data=found_df, y=col, x='experiment_name')
        plt.xticks(rotation=10)
        plt.savefig(f'./plots/{col}_boxplot.jpg')
        plt.close()


if __name__ == '__main__':
    ts = time()
    number_of_iterations = 101
    fld = 'outputs'
    results_per_exp = {
        'A_manhattan': [],
        'A_hamming': [],
        'IDA_manhattan': [],
        'IDA_hamming': []
    }
    results_list = []

    ## 1. 1-10, 2. 11-81, 3. 80-100
    for seed in range(80, number_of_iterations):
        print(f'Iteration no. {seed} with seed no. {seed}')
        np.random.seed(seed)

        board = Board(size=3)
        print(f'Board is: {board}')

        dir_path = os.path.join(fld)
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)

        print("\n##### A* - MANHATTAN #####")
        heuristic = 'manhattan'
        a_solver_manhattan = AStarSolver(board, heuristic)
        res_df = run_solver_and_save_results(a_solver_manhattan, board, seed, heuristic, dir_path, solver_name='Astar')
        results_per_exp['A_manhattan'].append(res_df)
        results_list.append(res_df)
        # all_res = pd.concat(results_per_exp['A_manhattan'])
        # all_res.to_csv(f'./outputs/a_manhattan_all_res_{ts}.csv')

        print("\n##### A* - HAMMING #####")
        heuristic = 'hamming'
        a_solver_hamming = AStarSolver(board, heuristic)
        res_df = run_solver_and_save_results(a_solver_hamming, board, seed, heuristic, dir_path, solver_name='Astar')
        results_per_exp['A_hamming'].append(res_df)
        results_list.append(res_df)
        # all_res = pd.concat(results_per_exp['A_hamming'])
        # all_res.to_csv(f'./outputs/a_hamming_all_res_{ts}.csv')

        print("\n##### IDA* - MANHATTAN #####")
        heuristic = 'manhattan'
        ida_solver_manhattan = IDAStarSolver(board, heuristic)
        res_df = run_solver_and_save_results(ida_solver_manhattan, board, seed, heuristic, dir_path, solver_name='IDAstar')
        results_per_exp['IDA_manhattan'].append(res_df)
        results_list.append(res_df)
        # all_res = pd.concat(results_per_exp['IDA_manhattan'])
        # all_res.to_csv(f'./outputs/ids_manhattan_all_res_{ts}.csv')

        print("\n##### IDA* - HAMMING #####")
        heuristic = 'hamming'
        ida_solver_hamming = IDAStarSolver(board, heuristic)
        res_df = run_solver_and_save_results(ida_solver_hamming, board, seed, heuristic, dir_path, solver_name='IDAstar')
        results_per_exp['IDA_hamming'].append(res_df)
        results_list.append(res_df)
        # all_res = pd.concat(results_per_exp['IDA_hamming'])
        # all_res.to_csv(f'./outputs/ida_hamming_all_res_{ts}.csv')

        all_res = pd.concat(results_list)
        all_res.to_csv(f'./outputs/all_res_{ts}.csv')


    evaluate_results(f'all_res_{ts}')
