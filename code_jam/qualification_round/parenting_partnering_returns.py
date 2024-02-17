import sys


def read_tasks(N):
    M = []
    for _ in range(N):
        M.append(list(map(int, input().split())))
    
    return M


def validate_assignment(task, schedule):
    # Schedule is empty
    if not schedule:
        return 0
    # Task can be assigned as the first
    elif task[1] <= schedule[0][0]:
        schedule = [task] + schedule
        return 0
    # Task can be assigned as the last one
    elif task[0] >= schedule[-1][1]:
        schedule = schedule + [task]
        return 1
    # Go trough all the tasks in a schedule
    else:
        # Insert task to the correct place
        for i in range(len(schedule)):
            if task[0] >= schedule[i][1] and task[1] <= schedule[i + 1][0]:
                return i
    
    return -1


def recursive_assignment(tasks, res, schedule_C, schedule_J):
    # Scheduling is finished
    if not tasks:
        return True, res

    # Assume invalid schedule for the beginning
    success = False

    # Try to assign task to C
    idx = validate_assignment(tasks[0], schedule_C)
    if idx != -1:
        candidate_schedule_C = schedule_C.copy()
        candidate_schedule_C.insert(idx, tasks[0])
        success, res = recursive_assignment(tasks[1:], res + "C", candidate_schedule_C, schedule_J)
    
    if success:
        return True, res

    # Try to assign task to C
    idx = validate_assignment(tasks[0], schedule_J)
    if idx != -1:
        candidate_schedule_J = schedule_J.copy()
        candidate_schedule_J.insert(idx, tasks[0])
        success, res = recursive_assignment(tasks[1:], res + "J", schedule_C, candidate_schedule_J)

    if success:
        return True, res

    return False, res[:-1]
        


def solve(M, N, t):
        success, res = recursive_assignment(M, "", [], [])
        if success:
            return "Case #{}: {}".format(t + 1, res)
        else:
            return "Case #{}: {}".format(t + 1, "IMPOSSIBLE") 
        

if __name__ == "__main__":
    T = int(input())
    for t in range(T):
        N = int(input())
        M = read_tasks(N)
        print(solve(M, N, t))

    sys.stdout.flush()