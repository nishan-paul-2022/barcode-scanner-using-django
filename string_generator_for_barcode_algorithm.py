from random import randrange
from functools import reduce


def string_generator_ean8():
    output = []
    for x in range(7):
        output.append(randrange(10))

    summation = lambda x, y: int(x) + int(y)
    evensum = reduce(summation, output[::2])
    oddsum = reduce(summation, output[1::2])
    checksum = (10 - ((evensum + oddsum * 3) % 10)) % 10
    output.append(checksum)
    output = ''.join(map(str, output))
    return output


def string_generator_ean13():
    output = []
    for x in range(12):
        output.append(randrange(10))

    summation = lambda x, y: int(x) + int(y)
    evensum = reduce(summation, output[::2])
    oddsum = reduce(summation, output[1::2])
    checksum = (10 - ((evensum + oddsum * 3) % 10)) % 10
    output.append(checksum)
    output = ''.join(map(str, output))
    return output


def string_generator_ean14():
    output = []
    for x in range(13):
        output.append(randrange(10))

    summation = lambda x, y: int(x) + int(y)
    evensum = reduce(summation, output[::2])
    oddsum = reduce(summation, output[1::2])
    checksum = (10 - ((evensum + oddsum * 3) % 10)) % 10
    output.append(checksum)
    output = ''.join(map(str, output))
    return output


def string_generator_itf():
    output = []
    for x in range(13):
        output.append(randrange(10))

    summation = lambda x, y: int(x) + int(y)
    evensum = reduce(summation, output[::2])
    oddsum = reduce(summation, output[1::2])
    checksum = (10 - ((evensum + oddsum * 3) % 10)) % 10
    output.append(checksum)
    output = ''.join(map(str, output))
    return output


if __name__ == '__main__':
    print(string_generator_ean8())
    print(string_generator_ean13())
    print(string_generator_ean14())
    print(string_generator_itf())

# https://github.com/maxmumford/random-ean13-generator/blob/master/ean13-generator.py
