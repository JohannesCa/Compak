import Convertions
import progressbar


def lzw_compress(dict_size, input_file, output_file):
    dictionary = dict()
    for i in range(256):
        dictionary.update({i: str(i)})

    print(dictionary)
    # Read the input file and prepare the output
    inputf = open('files/' + input_file, 'rb')
    output = open('output/' + output_file, 'wb')

    inputf.close()
    output.close()


def lzw_decompress(input_file):
    dictionary = dict()

    # Read the input file and prepare the output
    inputf = open('output/' + input_file, 'rb')
    inputf.close()