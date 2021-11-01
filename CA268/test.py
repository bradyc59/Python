import sys
from labexam import findmax
from LinkedList import LinkedList

def printlist(lst):
    ptr = lst.head;
    while ptr != None:
        print(str(ptr.item) + " -> ", end="")
        ptr = ptr.next
    print("None")

def main():
    # Read each set
    line = sys.stdin.readline()
    items = line.strip().split()
    intitems = [int(x) for x in items] # make a list of integers

    # Add the integers to the list
    linklist = LinkedList()

    # Add the integers to the linked list
    for item in intitems:
        linklist.add(item)

    printlist(linklist)
    print("The max is " + str(findmax(linklist)))

if __name__ == "__main__":
    main()