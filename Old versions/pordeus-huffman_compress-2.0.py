#!/usr/bin/python
# -*- coding: utf-8 -*-

# from pprint import pprint
import json
from heapq import heappush, heappop, heapify
from math import log2
from sys import argv
from os import stat
import binascii
from bitstring import BitArray


def bitstring_to_bytes(s):
    # print(len(s))
    if len(s) % 8 != 0:
        s = s + '0'*(8 - (len(s) % 8))

    # v = int(s, 2)
    b = []
    # while v:
    #     print("v", v, "b", b)
    #     b.append(v & 0xff)
    #     v >>= 8
    # print(s, len(s))
    while s:
        sub = s[:8]
        b.append(int(sub, 2))
        # print(hex(int(sub, 2)), sub)
        s = s[8:]
    return bytes(b)


def updateTree(char_freqs, verbose=False):
    new_tree = []
    min_heap = []
    for symbol in char_freqs:
        heappush(min_heap, [char_freqs[symbol], symbol])

    if verbose:
        print('>> constructing tree')

    while min_heap:
        smallest0 = (heappop(min_heap))
        if verbose:
            print('poped ', smallest0)

        try:
            smallest1 = (heappop(min_heap))
            if verbose:
                print('poped ', smallest1)

        except IndexError:
            new_tree = smallest0
            break

        heappush(min_heap, [smallest0[0] + smallest1[0], smallest0[1] + smallest1[1], smallest0, smallest1])
        if verbose:
            print('pushing ', [smallest0[0] + smallest1[0], smallest0[1] + smallest1[1], smallest0, smallest1])

    if verbose:
        print('>> final tree: ', new_tree, '\n')

    return new_tree


def compak(arquivo, verbose=False):
    freqs = {}

    for symbol in arquivo:
        if symbol not in freqs:
            freqs.update({symbol: 1})
        else:
            freqs[symbol] += 1
    it = 0
    tree = updateTree(freqs, verbose)
    original_freqs = dict(freqs)

    buffer = ''
    for symbol in arquivo:
        it += 1
        print(it)
        sym_buffer = ''
        lvl = tree
        if verbose:
            print('verifying symbol ', symbol)
            print('>> tree: ', lvl)

        while True:
            if len(lvl[1]) > 1:
                if symbol in lvl[2][1]:
                    lvl = lvl[2]
                    sym_buffer += '1'
                    if verbose:
                        print('new lvl: ', lvl)
                        print('sym_buffer: ', sym_buffer)
                    continue

                else:
                    lvl = lvl[3]
                    sym_buffer += '0'
                    if verbose:
                        print('new lvl: ', lvl)
                        print('sym_buffer: ', sym_buffer)
                    continue

            else:
                buffer += sym_buffer
                freqs[symbol] -= 1
                if freqs[symbol] == 0:
                    del freqs[symbol]

                if tree == 2:
                    sym_buffer += '0'
                else:
                    tree = updateTree(freqs, verbose)

                if verbose:
                    print('>> end of line')
                    print('>> buffer: ', buffer)
                break

    buffer = '1' + buffer
    # print(buffer)
    bin_data = bitstring_to_bytes(buffer[:-1])
    # print(bin_data)
    compressed_file = argv[1].split('.')[0] + '.zop'
    with open(compressed_file, 'wb') as output:
        if verbose:
            print('>> Writing compressed file:', compressed_file)
        output.write(bin_data)

    return json.dumps({"freqs": original_freqs, "data": compressed_file})


def unpack(metadata, verbose=False):
    with open(metadata, 'r') as input:
        fdata = input.read()
        fdata = json.loads(fdata)

    freqs = fdata["freqs"]
    file = fdata["data"]
    raw_data = []
    with open(file, 'rb') as input:
        raw_data += input.read()

    # print(type(raw_data), raw_data)
    bits = ''
    for byte in raw_data:
        binstr = bin(byte)[2:]
        resto = len(binstr) % 8
        if resto != 0:
            binstr = ('0'*(8-resto)) + binstr
        # print(hex(byte), " ", binstr)
        bits += binstr
    # print(bits)

#100010001100110100010000000100111101001001001000110110101101000011010111011110001001001001000000
#100010001100110100010000000100111101001001001000110110101101000011010111011110001001001001000000
    #     bit = bin(byte)[2:]
    #     aux = ''
    #     if bit != '0':
    #         fillz = len(bit) % 8
    #     else:
    #         print('AAAAAAAAAAAAAAAAA')
    #         bits += '00000000'
    #         continue
    #     if fillz != 0:
    #         aux = str('0' * (8 - fillz))
    #         print(bin(byte)[2:], "entrou no fillz!")
    #     bits += (bit + aux)
    #     print(hex(byte), bits, len(bits))
    #     flag = True
    # #10000100 01010000 10000000 100111100111 00010010
    #10000100 01010    10000000 100110001100 111010010
    print(bits, type(bits))
    tree = updateTree(freqs, False)

    if verbose:
        pass
        # print('>> unpacking ', raw_data)

    buffer = ''
    lvl = tree
    count = 0
    # bits = '110000'
    bits = bits[1:]
    for bit in bits:
        # bit =
        if verbose:
            print('lvl:', lvl, raw_data)
            print('>> verifying bit', count, '=', bit)

        if bit == '1':
            lvl = lvl[2]

        else:
            lvl = lvl[3]

        if len(lvl[1]) == 1:
            buffer += lvl[1]
            freqs[lvl[1]] -= 1
            if freqs[lvl[1]] == 0:
                del freqs[lvl[1]]

            if verbose:
                print('found leaf:', lvl)
                print('new_buffer: ', buffer, '\n')

            lvl = updateTree(freqs, False)
        # print('CACETE LVL', lvl)
        if len(lvl) == 2:
            # print('caralho')
            buffer += lvl[1]
            break
        count += 1


    return buffer


if __name__ == '__main__':
    print(
        '''
    Pordeus-Huffman Compressor --- Version 1.3.8 Mar 31 2018
    Copyright (c) 2018 by all Contributors,
    ALL RIGHTS RESERVED
        ''')

    # test = compak('ABRACADABRA', verbose=True)
    # print(test)

    # prev_tree = compak('ABRACADABRA')
    # new_tree = compak('ABRACADABRA')
    # for i in range(100):
    #     if new_tree != prev_tree:
    #         print('Test', i, 'ERROR:', new_tree, '!=', prev_tree)
    #         break
    #     else:
    #         print('Test', i, 'PASSED:', new_tree)
    #         prev_tree = new_tree
    #         new_tree = compak('ABRACADABRA')

    word = ''
    if len(argv) < 2:
        print('>> Running default test')
        file = 'compress.txt'
        word = 'ABRACADABRA'
    else:
        file = argv[1]
        print('Opening', file)
        with open(file, 'rb') as input:
            word = input.read()
        # print(type(word), word)
        word = word.decode('ascii')
        # print(word[:100])

    file = 'output.txt'
    with open(file, 'w') as output:
        # print('>> Compressing', word)
        data = compak(word)
        print('>> Writing in file', file)
        output.write(data)

    print('Tamanho do arquivo comprimido em bytes:', stat('output.txt').st_size)
    print('\n>> Uncompressing file', file)

    data = str.encode(unpack(file))
    with open('output2.txt', 'wb') as output:
        output.write(data)

    print('>> Uncompressed:', )



    # s = "0110100001101001"
    # print(bitstring_to_bytes(s))
    #
    # c = BitArray(bitstring_to_bytes(s))
    # print(s)
    # print(c.bin)

