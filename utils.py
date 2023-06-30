def str_to_int(str):
    res = 0
    for char in str:
        res = res * 256 + ord(char)
    return res