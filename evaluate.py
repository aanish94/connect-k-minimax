import csv
import matplotlib.pyplot as plt
import os

from main import Game
from player import MiniMax


PLAYER1_PIECE = 1
PLAYER2_PIECE = 2

use_pruning = True

player1 = MiniMax(
    PLAYER1_PIECE,
    PLAYER2_PIECE,
    max_player=True,
    alpha_beta_pruning=use_pruning,
    use_heuristic=False,
)

player2 = MiniMax(
    PLAYER2_PIECE,
    PLAYER1_PIECE,
    max_player=False,
    alpha_beta_pruning=use_pruning,
    use_heuristic=False,
)

all_times = []
all_move_counts = []

for m in range(3, 5):
    for n in range(3, 5):
        for k in range(3, 5):
            if k > m or k > n:
                continue
            game = Game(player1, player2, m=m, n=n, k=k)
            _, execution_times, move_counts = game.play(quiet=True, record_stats=True)
            all_times.append([(m, n, k), execution_times])
            all_move_counts.append([(m, n, k), move_counts])

output_folder = 'results'
if not os.path.exists(output_folder):
    os.mkdir(output_folder)
results = []

# Plot times
plt.figure(figsize=(12, 9))
for cur_entry in all_times:
    params, cur_time_arr = cur_entry
    m, n, k = params
    results.append([m, n, k, cur_time_arr[0]])
    label_str = f"m: {m}, n: {n}, k: {k}"
    plt.plot(cur_time_arr, label=label_str)
plt.xlabel('Turn #')
plt.ylabel('Time (s)')
plt.title('MiniMax Execution Times')
plt.legend()
plt.grid()
plt.tight_layout()
plt.savefig(f'{output_folder}/times.png')

# Plot visited states
plt.figure(figsize=(12, 9))
for idx, cur_entry in enumerate(all_move_counts):
    params, cur_move_arr = cur_entry
    m, n, k = params
    results[idx].append(cur_move_arr[0])
    label_str = f"m: {m}, n: {n}, k: {k}"
    plt.plot(cur_move_arr, label=label_str)
plt.xlabel('Turn #')
plt.ylabel('# of Visited States')
plt.title('MiniMax State Counts')
plt.legend()
plt.grid()
plt.tight_layout()
plt.savefig(f'{output_folder}/states.png')

# Output CSV with data
with open(f'{output_folder}/results.csv', mode='w') as file:
    writer = csv.writer(file)
    writer.writerow(['m', 'n', 'k', 'Time', 'States'])
    for row in results:
        writer.writerow(row)
