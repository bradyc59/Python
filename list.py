# Author: Conor Brady
# ID: 19448162
# Acknowledgement of DCU Academic integrity policy


def insert(taskList, taskName, taskPriority, taskCpuBurst):
    taskList[taskName] = {'priority' : taskPriority, 'CPU_burst' : taskCpuBurst}


def delete(taskList, taskName):
    taskList.pop(taskName)


def traverse(taskList):
    for task in taskList:
        print(task, " ", taskList.get(task).get('priority'), " ", taskList.get(task).get('CPU_burst'))

