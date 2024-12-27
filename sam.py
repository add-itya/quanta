def can_finish(n, m, levels, prerequisites):
    graph = {level: [] for level in levels}
    indegree = {level: 0 for level in levels}
    
    for u, v in prerequisites:
        graph[u].append(v)
        indegree[v] += 1
    
    queue = [lvl for lvl in levels if indegree[lvl] == 0]
    
    visited_count = 0
    while queue:
        node = queue.pop()
        visited_count += 1
        for nei in graph[node]:
            indegree[nei] -= 1
            if indegree[nei] == 0:
                queue.append(nei)
    
    return visited_count == n

first_line = input().strip()
N, M = first_line.split()
N, M = int(N), int(M)

levels_line = input().strip()
levels = levels_line.split()

prerequisites = []
for _ in range(M):
    line = input().strip().split()
    u, v = line[0], line[1]
    prerequisites.append((u, v))

if can_finish(N, M, levels, prerequisites):
    print("true")
else:
    print("false")
