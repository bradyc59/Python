def insertion_sort(lst):
    compare = 0
    move = 0
    if len(lst) == 0:
        return

    # Find the smallest element
    min_index = 0
    for i in range(1, len(lst)):
        compare = compare + 1
        if lst[i] < lst[min_index]:
            min_index = i;

    # Move smallest to the front (swap elements min_index and 0)
    lst[0], lst[min_index] = lst[min_index], lst[0]
    move = move + 3

    # Now, with the smallest in the front, we don't need to check i in the inner loop
    
    # At each pass ensure that that section is sorted (start at 2, cos smallest already in position).
    for todo in range(2, len(lst)):
        # Find correct position for lst[todo]
        store = lst[todo]
        i = todo
        compare = compare + 1
        while store < lst[i-1]: # Don't need to check i > 0
            lst[i] = lst[i-1] # Make space for the item
            i -= 1
            move = move + 1
            if i != 0:
                compare = compare + 1
        lst[i] = store  # Found the place for this item, plonk it in
        move = move + 2

    return compare, move
