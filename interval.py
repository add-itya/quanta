def solve():
    N, M = map(int, input().split())
    board = list(map(int, input().split()))
    
    intervals = []
    for _ in range(M):
        l, r = map(int, input().split())
        interval_min = min(board[l:r+1])
        intervals.append(interval_min)
    
    intervals.sort(reverse=True)
    
    alice_score = 0
    bob_score = 0
    
    turn = 0
    for val in intervals:
        if val > 0:
            if turn == 0:
                alice_score += val
            else:
                bob_score += val
            turn = 1 - turn
    
    print(alice_score, bob_score)
solve()