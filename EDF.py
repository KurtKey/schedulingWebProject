import pandas as pd
import numpy as np


def cpu_occupation(tasks):
    total_occupation = 0
    for task in tasks:
        total_occupation += task['Burst Time'] / task['Period']
    return total_occupation


def edf(tasks):
    total_occupation = 100*cpu_occupation(tasks)
    occupation_remark = ''
    timeline = [{'task': 0, 'start': 0, 'end': 0, 'length': 0}]
    if total_occupation > 100:
        occupation_remark = f'Tasks are not schedulable, CPU occupation is {total_occupation}%'
        return occupation_remark, pd.DataFrame(timeline)

    tasks = pd.DataFrame(tasks)  # Convert list of dictionaries to a DataFrame

    tasks['current_capacity'] = tasks['Burst Time']
    tasks['current_deadline'] = tasks['Deadline']
    timeline = []

    # build the timeline for the required time slots
    for i in range(np.lcm.reduce(tasks['Period'].astype(int))):
        # filter the completed tasks
        left_tasks = tasks[tasks['current_capacity'] > 0]

        if not left_tasks.empty:
            # find the task with the closest Deadline
            top_task = left_tasks.sort_values('current_deadline').index[0]

            # decrease the Burst Time of the current task by one
            tasks.at[top_task, 'current_capacity'] -= 1

            if timeline and timeline[-1]['task'] == top_task and timeline[-1]['end'] == i:
                # if the current task is the same as the last task, update its end time and length
                timeline[-1].update({'end': i + 1,
                                     'length': timeline[-1]['length'] + 1})
            else:
                # otherwise add the new task to the timeline
                timeline += [{'task': top_task,
                              'start': i,
                              'end': i + 1,
                              'length': 1}]

        # update the Burst Time and the Deadline of newly arrived tasks
        arrived = tasks.index[(i + 1) % tasks['Period'] == 0]
        tasks.loc[arrived, 'current_capacity'] = tasks.loc[arrived, 'Burst Time']
        tasks.loc[arrived, 'current_deadline'] = tasks.loc[arrived, 'current_deadline'] + tasks.loc[arrived, 'Period']
        occupation_remark = f'Tasks are schedulable, CPU occupation is {total_occupation}%'
    return occupation_remark, pd.DataFrame(timeline)
