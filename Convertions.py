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
