# # Write any import statements here
#
# def getArtisticPhotographCount(N: int, C: str, X: int, Y: int) -> int:
#     # Write your code here
#
#     #
#     # N^2
#     # . P . B A A P . B
#     #       ]
#
#     # [PBBP] A [BPP]
#     # {ind -> [{B: #, P: #}, {B: #, P: #}]}
#     # for each A, number of possible photographs is #B_l * #P_r + #P_l * #B_r
#     # window length is Y - X
#     # offset is X
#
#     for ind, entity in enumerate(C):
#         if entity == "P" or entity == "B":
#             # looking for Actor
#             for query_entity in C[ind + X:ind + Y + 1]:
#                 if query_entity == "A":
#                     break
#
#             if actor_lookup_ind <= ind + Y:
#                 # Actor was found
#                 for opposite_lookup_ind in range(actor_lookup_ind + X, actor_lookup_ind)
#
#     return 0

# Write any import statements here

from collections import defaultdict

def opposite(entity: str):
    return "B" if entity == "P" else "P"


def getArtisticPhotographCount(N: int, C: str, X: int, Y: int) -> int:
    # [PBBP] A [BPP]

    # P.AAA
    # 0123
    # X = 2,
    # Y = 3
    # {ind -> [{B: #, P: #}, {B: #, P: #}]}
    # for each A, number of possible photographs is #B_l * #P_r + #P_l * #B_r
    # window length is Y - X
    # offset is X

    total_count = 0
    counts_from_left = defaultdict(lambda: defaultdict(int))
    counts_from_right = defaultdict(lambda: defaultdict(int))

    # from left to right
    for ind, entity in enumerate(C):
        if entity == "B" or entity == "P":
            for offset, opposite_entity in enumerate(C[ind + X: ind + Y + 1]):
                if opposite_entity == "A":
                    actors_ind = ind + X + offset
                    counts_from_left[actors_ind][entity] += 1

    # from right to left
    C_reversed = C[::-1]
    for ind, entity in enumerate(C_reversed):
        if entity == "B" or entity == "P":
            for offset, opposite_entity in enumerate(C_reversed[ind + X: ind + Y + 1]):
                if opposite_entity == "A":
                    actors_ind = len(C) - (ind + X + offset) - 1
                    counts_from_right[actors_ind][entity] += 1

    # Compute final sum
    for ind, entity_count_dict in counts_from_left.items():
        for entity, count in entity_count_dict.items():
            total_count += count * counts_from_right[ind][opposite(entity)]

    return total_count


def getArtisticPhotographCountV2(N: int, C: str, X: int, Y: int) -> int:
    counts_from_left = getCountFromLeft(N, C, X, Y)
    counts_from_right = getCountFromLeft(N, C[::-1], X, Y)

    total_count = 0
    for ind, counts in counts_from_left.items():
        for entity, count in counts.items():
            total_count += count * counts_from_right[N - ind - 1][opposite(entity)]

    return total_count

def getCountFromLeft(N, C, X, Y):
    total_counts = defaultdict(lambda: defaultdict(int))
    moving_counts = defaultdict(int)
    yi = X - Y - 1
    for xi in range(0, N - X):
        moving_counts[C[xi]] += 1
        if yi >= 0:
            moving_counts[C[yi]] -= 1
        yi += 1

        if C[xi + X] == "A":
            total_counts[xi + X]["B"] = moving_counts["B"]
            total_counts[xi + X]["P"] = moving_counts["P"]

    return total_counts


if __name__ == "__main__":
    print(getArtisticPhotographCountV2(5, "APABA", 1, 2))
