# app.py
import streamlit as st
from FCFS import fcfs
from SJF_without_preemption import sjf_without_preemption
from SJF_with_preemption import sjf_with_preemption
from RM import rate_monotonic
from DM import deadline_monotonic
from EDF import edf
import pandas as pd
from gantt_chart_functions import fcfs_sjf_preememptif_sjf_gantt_chart
from gantt_chart_functions import edf_llf_gantt_chart


def fcfsOrSJF_page(algorithm):
    st.subheader(f"{algorithm} Scheduling Algorithm")
    # Initialize the data in session state
    if "data" not in st.session_state:
        st.session_state["data"] = {
            "Task": [],
            "Burst Time": [],
            "Arrival Time": []
        }

    data = st.session_state["data"]

    with st.form("Input Data"):
        # Display the current data
        st.table(data)

        # Allow adding new rows
        new_burst_time = st.number_input("Enter Burst Time:")
        new_arrival_time = st.number_input("Enter Arrival Time:")
        add_button = st.form_submit_button("Add")

        if add_button:
            # Add new row to the data
            data["Task"].append("T" + str(len(st.session_state.data["Arrival Time"])))
            data["Burst Time"].append(new_burst_time)
            data["Arrival Time"].append(new_arrival_time)
            st.session_state["data"] = data  # Update session state

            # Update the displayed table
            st.table(data)

    if st.button(f"Run {algorithm}"):
        # Extract the lists of burst time and arrival time from the "data" dictionary
        tasks = st.session_state.data["Task"]
        burst_times = st.session_state.data["Burst Time"]
        arrival_times = st.session_state.data["Arrival Time"]

        # Create a list of dictionaries representing processes
        processes = [
            {"Process ID": i + 1, "Task": tasks[i], "Arrival Time": arrival_times[i],
             "Burst Time": burst_times[i]}
            for i in range(len(burst_times))
        ]
        if algorithm == "FCFS":
            a, b, c = fcfs(processes)
        elif algorithm == "SJF Without Preemption":
            a, b, c = sjf_without_preemption(processes)
        else:
            a, b, c = sjf_with_preemption(processes)

        st.subheader("Response :")
        st.text(f"waiting_times: {a}, average_waiting_time: {b}")
        fcfs_sjf_preememptif_sjf_gantt_chart(c)

def dm_rm_edf_page(algorithm):
    st.subheader(f"{algorithm} Scheduling Algorithm")
    # Initialize the data in session state
    if "data" not in st.session_state:
        st.session_state["data"] = {
            "Task": [],
            "Arrival Time": [],
            "Burst Time": [],
            "Deadline": [],
            "Period": []
        }

    data = st.session_state["data"]

    with st.form("Input Data"):
        # Display the current data
        st.table(data)

        # Allow adding new rows
        new_arrival_time = st.number_input("Enter Arrival Time:")
        new_burst_time = st.number_input("Enter Burst Time:")
        new_deadline = st.number_input("Enter Deadline:")
        new_period = st.number_input("Enter Period:")
        add_button = st.form_submit_button("Add")

        if add_button:
            # Add new row to the data
            data["Task"].append("T" + str(len(st.session_state.data["Arrival Time"])))
            data["Arrival Time"].append(new_arrival_time)
            data["Burst Time"].append(new_burst_time)
            data["Deadline"].append(new_deadline)
            data["Period"].append(new_period)
            st.session_state["data"] = data  # Update session state

            # Update the displayed table
            st.table(data)

    if st.button(f"Run {algorithm}"):
        # Extract the lists of burst time and arrival time from the "data" dictionary
        tasks = st.session_state.data["Task"]
        arrival_times = st.session_state.data["Arrival Time"]
        burst_times = st.session_state.data["Burst Time"]
        deadlines = st.session_state.data["Deadline"]
        periods = st.session_state.data["Period"]

        # Create a list of dictionaries representing processes
        processes = [
            {"Process ID": i + 1, "Task": tasks[i], "Arrival Time": arrival_times[i],
             "Burst Time": burst_times[i], "Deadline": deadlines[i], "Period": periods[i]}
            for i in range(len(burst_times))
        ]
        if algorithm == "RM":
            a, b, c = rate_monotonic(processes)
        elif algorithm == "DM":
            a, b, c = deadline_monotonic(processes)
        elif algorithm == "EDF":
            # a, b, c = edf(processes)
            b, c = edf(processes)
        else:
            print("later")

        st.subheader("Response :")
        # st.text(f"waiting_times: {a}, average_waiting_time: {b}, gantt: {c}")
        st.text(f"{b}")
        df = pd.DataFrame(c)

        edf_llf_gantt_chart(df)




def main():
    st.title("Scheduling Algorithm Simulator")

    # Sidebar
    selected_algorithm = st.sidebar.selectbox("Select Scheduling Algorithm",
                                              ["EDF", "FCFS", "SJF Without Preemption", "SJF With Preemption", "DM",
                                               "RM", "LLF"])

    # Main page content
    if selected_algorithm == "FCFS" or selected_algorithm == "SJF Without Preemption" or selected_algorithm == "SJF With Preemption":
        fcfsOrSJF_page(selected_algorithm)
    else:
        dm_rm_edf_page(selected_algorithm)


if __name__ == "__main__":
    main()
