from math import lcm

def calculate_lcm(periods):
    if len(periods) == 1:
        return periods[0]
    return lcm(*periods)

# Utilization factor calculation
def calculate_utilization_factor(tasks):
    total_utilization = 0
    for task in tasks:
        total_utilization += task['burst_time'] / task['period']
    return total_utilization

# RM scheduling function using LCM
def rate_monotonic(tasks):
    utilization_factor = calculate_utilization_factor(tasks)
    if utilization_factor >= 1:
        print("Not schedulable. Utilization factor exceeds 1.")
        return None

    tasks.sort(key=lambda x: x['period'])

    periods = [task['period'] for task in tasks]
    max_period = calculate_lcm(periods)

    schedule = []
    current_time = 0

    for task in tasks:
        burst_time = task['burst_time']
        period = task['period']

        while current_time < max_period:
            if burst_time > 0:
                time_to_execute = min(burst_time, period - (current_time % period))
                schedule.append((task['task'], time_to_execute))
                burst_time -= time_to_execute
            else:
                break

            current_time += time_to_execute

    return schedule


# Sample tasks
tasks = [
    {'task': 'task1', 'burst_time': 3, 'deadline': 20, 'period': 20},
    {'task': 'task2', 'burst_time': 2, 'deadline': 5, 'period': 5},
    {'task': 'task3', 'burst_time': 2, 'deadline': 10, 'period': 10}
]

# Check if tasks are schedulable and execute RM scheduling if they are
result = rate_monotonic(tasks)
if result is not None:
    for task, time in result:
        print(f"Task {task} , {time}")