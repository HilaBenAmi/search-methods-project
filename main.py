import os.path
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


def save_results_stats(all_res_df, found_res, ts=time()):
    if found_res == 'all':
        df = all_res_df.drop(columns=['actual_cost'])
    elif found_res is True:
        df = all_res_df[all_res_df['actual_cost'] != 'NOT_FOUND']
        df = df.astype({'actual_cost': int})
    else:
        df = all_res_df[all_res_df['actual_cost'] == 'NOT_FOUND']
    gb = df.groupby('experiment_name')
    mean_per_exp = gb.mean().add_prefix('mean_')
    std_per_exp = gb.std().add_prefix('std_')
    if found_res != 'all':
        count_exp = gb.count().rename(columns={'actual_cost': 'count_exp'})[['count_exp']]
        stat_res = pd.concat([count_exp, mean_per_exp, std_per_exp], axis=1)
    else:
        stat_res = pd.concat([mean_per_exp, std_per_exp], axis=1)
    stat_res.to_csv(f'stat_results_found={found_res}_{ts}.csv')
    return df


def evaluate_results(file_name_list):
    ts = time()
    dfs_list = []
    for file_name in file_name_list:
        df = pd.read_csv(f'./outputs/{file_name}.csv', index_col=0)
        if 'ida' in file_name:
            df = df[(df['experiment_name'] == 'IDAstar_manhattan') | (df['experiment_name'] == 'IDAstar_hamming')]
        dfs_list.append(df)
    df = pd.concat(dfs_list)

    found_df = save_results_stats(df, found_res=True, ts=ts)
    _ = save_results_stats(df, found_res=False, ts=ts)
    _ = save_results_stats(df, found_res='all', ts=ts)

    # found_df = df[df['experiment_name'] != 'IDAstar_hamming']
    # found_df = found_df.astype({'actual_cost': int})
    for col in found_df.columns:
        print(col)
        if col == 'experiment_name':
            continue
        sns.boxplot(data=found_df, y=col, x='experiment_name')
        plt.xticks(rotation=10)
        plt.savefig(f'./plots/without_ida_hamming/{col}_boxplot.jpg')
        plt.close()


if __name__ == '__main__':
    # files_list = [
    #     'all_res_1677527959.1735578-1-10-ida',
    #     'all_res_1677564499.3073084-10-80-ida',
    #     'all_res_1677615685.689554-astar1-80',
    #     'all_res_1677616098.3077073'
    # ]
    # evaluate_results(files_list)


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

    for seed in range(1, number_of_iterations):
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

        print("\n##### A* - HAMMING #####")
        heuristic = 'hamming'
        a_solver_hamming = AStarSolver(board, heuristic)
        res_df = run_solver_and_save_results(a_solver_hamming, board, seed, heuristic, dir_path, solver_name='Astar')
        results_per_exp['A_hamming'].append(res_df)
        results_list.append(res_df)

        print("\n##### IDA* - MANHATTAN #####")
        heuristic = 'manhattan'
        ida_solver_manhattan = IDAStarSolver(board, heuristic)
        res_df = run_solver_and_save_results(ida_solver_manhattan, board, seed, heuristic, dir_path, solver_name='IDAstar')
        results_per_exp['IDA_manhattan'].append(res_df)
        results_list.append(res_df)

        print("\n##### IDA* - HAMMING #####")
        heuristic = 'hamming'
        ida_solver_hamming = IDAStarSolver(board, heuristic)
        res_df = run_solver_and_save_results(ida_solver_hamming, board, seed, heuristic, dir_path, solver_name='IDAstar')
        results_per_exp['IDA_hamming'].append(res_df)
        results_list.append(res_df)

        all_res = pd.concat(results_list)
        all_res.to_csv(f'./outputs/all_res_{ts}.csv')
    # evaluate_results(files_list)
