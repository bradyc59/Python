#
#   Determine how many nodes are visited while searching for a particular value
#
def how_many_searched(val, bst = 0):
    if val is None:
        return bst
    return how_many_searched(val.left, how_many_searched(val.right, bst + 1))