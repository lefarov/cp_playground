import sys


def solve(dat, t):
    N, K = dat

    if K % N == 0:
        # Build the list from 1 to N
        range_lst = list(range(1, N + 1))
        # Find the index of diag element
        i = range_lst.index(K / N)
        res = [""] * N
        for k in range(N):
            j = (i - k) % N
            print(j)
            for _ in range(N):
                res[k] += "{} ".format(range_lst[j])
                j = (j + 1) % N

        print("Case #{}: {}".format(t + 1, "POSSIBLE"))
        for r in res:
            print(r)
        
    # elif sum(range(1, N + 1)):
            
    else:
        print("Case #{}: {}".format(t + 1, "IMPOSSIBLE"))


if __name__ == "__main__":
    T = int(input())
    for t in range(T):
        solve(map(int, input().split()), t)

    sys.stdout.flush()
