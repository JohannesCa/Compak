#!/usr/bin/python3
# -*- coding: utf-8 -*-

from json import loads as import_dict


if __name__ == "__main__":
    with open('output/dict1.comp', 'r') as input1:
        file1 = str(input1.read())

    with open('output/dict2.comp', 'r') as input2:
        file2 = str(input2.read())

    file1.replace("'", '"')
    file2.replace("'", '"')

    print('-- File 1 dict:\n', file1)
    print('\n-- File 2 dict:\n', file2)

    dict1 = import_dict(file1)
    dict2 = import_dict(file2)

    print('YUP' if dict1==dict2 else 'OH NO')
