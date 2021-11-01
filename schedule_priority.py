# Author: Conor Brady
# ID: 19448162
# Acknowledgement of DCU Academic integrity policy


import CPU

def priority(taskList):
    waitTime = 0
    TAT = 0
    allTAT = 0
    avgWaitTime = 0
    allWaitTime = 0
    i = 0
    n = len(taskList) #length of task list

    print("Priority scheduling:")

    for task in sorted(taskList, key=lambda x: taskList[x]['priority']): #sorting the file by priority from lowest to highest

        i = i + 1

        x = taskList.get(task).get('CPU_burst') #assigning x to burst time

        CPU.run(taskList.get(task), x) #running cpu

        if i != n:
            TAT = waitTime + taskList.get(task).get('CPU_burst') #calculating turn around time
            allWaitTime = allWaitTime + waitTime
            allTAT = allTAT + TAT
            waitTime = taskList.get(task).get('CPU_burst') + waitTime #calculating wait time

    avgWaitTime = allWaitTime / n
    avgTAT = allTAT / n #getting average of both wait time and turn around time

    print("\nAverage wait time: ", avgWaitTime)
    print("Average turn around time: ", avgTAT)
    print("\n")