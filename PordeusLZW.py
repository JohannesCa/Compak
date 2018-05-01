from locale import str

from itsdangerous import int_to_byte, int_to_bytes
from Convertions import intarray_to_bytes
from math import log2, floor
from os import stat
import progressbar


def lzw_compress(dict_size, input_file, output_file, verbose=False):
    max_dict_size = dict_size
    code = list()

    if max_dict_size < 256:
        max_dict_size = 256

    if verbose:
        print('-- Dictionary max size:', max_dict_size)

    # Preparing dict
    dictionary = dict()
    for i in range(256):
        aux = str(i)
        dictionary.update({aux: i})

    # dictionary = {'97': 0, '98': 1, '99': 2, '100': 3, '114': 4}
    # max_dict_size =

    # Read the input file and save data as string list
    with open('files/' + input_file, 'rb') as inputf:
        data = list(inputf.read())
        data = [str(x) for x in data]
        data = data[:-1]

    if verbose:
        print('-- Reading input:\n', data)

    # Preparing procedure
    index = 256
    sym = 0

    while sym < len(data):
        new_block = data[sym]
        block = data[sym]

        # Verify if the block is already in the dictionary
        while new_block in dictionary:
            block = new_block
            sym += 1

            # Try to append the next symbol of the word to the block
            try:
                new_block += '|' + data[sym]

            except IndexError:
                break

        # Now get the code corresponding to the block
        code.append(dictionary[block])

        # Adds the new block to the dictionary if the dict is not full
        if new_block not in dictionary and index < max_dict_size:
            dictionary.update({new_block: index})
            index += 1

    # Calculate de maximum index length
    index_size = floor(log2(index) + 1)

    # Generating byte code
    bytecode = intarray_to_bytes(code, index_size, showprogress=True)

    # Generating dictionary size bytes
    max_dict_size = int_to_bytes(max_dict_size)
    if len(max_dict_size) < 2:
        max_dict_size = int_to_byte(0) + max_dict_size

    # Saving the maximum dictionary size within the code
    bytecode = max_dict_size + int_to_byte(index_size) + bytecode

    if verbose:
        print('-- Final code: ', code)
        print('-- Byte code:', bytecode)

    # Writing output file
    compressed_file = 'output/' + output_file
    print('\n>> Writing compressed file:', compressed_file)
    with open(compressed_file, 'wb') as output:
        output.write(bytecode)

    # Getting statistics
    original_size = stat('files/' + input_file).st_size
    compressed_size = stat(compressed_file).st_size
    compress_ratio = original_size/compressed_size

    print('\n:: Some info:')
    print('   -- Compressed file size:\t', compressed_size, 'bytes')
    print('   -- Original file size:\t', original_size, 'bytes')
    print('   -- Compression ratio:\t {0:.3f}\n\n'.format(compress_ratio))


def lzw_decompress(input_file):
    # Preparing dict
    dictionary = dict()
    for i in range(256):
        aux = str(i)
        dictionary.update({aux: i})

    # Read the input file and prepare the output
    with open('output/' + input_file, 'rb') as inputf:
        data = bytes(inputf.read())

    dict_max_size = data[0]*256 + data[1]
    index_size = data[2]

    data = data[3:]
    data = ['0'*(8-len(bin(x)[2:])) + bin(x)[2:] for x in data]
    bitstring = ''

    for i in range(len(data)):
        bitstring += data[i]


    print(data)
    print(bitstring)