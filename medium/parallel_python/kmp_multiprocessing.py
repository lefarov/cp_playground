import argparse
import os
import time

from multiprocessing import Process, Queue
from typing import List


def compute_lps(pattern: str) -> List[int]:
    # Longest Proper Prefix that is suffix array
    lps = [0] * len(pattern)

    prefi = 0
    for i in range(1, len(pattern)):
        
        # Phase 3: roll the prefix pointer back until match or 
        # beginning of pattern is reached
        while prefi and pattern[i] != pattern[prefi]:
            prefi = lps[prefi - 1]

        # Phase 2: if match, record the LSP for the current `i`
        # and move prefix pointer
        if pattern[prefi] == pattern[i]:
            prefi += 1
            lps[i] = prefi

        # Phase 1: is implicit here because of the for loop and 
        # conditions considered above

    return lps


def kmp(pattern: str, text: str) -> List[int]:
    match_indices = []
    pattern_lps = compute_lps(pattern)

    patterni = 0
    for i, ch in enumerate(text):
        
        # Phase 3: if a mismatch was found, roll back the pattern
        # index using the information in LPS
        while patterni and pattern[patterni] != ch:
            patterni = pattern_lps[patterni - 1]

        # Phase 2: if match
        if pattern[patterni] == ch:
            # If the end of a pattern is reached, record a result
            # and use infromation in LSP array to shift the index
            if patterni == len(pattern) - 1:
                match_indices.append(i - patterni)
                patterni = pattern_lps[patterni]
            
            else:
                # Move the pattern index forward
                patterni += 1

        # Phase 1: is implicit here because of the for loop and 
        # conditions considered above

    return match_indices


def find_anna(text, queue):
    queue.put(len(kmp("Anna", text)))


if __name__ == "__main__":
    """
    Computate a number of occurances of the word "Anna" 
    with the KMP algorithm and time the exectuion.
    """
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-n", 
        "--num_workers", 
        type=int, 
        default=1,
        choices=[1, 2, 4, 8],
        help="Number of workers. If 1, computation is happening serially."
    )

    args = parser.parse_args()

    # Load 50 concatenated "War and Peace" into the memory. 
    # File contains 887228714 symbols
    text_path = os.path.join(os.path.dirname(__file__), "data", "war_and_peace_repeated.txt")
    with open(text_path) as text_file:
        text = text_file.read()

    if args.num_workers == 1:
        # Serial execution
        t_start = time.time()
        res = len(kmp("Anna", text))

        # Assert the result and return timing
        assert res == 810081
        print(time.time() - t_start)

    else:
        # Parallel execution
        # Define the length of substring to be processed by every worker
        len_worker = int(len(text) / args.num_workers)
        t_start = time.time()

        # Define the MP queue for the result communication and
        # initialize the processes list
        queue = Queue()
        processes = []

        # Iterate over n-1 workers (the driver process will also do its part)
        for wi in range(args.num_workers - 1):
            # Define the boundaries of the substring for every worker
            lb = wi * len_worker
            rb = (wi + 1) * len_worker

            # Start process and append it to the list
            process = Process(target=find_anna, args=(text[lb:rb], queue))
            process.start()
            processes.append(process)

        # Compute the rest of the text on the driver process
        lb = (args.num_workers - 1) * len_worker
        res = len(kmp("Anna", text[lb:]))
        
        # Join all processes
        for process in processes:
            process.join()
        
        # Add up the results from all processes
        for _ in range(args.num_workers - 1):
            res += queue.get()

        # Assert hte result and return the timing
        assert res == 810081
        print(time.time() - t_start)