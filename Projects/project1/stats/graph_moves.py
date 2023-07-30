import matplotlib.pyplot as plt

# Read data from file
bfs_stats = open("bfs_stats.txt").readlines()
dfs_stats = open("dfs_stats.txt").readlines()
ifs_stats = open("ifs_stats.txt").readlines()
greedy_stats = open("greedy_stats.txt").readlines()
a_star_stats = open("a_star_stats.txt").readlines()

bfs_stats = [x.split(";") for x in bfs_stats]
dfs_stats = [x.split(";") for x in dfs_stats]
ifs_stats = [x.split(";") for x in ifs_stats]
greedy_stats = [x.split(";") for x in greedy_stats]
a_star_stats = [x.split(";") for x in a_star_stats]

# Convert data to float
bfs_moves = float(bfs_stats[0][1])
dfs_moves = float(dfs_stats[0][1])
ifs_moves = float(ifs_stats[0][1])
greedy_moves = float(greedy_stats[0][1])
a_star_moves = float(a_star_stats[0][1])

# Create graph
fig, ax = plt.subplots()
ax.bar(1, bfs_moves, label='BFS')
ax.bar(2, dfs_moves, label='DFS')
ax.bar(3, ifs_moves, label='IFS')
ax.bar(4, greedy_moves, label='GREEDY')
ax.bar(5, a_star_moves, label='A*')
ax.legend()
ax.set_xlabel('Algorithms')
ax.set_ylabel('Moves')
ax.set_title('Number of moves for each algorithm')
plt.show()