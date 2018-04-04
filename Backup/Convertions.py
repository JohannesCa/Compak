def bitstring_to_bytes(s):
    if len(s) % 8 != 0:
        s = s + '0'*(8 - (len(s) % 8))

    b = []
    while s:
        sub = s[:8]
        b.append(int(sub, 2))
        s = s[8:]

    return bytes(b)
