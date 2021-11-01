def above_average(lst):

    average = sum(lst) / len(lst)

    return [n for n in lst if n > average]
