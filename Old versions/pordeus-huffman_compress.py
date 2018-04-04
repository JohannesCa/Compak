#!/usr/bin/python
# -*- coding: utf-8 -*-

from sys import argv
# import numpy as np
import json
# from pprint import pprint
from heapq import heappush, heappop, heapify


def updateTree(char_freqs):
    new_tree = []
    min_heap = []
    for symbol in char_freqs:
        heappush(min_heap, [char_freqs[symbol], symbol])

    smallest0, smallest1 = None, None

    while min_heap:
        smallest0 = (heappop(min_heap))
        try:
            smallest1 = (heappop(min_heap))
        except IndexError:
            break
        heappush(min_heap, smallest0 + smallest1)
        new_tree.append([smallest0, smallest1])

    return new_tree[::-1]


def compak(arquivo):
    #arquivo = "ABRACADABRA"
    freqs = {}
    tree = []

    for symbol in arquivo:
        if symbol not in freqs:
            freqs.update({symbol:1})
        else:
            freqs[symbol] += 1

    tree = updateTree(freqs)
    original_tree = list(tree)
    original_freqs = dict(freqs)
    buffer = ''

    for symbol in arquivo:
        symbol_buffer = ''
        for level in tree:
            if symbol not in level[0]:
                symbol_buffer += '1'
                break
            else:
                symbol_buffer += '0'

        buffer += symbol_buffer
        freqs[symbol] -= 1
        tree = updateTree(freqs)

    return json.dumps({"bits": buffer, "tree": original_freqs})


def unpack(arquivo):
    data = open(arquivo).read()
    data = json.loads(data)
    #print()

    freqs = data["tree"]
    raw_data = data["bits"]

    tree = updateTree(freqs)
    print(tree, raw_data)
    x = ''
    buffer = ''
    while raw_data:
        if len(raw_data[int(raw_data[0])]) == 2:
            print("a")
            del raw_data[0]

    # pprint.pprint(original_tree[0])
    # freqs = {}
    # for i in original_tree[0]:
    #     for j in range(i):



if __name__ == '__main__':
    fp = open('compress.txt', 'w')
    fp.write(compak("ABRACADABRA"))
    fp.close()
    unpack('compress.txt')
