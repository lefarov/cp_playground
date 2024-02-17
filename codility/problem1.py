from collections import defaultdict


def solution(S):
    # write your code in Python 3.6
    # HM: file type -> size
    sizes = {"music": 0, "images": 0, "movies": 0, "other": 0}
    # HM: extenstion -> file type
    ext_2_type = {
        "mp3": "music",
        "aax": "music",
        "flac": "music",
        "jpg": "images",
        "bmp": "images",
        "gif": "images",
        "mp4": "movies",
        "avi": "movies",
        "mkv": "movies",
    }
    
    # Split liens by "\n"
    lines = S.splitlines()
    for file_line in lines:
        # Split line by " "
        name, size = file_line.split()
        # Split name by "." and get the last one
        ext = name.split('.')[-1]

        # Add size to corect category
        if ext in ext_2_type:
            sizes[ext_2_type[ext]] += int(size[:-1])

        else:
            sizes["other"] += int(size[:-1])
    
    return "\n".join([f"{k} {v}b" for k, v in sizes.items()])


if __name__ == "__main__":
    print(solution(''''''))