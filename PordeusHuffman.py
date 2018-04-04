import json
from Convertions import bitstring_to_bytes
from HuffmanTree import updateTree
from os import stat


def compak(fname, verbose=False):
    with open('files/' + fname, 'rb') as inputf:
        data = list(inputf.read())

    data = [hex(x) for x in data]
    # print(data, type(data), type(data[0]))

    freqs = dict()

    for symbol in data:
        if symbol not in freqs:
            freqs.update({symbol: 1})
        else:
            freqs[symbol] += 1
    # print(freqs)

    tree = updateTree(freqs, verbose)
    original_freqs = dict(freqs)

    buffer = ''
    for symbol in data:
        sym_buffer = ''
        lvl = tree
        if verbose:
            print('verifying symbol ', symbol)
            print('>> tree: ', lvl)

        while True:
            if len(lvl[1]) > 4:
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

                tree = updateTree(freqs, verbose)

                if verbose:
                    print('>> end of line')
                    print('>> buffer: ', buffer)
                break

    buffer = '1' + buffer
    bin_data = bitstring_to_bytes(buffer)
    if verbose:
        print('>> Final Bit array:', buffer)
        print('>> Byte code: ', bin_data)

    compressed_file = 'output/' + fname.split('.')[0] + '.zop'
    if verbose:
        print('>> Writing compressed file:', compressed_file)

    with open(compressed_file, 'wb') as outputf:
        outputf.write(bin_data)

    metadata = json.dumps({"freqs": original_freqs, "data": compressed_file, "extension": fname.split('.')[-1]})
    metadata_file = 'output/' + fname.split('.')[0] + '.meta'
    if verbose:
        print('>> Writing metadata file:', metadata_file)

    with open(metadata_file, 'w') as metadataf:
        metadataf.write(metadata)

    if verbose:
        print('>> Compressed file size in bytes:', stat(compressed_file).st_size)


def unpack(metadata_file, verbose=False):
    with open(metadata_file, 'r') as input:
        fdata = input.read()
        fdata = json.loads(fdata)

    freqs = fdata["freqs"]
    file = fdata["data"]

    with open(file, 'rb') as input:
        raw_data = list(input.read())

    bits = ''
    for byte in raw_data:
        binstr = bin(byte)[2:]
        resto = len(binstr) % 8
        if resto != 0:
            binstr = ('0' * (8 - resto)) + binstr

        bits += binstr

    tree = updateTree(freqs, verbose)

    if verbose:
        print('>> Unpacking ', raw_data)

    buffer = ''
    lvl = tree
    count = 0
    bits = bits[1:]
    for bit in bits:
        if verbose:
            print('lvl:', lvl, raw_data)
            print('>> Verifying bit', count, '=', bit)

        if bit == '1':
            lvl = lvl[2]

        else:
            lvl = lvl[3]

        if len(lvl[1]) == 3 or len(lvl[1]) == 4:
            buffer += lvl[1]
            freqs[lvl[1]] -= 1
            if freqs[lvl[1]] == 0:
                del freqs[lvl[1]]

            if verbose:
                print('found leaf:', lvl)
                print('new_buffer: ', buffer, '\n')

            lvl = updateTree(freqs, verbose)

        if len(lvl) == 2:
            if verbose:
                print('last char: ', lvl[1])
            buffer += lvl[1]
            break

        count += 1

    buffer = buffer.split('0x')[1:]
    buffer = [int(x, 16) for x in buffer]
    buffer = bytearray(buffer)
    if verbose:
        print('>> Decompressed file:', buffer)

    output_file = metadata_file.split('.')[0] + '.' + fdata["extension"]
    if verbose:
        print('>> Writing decompressed file', output_file)

    with open(output_file, 'wb') as output:
        output.write(buffer)
