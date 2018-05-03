#!/usr/bin/python3
# -*- coding: utf-8 -*-

import PordeusHuffman
import PordeusLZW
from sys import argv


if __name__ == '__main__':
    print(
        '''
    Compak --- Version 3.6.10 Apr 30 2018
    Copyright (c) 2018 by all Contributors,
    ALL RIGHTS RESERVED
        ''')

    pack_file = ''
    unpack_file = ''
    compress, decompress = False, False

    # print(argv)
    if len(argv) < 2 or len(argv) > 4:
        print('Usage: ', argv[0], '[options] <input file>')
        exit(-1)

    if len(argv) == 2:
        if argv[1] == '-h':
            print(
                '''
    Usage:''', argv[0], '''[options] <input file>
    
    
DESCRIPTION
    Compak - A multi method compressor
    
    Authors:
        Johannes Pordeus
        Samuel Pordeus
    
    
DEFAULT OPERATION
    Compresses a file <input file> to .zop (compressed file) and generate the metadata file .meta with the same name.
    Then uncompresses the compressed file to comparison.


OPTIONS
    -d --default
        Use Huffman compressor (semi-adaptive).
            
    -l --lzw [dict_max_size]
        Use LZW compressing method, limiting the size of the dictionary. Case dict_max_size is not defined, the
        dictionary has undefined size (unlimited). Minimum dictionary size = 256.
            '''
            )
            exit(0)

        else:
            print('>> Using Huffman method')

            # File name is in the 1st position
            pack_file = argv[1]
            unpack_file = 'output/' + pack_file.split('.')[0] + '.meta'

            print('>> Compressing file', pack_file)
            PordeusHuffman.compak(pack_file)

            print('>> Decompressing file', unpack_file)
            PordeusHuffman.unpack(unpack_file)
            exit(0)

    # Case there is a flag
    elif len(argv) == 3 or len(argv) == 4:
        dict_max_size = 256
        pack_file = ''

        # Case dict_max_size is not defined, file name is in 2nd position
        if len(argv) == 3:
            pack_file = argv[2]
            # Else, it's on 3rd position

        else:
            dict_max_size = int(argv[2])
            pack_file = argv[3]

        # Verifying the flag
        if argv[1] == '-l' or argv[1] == '--lzw':
            print('>> Using LZW method')
            unpack_file = pack_file.split('.')[0] + '.lzp'

            print('>> Compressing file', pack_file)
            PordeusLZW.lzw_compress(dict_max_size, pack_file, unpack_file, verbose=False)

            print('>> Decompressing file', unpack_file)
            PordeusLZW.lzw_decompress(unpack_file, pack_file.split('.')[-1], verbose=False)
            exit(0)

        # Case crippled call
        else:
            print('Usage: ', argv[0], '[options] <input file>')
            exit(-1)
