# Author: Conor Brady
# ID: 19448162
# Acknowledgement of DCU Academic integrity policy


import sys
import list
import schedule_fcfs
import schedule_priority
import schedule_sjf


def main():
    taskList = {}

    try: #try execute
        txt_file = open(sys.argv[1], 'r') #opening text file
        tasks = txt_file.read().splitlines() #reading from text file
        txt_file.close() # closes text file

        for task in tasks:
            new_task = task.split(', ') #splits after every comma
            taskList[new_task[0]] = {'name': new_task[0], 'priority': int(new_task[1]), 'CPU_burst': int(new_task[2])} # assinging dictionary names to values
    except FileNotFoundError: #if a filenotfounderror is thrown execute this
        print("It appears that this file does not exist, please enter a valid file name.")

    # calling functions
    schedule_fcfs.fcfs(taskList)
    schedule_priority.priority(taskList)
    schedule_sjf.sjf(taskList)


if __name__ == "__main__":
    main()