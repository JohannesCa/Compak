import Convertions
import progressbar


def lzw_compress(dict_size, input_file, output_file):
    size = dict_size
    code = list()

    if dict_size < 256:
        size = 256

    # Preparing dict
    # dictionary = dict()
    # for i in range(256):
    #     aux = str(i)
    #     dictionary.update({aux: i})

    dictionary = {'97': 0, '98': 1, '99': 2, '100': 3, '114': 4}

    # dictionary = {1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e', 6: 'a|d'}
    # # print(dictionary)
    #
    # dictionary = {v: k for k, v in dictionary.items()}
    # print(dictionary)
    #
    # a = 'a|a'
    # if a in dictionary:
    #     print('TRUE', dictionary[a])
    # else:
    #     print('HAHA FALSE')

    # Read the input file and save data as string list
    with open('files/' + input_file, 'rb') as inputf:
        data = list(inputf.read())
        data = [str(x) for x in data]
        data = data[:-1]

    print('Data:', data)


    index = 5
    for sym in range(len(data)):
        new_block = data[sym]

        while new_block in dictionary:
            block = new_block
            sym += 1
            try:
                new_block += '|' + data[sym]

            except IndexError:
                break

            # print('tmp: ', new_block, type(new_block))
            # print('dic: ', dictionary, '\n')

        print('BREAK', block, sym)

        code.append(dictionary[block])

        if new_block not in dictionary:
            print('NEW BLOCK INSERT', new_block)
            # print('old dic')
            # print(dictionary)

            dictionary.update({new_block: index})
            index += 1

            # print('new dic')
            # print(dictionary)
            # print('\n')

    print('Final code: ', code)


    # output = open('output/' + output_file, 'wb'
    # output.close()


def lzw_decompress(input_file):
    dictionary = dict()

    # Read the input file and prepare the output
    inputf = open('output/' + input_file, 'rb')
    inputf.close()