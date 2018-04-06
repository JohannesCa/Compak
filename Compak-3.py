#!/usr/bin/python3
# -*- coding: utf-8 -*-

import PordeusHuffman
from sys import argv


if __name__ == '__main__':
    print(
        '''
    Compak --- Version 3.5.0 Apr 3 2018
    Copyright (c) 2018 by all Contributors,
    ALL RIGHTS RESERVED
        ''')

    pack_file = ''
    unpack_file = ''
    compress, decompress = False, False

    # print(argv)
    if len(argv) < 2 or len(argv) > 3:
        print('Usage: ', argv[0], '[flags] <input file>')
        exit(-1)

    if len(argv) == 2:
        if argv[1] == '-h':
            print(
                '''
    Usage:''', argv[0], '''<input file>
    
    
DESCRIPTION
    Compak - A semi-adaptive Huffman Compressor
    
    Authors:
        Johannes Pordeus
        Samuel Pordeus
    
    
DEFAULT OPERATION
    Compresses a file <input file> to .zop (compressed file) and generate the metadata file .meta with the same name.
    Then uncompresses the compressed file to comparison.


OPTIONS
    PACKING OPTIONS
        -c --compress
            Compress a single file and save compressed file with the same name case the option -o is not set.
            
        -u --unpack
            Decompress a single file and save decompressed file with the same name case option -o is not set.
                '''
            )
            exit(0)

        else:
            pack_file = argv[1]
            unpack_file = 'output/' + pack_file.split('.')[0] + '.meta'
            compress = True
            decompress = True

    elif len(argv) == 3:
        if argv[1] == '-c':
            pack_file = argv[2]
            compress = True

        elif argv[1] == '-u':
            unpack_file = 'output/' + argv[2]
            if argv[2].split('.')[-1] != 'meta':
                print('ERROR: Invalid file extension. Expected *.meta')
                exit(-1)
            decompress = True

        else:
            print('Usage: ', argv[0], '[flags] <input file>')
            exit(-1)

    if compress:
        print('>> Compressing file', pack_file)
        PordeusHuffman.compak(pack_file)

    if decompress:
        print('>> Decompressing file', unpack_file)
        PordeusHuffman.unpack(unpack_file)
