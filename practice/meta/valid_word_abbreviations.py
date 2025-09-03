
def valid_abbr(source, abbr):
    source_p = 0
    abbr_p = 0

    while source_p < len(source) and abbr_p < len(abbr):
        if abbr[abbr_p].isdigit():
            if int(abbr[abbr_p]) == 0:
                return False
            
            n_steps = 0
            while abbr_p < len(abbr) and abbr[abbr_p].isdigit():
                n_steps *= 10
                n_steps += int(abbr[abbr_p])
                abbr_p += 1

            source_p += n_steps
            
        else:
            if source[source_p] != abbr[abbr_p]:
                return False
            
            source_p += 1
            abbr_p += 1

    return True


if __name__ == "__main__":
    # print(valid_abbr("apple", "a3le"))
    print(valid_abbr("apple", "a04"))
    print(valid_abbr("apple", "a02le"))