# Author: Conor Brady
# ID: 19448162
# Acknowledgement of DCU Academic integrity policy


def run(task, slice):
    print("Running task: [{}] {} {} for {} units".format(task.get('name'), str(task.get('priority')), str(task.get('CPU_burst')), str(slice)))
