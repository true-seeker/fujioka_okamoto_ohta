import math


def bytes_to_int(b):
    return int.from_bytes(b, byteorder='little')


def int_to_bytes(i):
    length = math.ceil(i.bit_length() / 8)
    return i.to_bytes(length, byteorder='little')
