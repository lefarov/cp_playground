import sys


def read_mat(N):
    M = []
    for _ in range(N):
        M.append(list(map(int, input().split())))
    
    return M


def solve(M, N, t):
    trace = 0
    ncol = 0
    nrow = 0
    # Create the vector of duplicate flags and matrix of visits for colums
    col_flags = [False] * N
    col_hits = [[0 for col in range(N)] for row in range(N)]
    for i in range(N):
        # Create the duplicate flag and vector of visits for row
        row_flag = False
        row_hits = [0] * N
        for j in range(N):
            # Check if we've been here already once
            if row_hits[M[i][j] - 1] > 0 and not row_flag:
                row_flag = True  # duplicate in the row
                nrow += 1
            
            # Increment hit
            row_hits[M[i][j] - 1] += 1
            
            # Same for column flags
            if col_hits[M[i][j] - 1][j] == 1 and not col_flags[j]:
                col_flags[j] = True  # duplicate in the column
                ncol += 1

            col_hits[M[i][j] - 1][j] += 1
        
        # Increment trace
        trace += M[i][i]
            
    
    return f"Case #{t + 1}: {trace} {nrow} {ncol}"


if __name__ == "__main__":
    T = int(input())
    for t in range(T):
        N = int(input())
        M = read_mat(N)
        print(solve(M, N, t))

    sys.stdout.flush()
