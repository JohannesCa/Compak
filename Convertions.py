import progressbar


def bitstring_to_bytes(s, showprogress=False):
    if len(s) % 8 != 0:
        s = s + '0'*(8 - (len(s) % 8))

    counter, bar = None, None
    b = []

    if showprogress:
        bar = progressbar.ProgressBar(max_value=progressbar.UnknownLength)
        counter = 0

    while s:
        sub = s[:8]
        b.append(int(sub, 2))
        s = s[8:]
        if showprogress:
            counter += 1
            bar.update(counter)

    return bytes(b)


def intarray_to_bytes(int_list, length, showprogress=False):
    bitstring = ''
    if showprogress:
        bar = progressbar.ProgressBar(max_value=progressbar.UnknownLength)
        counter = 0

    print('\n-- Generating bitarrays')
    for i in range(len(int_list)):
        binval = bin(int_list[i])[2:]

        binlen = bin(len(binval))[2:]
        binlen = fill_bitstring(binlen, length)

        binary = binlen + binval
        bitstring += binary

        if showprogress:
            counter += 1
            bar.update(counter)

    print('\n\n-- Generating bytecode')
    return bitstring_to_bytes(bitstring, showprogress)


def fill_bitstring(binary, zeros):
    return '0'*(zeros - len(binary)) + binary
