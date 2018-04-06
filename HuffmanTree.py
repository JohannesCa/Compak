from heapq import heappush, heappop


def updateTree(char_freqs, verbose=False):
    new_tree = []
    min_heap = []
    for symbol in char_freqs:
        heappush(min_heap, [char_freqs[symbol], [symbol]])

    if verbose:
        print('>> constructing tree')

    while min_heap:
        smallest0 = (heappop(min_heap))
        if verbose:
            print('poped ', smallest0)

        try:
            smallest1 = (heappop(min_heap))
            if verbose:
                print('poped ', smallest1)

        except IndexError:
            new_tree = smallest0
            break

        heappush(min_heap, [smallest0[0] + smallest1[0], smallest0[1] + smallest1[1], smallest0, smallest1])
        if verbose:
            print('pushing ', [smallest0[0] + smallest1[0], smallest0[1] + smallest1[1], smallest0, smallest1])

    if verbose:
        print('>> final tree: ', new_tree, '\n')

    return new_tree
