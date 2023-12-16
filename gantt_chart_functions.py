import streamlit as st
import plotly.figure_factory as ff


def edf_llf_gantt_chart(df):
    # Create a list to store the Gantt chart data
    gantt_data = []

    # Set a color for all tasks (e.g., blue)
    task_color = 'rgb(0, 0, 255)'

    # Iterate through the DataFrame and create Gantt chart data
    current_time_slot = 0
    for index, row in df.iterrows():
        task = row['task']
        duration = row['length']
        start_time = row['start']

        # Check if there is a gap between tasks
        if index > 0:
            previous_end_time = df.loc[index - 1, 'end']
            if start_time > previous_end_time:
                current_time_slot += start_time - previous_end_time

        # Skip tasks with a duration of 0
        if duration == 0:
            continue

        gantt_data.append(
            dict(Task=f'Task {task}', Start=current_time_slot, Finish=current_time_slot + duration,
                 Color=task_color))
        current_time_slot += duration

    # Create a Gantt chart figure
    fig = ff.create_gantt(
        gantt_data,
        show_colorbar=True,
        index_col='Task',
        group_tasks=True,
    )

    fig.update_layout(
        title_text='Gantt Chart Representation',
        xaxis_title='Time Slots',
        yaxis_title='Tasks',
        xaxis_type='linear',  # Set x-axis type to category
        xaxis=dict(range=[0, current_time_slot]),  # Set the range of x-axis
    )

    # Display the Gantt chart using Streamlit
    st.plotly_chart(fig)


def fcfs_sjf_preememptif_sjf_gantt_chart(c):
    # Create a list to store the Gantt chart data
    gantt_data = []

    # Set a color for all tasks (e.g., blue)
    task_color = 'rgb(0, 0, 255)'

    # Iterate through the gantt_representation and create Gantt chart data
    current_time_slot = 0
    for task, duration in c:
        if task == 'Task No Task':
            current_time_slot += duration
            continue  # Skip Task No Task
        gantt_data.append(
            dict(Task=task, Start=current_time_slot, Finish=current_time_slot + duration, Color=task_color))
        current_time_slot += duration

    # Create a Gantt chart figure
    fig = ff.create_gantt(
        gantt_data,
        show_colorbar=True,
        index_col='Task',
        group_tasks=True,
    )

    fig.update_layout(
        title_text='Gantt Chart Representation',
        xaxis_title='Time Slots',
        yaxis_title='Tasks',
        xaxis_type='linear',  # Set x-axis type to category
        xaxis=dict(range=[0, current_time_slot]),  # Set the range of x-axis
    )
    # Display the Gantt chart using Streamlit
    st.plotly_chart(fig)
