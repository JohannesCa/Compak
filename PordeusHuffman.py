import json
import progressbar
from Convertions import bitstring_to_bytes
from HuffmanTree import updateTree
from os import stat


def compak(fname, verbose=False):
    with open('files/' + fname, 'rb') as inputf:
        data = list(inputf.read())

    freqs = dict()

    for symbol in data:
        if symbol not in freqs:
            freqs.update({symbol: 1})
        else:
            freqs[symbol] += 1

    tree = updateTree(freqs, verbose)
    original_freqs = dict(freqs)

    buffer = ''
    progress = 0

    with progressbar.ProgressBar(max_value=len(data)) as bar:
        for symbol in data:
            sym_buffer = ''
            lvl = tree
            if verbose:
                print('-- Verifying symbol ', symbol)
                print('-- tree: ', lvl)

            while True:
                if len(lvl[1]) > 1:
                    if symbol in lvl[2][1]:
                        lvl = lvl[2]
                        sym_buffer += '1'
                        if verbose:
                            print('-- new lvl: ', lvl)
                            print('-- sym_buffer: ', sym_buffer)
                        continue

                    else:
                        lvl = lvl[3]
                        sym_buffer += '0'
                        if verbose:
                            print('-- new lvl: ', lvl)
                            print('-- sym_buffer: ', sym_buffer)
                        continue

                else:
                    buffer += sym_buffer
                    freqs[symbol] -= 1

                    if freqs[symbol] == 0:
                        del freqs[symbol]

                    tree = updateTree(freqs, verbose)

                    if verbose:
                        print('-- end of line')
                        print('-- buffer: ', buffer)
                        print('-- updated freqs:', freqs)
                    break

            progress += 1
            bar.update(progress)

    print('\n>> Encoding code to bytes...')
    buffer = '1' + buffer
    bin_data = bitstring_to_bytes(buffer, showprogress=True)
    compressed_file = 'output/' + fname.split('.')[0] + '.zop'

    if verbose:
        print('-- Final Bit array:', buffer)
        print('-- Byte code: ', bin_data)

    print('\n\n>> Writing compressed file:', compressed_file)
    with open(compressed_file, 'wb') as outputf:
        outputf.write(bin_data)

    metadata = json.dumps({"freqs": original_freqs, "data": compressed_file, "extension": fname.split('.')[-1]})
    metadata_file = 'output/' + fname.split('.')[0] + '.meta'

    print('>> Writing metadata file:', metadata_file)
    with open(metadata_file, 'w') as metadataf:
        metadataf.write(metadata)

    original_size = stat('files/' + fname).st_size
    compressed_size = stat(compressed_file).st_size
    compress_ratio = original_size/compressed_size

    print('\n:: Some info:')
    print('   -- Compressed file size:\t', compressed_size, 'bytes')
    print('   -- Original file size:\t', original_size, 'bytes')
    print('   -- Compression ratio:\t {0:.3f}\n\n'.format(compress_ratio))


def unpack(metadata_file, verbose=False):
    print('>> Reading metadata file...\t', metadata_file)
    with open(metadata_file, 'r') as input:
        fdata = input.read()
        fdata = json.loads(fdata)

    file = fdata["data"]
    freqs = fdata["freqs"]
    freqs = {int(key): int(value) for key, value in freqs.items()}

    if verbose:
        print('-- Unpack read freqs', freqs)

    print('>> Reading compressed file...\t', file)
    with open(file, 'rb') as input:
        raw_data = list(input.read())

    bits = ''
    bar = progressbar.ProgressBar(max_value=progressbar.UnknownLength)
    progress = 0

    print("\n>> Decoding raw data...")
    for byte in raw_data:
        binstr = bin(byte)[2:]
        resto = len(binstr) % 8
        if resto != 0:
            binstr = ('0' * (8 - resto)) + binstr

        bits += binstr
        progress += 1
        bar.update(progress)

    tree = updateTree(freqs, verbose)

    buffer = list()
    lvl = tree
    progress = 0
    bits = bits[1:]

    if verbose:
        print('-- Bit Code:', bits)

    print('\n\n>> Decompressing file...')
    with progressbar.ProgressBar(max_value=len(bits)) as bar:
        for bit in bits:
            if verbose:
                print('-- lvl:', lvl)

            if bit == '1':
                lvl = lvl[2]

            else:
                lvl = lvl[3]

            if len(lvl[1]) == 1:
                buffer.append(lvl[1][0])
                freqs[lvl[1][0]] -= 1
                if freqs[lvl[1][0]] == 0:
                    del freqs[lvl[1][0]]

                if verbose:
                    print('!- found leaf:', lvl)
                    print('!- new_buffer: ', buffer, '\n')

                lvl = updateTree(freqs, verbose)

            if len(lvl) == 2:
                while lvl[0] > 0:
                    if verbose:
                        print('!- last char: ', lvl[1])
                    buffer.append(lvl[1][0])
                    lvl[0] -= 1
                break

            progress += 1
            bar.update(progress)

    buffer = bytearray(buffer)
    output_file = metadata_file.split('.')[0] + '.' + fdata["extension"]

    if verbose:
        print('-- Decompressed file:', buffer)

    print('\n>> Writing decompressed file: ', output_file)
    with open(output_file, 'wb') as output:
        output.write(buffer)
