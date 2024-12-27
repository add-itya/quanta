def solve():
    first_line = input().strip().split()
    N, Q = int(first_line[0]), int(first_line[1])
    
    arr = list(map(int, input().strip().split()))
    
    queries = []
    for _ in range(Q):
        l, r = map(int, input().strip().split())
        queries.append((l, r))
    
    size = 1
    while size < N:
        size <<= 1

    sum_tree = [0] * (2*size)
    max_tree = [float('-inf')] * (2*size)
    idx_tree = [0] * (2*size)
    
    for i in range(N):
        sum_tree[size+i] = arr[i]
        max_tree[size+i] = arr[i]
        idx_tree[size+i] = i
    for i in range(N, size):
        sum_tree[size+i] = 0
        idx_tree[size+i] = i
    
    def combine(i_left, i_right):
        s = sum_tree[i_left] + sum_tree[i_right]
        if max_tree[i_left] > max_tree[i_right]:
            mv = max_tree[i_left]
            mi = idx_tree[i_left]
        elif max_tree[i_left] < max_tree[i_right]:
            mv = max_tree[i_right]
            mi = idx_tree[i_right]
        else:
            mv = max_tree[i_left]
            mi = idx_tree[i_left] if idx_tree[i_left] > idx_tree[i_right] else idx_tree[i_right]
        return s, mv, mi
    
    for i in range(size-1, 0, -1):
        s, mv, mi = combine(i*2, i*2+1)
        sum_tree[i] = s
        max_tree[i] = mv
        idx_tree[i] = mi
    
    def query_sum(l, r):
        l += size
        r += size
        res = 0
        while l <= r:
            if (l & 1) == 1:
                res += sum_tree[l]
                l += 1
            if (r & 1) == 0:
                res += sum_tree[r]
                r -= 1
            l >>= 1
            r >>= 1
        return res
    
    def query_max(l, r):
        l += size
        r += size
        max_val = float('-inf')
        max_idx = -1
        while l <= r:
            if (l & 1) == 1:
                if max_tree[l] > max_val:
                    max_val = max_tree[l]
                    max_idx = idx_tree[l]
                elif max_tree[l] == max_val and idx_tree[l] > max_idx:
                    max_idx = idx_tree[l]
                l += 1
            if (r & 1) == 0:
                if max_tree[r] > max_val:
                    max_val = max_tree[r]
                    max_idx = idx_tree[r]
                elif max_tree[r] == max_val and idx_tree[r] > max_idx:
                    max_idx = idx_tree[r]
                r -= 1
            l >>= 1
            r >>= 1
        return max_val, max_idx
    
    def update(pos, val):
        idx = pos + size
        sum_tree[idx] = val
        max_tree[idx] = val
        idx_tree[idx] = pos
        idx //= 2
        while idx > 0:
            s, mv, mi = combine(idx*2, idx*2+1)
            sum_tree[idx] = s
            max_tree[idx] = mv
            idx_tree[idx] = mi
            idx //= 2
    
    out = []
    idx = 0
    for _ in range(Q):
        l, r = queries[idx]
        idx += 1
        
        mid = (l + r) // 2
        sumLeft = query_sum(l, mid)
        sumRight = query_sum(mid + 1, r)
        diff = sumLeft - sumRight
        
        if diff == 0:
            out.append("0")
        else:
            absDiff = abs(diff)
            if diff > 0:
                mv, mi = query_max(l, mid)
                newVal = mv - absDiff
                update(mi, newVal)
                out.append(f"{absDiff} {newVal}")
            else:
                mv, mi = query_max(mid + 1, r)
                newVal = mv - absDiff
                update(mi, newVal)
                out.append(f"{absDiff} {newVal}")
    
    print("\n".join(out))
solve()