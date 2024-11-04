from typing import List


# Write any import statements here

def getMaxVisitableWebpages(N: int, L: List[int]) -> int:
    # Write your code here
    #     *
    # [2, 4, 2, 2, 3]
    # [0, 0, 0, 3, 0]
    #     *
    # [

    subsolutions = [0] * N
    for i in range(N):
        if subsolutions[i] != 0:
            continue

        current_session = [i]
        current_session_inds = {i: 0}
        j = L[i] - 1
        while True:
            if j in current_session_inds:
                ind_in_session = current_session_inds[j]
                for k in range(ind_in_session, len(current_session)):
                    subsolutions[current_session[k]] = len(current_session) - ind_in_session

                for k in range(ind_in_session):
                    subsolutions[current_session[k]] = len(current_session) - k

                break

            if subsolutions[j] != 0:
                for k, pos in enumerate(current_session[::-1]):
                    subsolutions[pos] = k + 1 + subsolutions[j]
                break

            current_session.append(j)
            current_session_inds[j] = len(current_session) - 1
            j = L[j] - 1

    return max(subsolutions)


if __name__ == "__main__":
    print(getMaxVisitableWebpages(4, [4, 1, 2, 1]))
