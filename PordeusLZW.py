from itsdangerous import int_to_byte, int_to_bytes
from iteration_utilities import deepflatten
from Convertions import intarray_to_bytes
from math import log2, floor
from os import stat
import progressbar


def lzw_compress(dict_size, input_file, output_file, verbose=False):
    max_dict_size = dict_size
    code = list()

    if max_dict_size < 256:
        max_dict_size = 256
        print('-- INFO: Using dictionary minimum size ({})\n'.format(max_dict_size))

    elif max_dict_size > 0xffff:
        max_dict_size = 0xffff
        print('-- INFO: Using dictionary maximum size ({})\n'.format(max_dict_size))

    if verbose:
        print('-- Dictionary max size:', max_dict_size)

    # Preparing dict
    dictionary = dict()
    for i in range(256):
        aux = str(i)
        dictionary.update({aux: i})

    # Read the input file and save data as string list
    with open('files/' + input_file, 'rb') as inputf:
        data = list(inputf.read())
        data = [str(x) for x in data]

    if verbose:
        print('-- Reading input:\n', data)

    # Preparing procedure
    index = 256
    sym = 0

    print('-- Indexing blocks:')
    with progressbar.ProgressBar(max_value=len(data)) as bar:
        while sym < len(data):
            new_block = data[sym]
            block = data[sym]

            # Verify if the block is already in the dictionary
            while new_block in dictionary:
                block = new_block
                sym += 1

                # Try to append the next symbol of the word to the block
                try:
                    aux = data[sym]
                    new_block += '|' + aux

                except IndexError:
                    break

            # Now get the code corresponding to the block
            code.append(dictionary[block])

            # Adds the new block to the dictionary if the dict is not full
            if new_block not in dictionary and index < max_dict_size:
                dictionary.update({new_block: index})
                index += 1

            bar.update(sym)

    # Calculate de maximum index length
    word_max_size = floor(log2(index) + 1)
    index_size = floor(log2(word_max_size) + 1)

    # Generating byte code
    bytecode = intarray_to_bytes(code, index_size, showprogress=True)

    # Generating dictionary size bytes
    max_dict_size = int_to_bytes(max_dict_size)
    if len(max_dict_size) < 2:
        max_dict_size = int_to_byte(0) + max_dict_size

    # Saving the maximum dictionary size within the code
    bytecode = max_dict_size + int_to_byte(index_size) + bytecode

    if verbose:
        print('\n-- Final code:\n', code)
        print('\n-- Byte code:\n', bytecode)

    # Writing output file
    compressed_file = 'output/' + output_file
    print('\n\n>> Writing compressed file:', compressed_file)
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


def lzw_decompress(input_file, original_format, verbose=False):
    # Preparing dict
    dictionary = dict()
    for i in range(256):
        dictionary.update({i: [i]})

    # Read the input file and prepare the output
    with open('output/' + input_file, 'rb') as inputf:
        data = bytes(inputf.read())

    if verbose:
        print('-- Read data:\n', data)

    # Get dictionary max size and index size
    dict_max_size = data[0]*256 + data[1]
    index_size = data[2]

    if verbose:
        print('-- Metadata:')
        print('\tdict_max_size:', dict_max_size)
        print('\tindex_size:', index_size)

    # Setting up the actual data in binary, with the padding
    data = data[3:]
    data = ['0'*(8-len(bin(x)[2:])) + bin(x)[2:] for x in data]

    # Fetch bitstring
    bitstring = ''
    for i in range(len(data)):
        bitstring += data[i]

    # Decode operation
    string = list()
    index = 256

    progress = 0
    with progressbar.ProgressBar(max_value=len(bitstring)) as bar:
        while bitstring:
            try:
                codeword_len = int(bitstring[:index_size], 2)
                bitstring = bitstring[index_size:]

                codeword = int(bitstring[:codeword_len], 2)
                bitstring = bitstring[codeword_len:]

            except ValueError:
                break

            char = dictionary[codeword]
            string.append(char)
            if verbose:
                print('-- Decoded', codeword, char)

            if index == 256:
                dictionary.update({index: list(char)})
                index += 1

            elif index < dict_max_size:
                dictionary[index-1].append(char[0])
                dictionary.update({index: list(char)})
                index += 1

            elif index == dict_max_size:
                dictionary[index-1].append(char[0])
                index += 1

            progress += codeword_len + index_size
            bar.update(progress)

    # Saving string and preparing to write to file
    string = list(deepflatten(string, depth=1))
    data = [int(x) for x in string]
    data = bytes(data)

    if verbose:
        print('-- Found string:\n', data)

    # Write output file
    file_name = input_file.split('.')[0] + '.' + original_format
    print('\n>> Writing decompressed file: ', file_name)
    with open('output/' + file_name, 'wb') as output:
        output.write(data)

    print('>> Done!')
