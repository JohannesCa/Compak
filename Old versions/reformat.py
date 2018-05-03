def reformat_dict(d):
    ret = dict()

    for key, value in d.items():
        aux = key.split('|')
        aux = [int(x) for x in aux]
        ret.update({value: aux})

    return ret
