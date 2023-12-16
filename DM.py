from math import gcd

# LCM function
def lcm(x, y):
    return x * y // gcd(x, y)

def calculate_lcm(periods):
    if len(periods) == 1:
        return periods[0]
    lcm_value = lcm(periods[0], periods[1])
    for i in range(2, len(periods)):
        lcm_value = lcm(lcm_value, periods[i])
    return lcm_value

# Utilization factor calculation
def calculate_utilization_factor(tasks):
    total_utilization = 0
    for task in tasks:
        total_utilization += task['burst_time'] / task['period']
    return total_utilization

# DM scheduling function using LCM
def deadline_monotonic(tasks):
    utilization_factor = calculate_utilization_factor(tasks)
    if utilization_factor >= 1:
        print("Not schedulable. Utilization factor exceeds 1.")
        return None

    tasks.sort(key=lambda x: x['deadline'])
    periods = [task['period'] for task in tasks]
    max_period = calculate_lcm(periods)

    schedule = []
    current_time = 0

    for task in tasks:
        burst_time = task['burst_time']
        period = task['period']
        deadline = task['deadline']

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

# Execute DM scheduling and display the schedule
result = deadline_monotonic(tasks)
for task, time in result:
    print(f"Task {task} , {time}")
