def solve():
    line = input().strip()
    while not line:
        line = input().strip()
    N, M = map(int, line.split())
    
    words = []
    for _ in range(N):
        w = input().strip()
        words.append(w)
    queries = []
    maxQuery = 0
    for _q in range(M):
        q = int(input().strip())
        queries.append(q)
        if q > maxQuery:
            maxQuery = q

    words.sort()
    
    def lcp(a, b):
        length = min(len(a), len(b))
        cnt = 0
        for x, y in zip(a, b):
            if x == y:
                cnt += 1
            else:
                break
        return cnt
    
    LCP = [0]*(N)
    for i in range(1, N):
        LCP[i] = lcp(words[i], words[i-1])
    
    max_word_length = max(len(w) for w in words) if words else 0
    max_query = max(queries) if queries else 0
    max_len = max(max_word_length, max_query)
    if max_len == 0:
        for _ in queries:
            print(-1)
        return

    parent = list(range(N))
    size = [1]*N

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        a = find(a)
        b = find(b)
        if a != b:
            if size[a] < size[b]:
                a, b = b, a
            parent[b] = a
            size[a] += size[b]
            return size[a]
        return size[a]

    freqForLen = [0]*(max_len+1)
    pairs = [(LCP[i], i) for i in range(1, N)]
    pairs.sort(key=lambda x: x[0], reverse=True)

    for val, idx in pairs:
        if val == 0:
            continue
        new_size = union(idx-1, idx)
        if new_size > freqForLen[val]:
            freqForLen[val] = new_size

    for w in words:
        wl = len(w)
    for l in range(1, max_word_length+1):
        if freqForLen[l] < 1:
            freqForLen[l] = 1

    for l in range(max_len, 1, -1):
        if freqForLen[l-1] < freqForLen[l]:
            freqForLen[l-1] = freqForLen[l]

    output = []
    for q in queries:
        if q > max_word_length:
            output.append(-1)
        else:
            output.append(freqForLen[q] if freqForLen[q] > 0 else -1)

    print('\n'.join(map(str, output)))
solve()