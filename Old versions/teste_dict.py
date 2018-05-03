#!/usr/bin/python3
# -*- coding: utf-8 -*-

from json import loads
from reformat import reformat_dict


if __name__ == "__main__":
    with open('output/dict1.comp', 'r') as input1:
        file1 = str(input1.read())

    file1 = file1.replace("'", '"')
    print('-- File 1 dict:\n', file1)

    dict1 = loads(file1)
    dict1 = reformat_dict(dict1)
    print('\n-- Reformat\n', dict1)

    with open('output/dict1.comp', 'w') as input1:
        input1.write(str(dict1))
