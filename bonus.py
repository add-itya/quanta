def solve():
    input_data = input().strip()
    T = int(input_data)
    to_print = []

    for _ in range(T):
        line = input().strip().split()
        M, R = int(line[0]), int(line[1])
        
        requests = list(map(int, input().strip().split()))
        
        size = M + R
        fenw = [0]*(size+1)
        offset = R

        def fenw_update(i, delta):
            i += 1
            while i <= size:
                fenw[i] += delta
                i += i & (-i)

        def fenw_sum(i):
            s = 0
            i += 1
            while i > 0:
                s += fenw[i]
                i -= i & (-i)
            return s
        
        pos = [0]*(M+1)
        for p in range(1, M+1):
            pos[p] = p-1
        
        for i in range(M):
            fenw_update(i+offset, 1)
        
        top_pos = -1
        result = []
        for p in requests:
            current_pos = pos[p]
            fenw_index = current_pos + offset
            above = fenw_sum(fenw_index - 1)
            result.append(str(above))
            fenw_update(fenw_index, -1)
            pos[p] = top_pos
            fenw_update(pos[p] + offset, 1)
            top_pos -= 1
        to_print.append(result)
    for result in to_print:
        print(' '.join(result))
solve()