def diskStacking(disks):
    # Write your code here.
    # [ [2 1 2] [3 2 3] [2 2 8] [2 3 4] [1 3 1] [4 4 5] ]

    # [ [1 3 1] [2 1 2] [3 2 3] [2 3 4] [4 4 5] [2 2 8]]
    # [0     1       2       5       4    ]

    # two actions -> replace
    #             -> but above
    #             -> discard the current disk
    #             -> take only current disk

    subsolutions = [0] * len(disks)
    subsolutions[0] = disks[0][-1]

    for i in range(1, len(disks)):
        max_height = subsolutions[i - 1]
        disk = disks[i]
        for j, target_disk in enumerate(disks[:i]):
            base_disk = get_or_none(disks, j - 1)
            top_disk = get_or_none(disks, j + 1)

            if disk_ge(disk, top_disk):
                if disk_ge(base_disk, disk):
                    max_height = max(
                        max_height,
                        subsolutions[i - 1] + disk[-1] - target_disk[-1]
                    )

                if disk_ge(target_disk, disk):
                    max_height = max(
                        max_height,
                        subsolutions[i - 1] + disk[-1]
                    )

        subsolutions[i] = max_height

    pass


def get_or_none(disks, i):
    if i < 0 or i >= len(disks):
        return None

    return disks[i]


def disk_ge(disk1, disk2):
    if disk1 is None or disk2 is None:
        return True

    return disk1[0] > disk2[0] and disk1[1] > disk2[1]