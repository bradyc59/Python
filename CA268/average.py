def above_average(lst):

    average = sum(lst) / len(lst)

    return [n for n in lst if n > average]

def main():
    lst = [1, 2, 3, 4]
    print(above_average(lst))

if __name__ == '__main__':
	main()
