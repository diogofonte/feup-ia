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
bfs_time = float(bfs_stats[0][0])
dfs_time = float(dfs_stats[0][0])
ifs_time = float(ifs_stats[0][0])
greedy_time = float(greedy_stats[0][0])
a_star_time = float(a_star_stats[0][0])

# Create graph
fig, ax = plt.subplots()
ax.bar(1, bfs_time, label='BFS')
ax.bar(2, dfs_time, label='DFS')
ax.bar(3, ifs_time, label='IFS')
ax.bar(4, greedy_time, label='GREEDY')
ax.bar(5, a_star_time, label='A*')
ax.legend()
ax.set_xlabel('Algorithms')
ax.set_ylabel('Time (seconds)')
ax.set_title('Time of execution for each algorithm')
plt.show()