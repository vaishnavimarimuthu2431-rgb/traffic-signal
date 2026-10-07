import tkinter as tk
import random
import csv
import os
from datetime import datetime


# ============================================================
# TRAFFIC SIGNAL MONITORING SYSTEM
# Advanced OS / Real-Time OS Project
# ============================================================

ROADS = ["Road 1", "Road 2", "Road 3", "Road 4"]

running = False
current_priority = None
countdown = 0
cycle_number = 0

# Store traffic information
traffic_data = {}

for road in ROADS:
    traffic_data[road] = {
        "vehicles": 0,
        "density": "LOW",
        "emergency": False,
        "green_time": 10,
        "signal": "RED"
    }


# ============================================================
# CALCULATE DENSITY
# ============================================================

def calculate_density(vehicles):

    if vehicles <= 15:
        return "LOW"

    elif vehicles <= 30:
        return "MEDIUM"

    else:
        return "HIGH"


# ============================================================
# CALCULATE GREEN TIME
# ============================================================

def calculate_green_time(vehicles, emergency):

    if emergency:
        return 15

    if vehicles <= 15:
        return 10

    elif vehicles <= 30:
        return 20

    else:
        return 30


# ============================================================
# CREATE CSV FILE
# ============================================================

def create_csv():

    if not os.path.exists("traffic_log.csv"):

        with open("traffic_log.csv", "w", newline="") as file:

            writer = csv.writer(file)

            writer.writerow([
                "Time",
                "Cycle",
                "Road",
                "Vehicles",
                "Density",
                "Emergency",
                "Signal",
                "Green_Time"
            ])


# ============================================================
# SAVE DATA
# ============================================================

def save_data():

    with open("traffic_log.csv", "a", newline="") as file:

        writer = csv.writer(file)

        current_time = datetime.now().strftime("%H:%M:%S")

        for road in ROADS:

            data = traffic_data[road]

            writer.writerow([
                current_time,
                cycle_number,
                road,
                data["vehicles"],
                data["density"],
                "YES" if data["emergency"] else "NO",
                data["signal"],
                data["green_time"]
            ])


# ============================================================
# GENERATE TRAFFIC
# ============================================================

def generate_traffic():

    global cycle_number

    cycle_number += 1

    for road in ROADS:

        vehicles = random.randint(5, 50)

        density = calculate_density(vehicles)

        # 20% chance of emergency
        emergency = random.random() < 0.20

        green_time = calculate_green_time(
            vehicles,
            emergency
        )

        traffic_data[road]["vehicles"] = vehicles
        traffic_data[road]["density"] = density
        traffic_data[road]["emergency"] = emergency
        traffic_data[road]["green_time"] = green_time
        traffic_data[road]["signal"] = "RED"

    choose_priority()

    # Set priority road GREEN
    set_green_signal()

    # Save correct signal state
    save_data()

    update_dashboard()


# ============================================================
# SELECT PRIORITY ROAD
# ============================================================

def choose_priority():

    global current_priority

    emergency_roads = []

    for road in ROADS:

        if traffic_data[road]["emergency"]:

            emergency_roads.append(road)

    # Emergency road gets highest priority
    if emergency_roads:

        current_priority = max(
            emergency_roads,
            key=lambda road: traffic_data[road]["vehicles"]
        )

    else:

        # Highest traffic gets priority
        current_priority = max(
            ROADS,
            key=lambda road: traffic_data[road]["vehicles"]
        )


# ============================================================
# SET GREEN SIGNAL
# ============================================================

def set_green_signal():

    for road in ROADS:

        traffic_data[road]["signal"] = "RED"

    if current_priority is not None:

        traffic_data[current_priority]["signal"] = "GREEN"


# ============================================================
# UPDATE DASHBOARD
# ============================================================

def update_dashboard():

    for i, road in enumerate(ROADS):

        data = traffic_data[road]

        vehicles = data["vehicles"]
        density = data["density"]
        emergency = data["emergency"]
        signal = data["signal"]

        # Vehicle count
        vehicle_labels[i].config(
            text=f"Vehicles: {vehicles}"
        )

        # Density
        density_labels[i].config(
            text=f"Density: {density}"
        )

        # Density color
        if density == "LOW":

            density_labels[i].config(
                fg="green"
            )

        elif density == "MEDIUM":

            density_labels[i].config(
                fg="orange"
            )

        else:

            density_labels[i].config(
                fg="red"
            )

        # Emergency
        if emergency:

            emergency_labels[i].config(
                text="EMERGENCY VEHICLE",
                fg="red"
            )

        else:

            emergency_labels[i].config(
                text="Normal Traffic",
                fg="gray"
            )

        # Signal
        update_signal_label(i, signal)

    # Priority information
    if current_priority is not None:

        data = traffic_data[current_priority]

        priority_label.config(
            text=f"Priority Road: {current_priority}"
        )

        traffic_level_label.config(
            text=f"Traffic Level: {data['density']}"
        )

        green_time_label.config(
            text=f"Green Time: {data['green_time']} sec"
        )

        if data["emergency"]:

            emergency_status_label.config(
                text="Emergency Priority: YES",
                fg="red"
            )

        else:

            emergency_status_label.config(
                text="Emergency Priority: NO",
                fg="gray"
            )

    else:

        priority_label.config(
            text="Priority Road: None"
        )

        traffic_level_label.config(
            text="Traffic Level: --"
        )

        green_time_label.config(
            text="Green Time: --"
        )

        emergency_status_label.config(
            text="Emergency Priority: --",
            fg="gray"
        )

    update_graph()


# ============================================================
# UPDATE SIGNAL LABEL
# ============================================================

def update_signal_label(index, signal):

    if signal == "GREEN":

        signal_labels[index].config(
            text="GREEN",
            fg="green"
        )

    elif signal == "YELLOW":

        signal_labels[index].config(
            text="YELLOW",
            fg="orange"
        )

    else:

        signal_labels[index].config(
            text="RED",
            fg="red"
        )


# ============================================================
# LIVE TRAFFIC GRAPH
# ============================================================

def update_graph():

    # Remove old bars
    for widget in graph_frame.winfo_children():

        widget.destroy()

    for road in ROADS:

        value = traffic_data[road]["vehicles"]

        density = traffic_data[road]["density"]

        row = tk.Frame(
            graph_frame,
            bg="white"
        )

        row.pack(
            fill="x",
            padx=10,
            pady=2
        )

        # Road name
        road_name = tk.Label(
            row,
            text=road,
            width=10,
            anchor="w",
            bg="white",
            font=("Arial", 9, "bold")
        )

        road_name.pack(side="left")

        # Bar color
        if density == "LOW":

            bar_color = "#2ecc71"

        elif density == "MEDIUM":

            bar_color = "#f1c40f"

        else:

            bar_color = "#e74c3c"

        # Bar width
        bar_width = max(20, value * 8)

        bar = tk.Frame(
            row,
            width=bar_width,
            height=18,
            bg=bar_color
        )

        bar.pack(side="left")

        bar.pack_propagate(False)

        # Vehicle number
        number = tk.Label(
            row,
            text=f"  {value}",
            bg="white",
            font=("Arial", 9, "bold")
        )

        number.pack(side="left")


# ============================================================
# START SYSTEM
# ============================================================

def start_system():

    global running
    global countdown

    if running:

        return

    running = True

    status_label.config(
        text="SYSTEM RUNNING",
        fg="green"
    )

    start_button.config(
        state="disabled"
    )

    stop_button.config(
        state="normal"
    )

    # Generate traffic
    generate_traffic()

    countdown = traffic_data[
        current_priority
    ]["green_time"]

    run_signal_cycle()


# ============================================================
# SIGNAL CYCLE
# ============================================================

def run_signal_cycle():

    global countdown

    if not running:

        return

    # Display GREEN
    update_dashboard()

    countdown_label.config(
        text=f"Green Time Remaining: {countdown} seconds"
    )

    if countdown > 0:

        countdown -= 1

        root.after(
            1000,
            run_signal_cycle
        )

    else:

        # Change GREEN to YELLOW
        if current_priority is not None:

            traffic_data[
                current_priority
            ]["signal"] = "YELLOW"

        update_dashboard()

        countdown_label.config(
            text="Yellow Signal: 2 seconds"
        )

        root.after(
            2000,
            change_to_red
        )


# ============================================================
# CHANGE YELLOW TO RED
# ============================================================

def change_to_red():

    if not running:

        return

    if current_priority is not None:

        traffic_data[
            current_priority
        ]["signal"] = "RED"

    update_dashboard()

    countdown_label.config(
        text="Signal cycle completed"
    )

    root.after(
        1500,
        next_cycle
    )


# ============================================================
# NEXT CYCLE
# ============================================================

def next_cycle():

    global countdown

    if not running:

        return

    generate_traffic()

    countdown = traffic_data[
        current_priority
    ]["green_time"]

    run_signal_cycle()


# ============================================================
# STOP SYSTEM
# ============================================================

def stop_system():

    global running
    global current_priority
    global countdown

    running = False

    current_priority = None

    countdown = 0

    # Set all signals RED
    for road in ROADS:

        traffic_data[road]["signal"] = "RED"

    # Update road displays
    for i in range(4):

        update_signal_label(
            i,
            "RED"
        )

    status_label.config(
        text="SYSTEM STOPPED",
        fg="red"
    )

    countdown_label.config(
        text="Green Time Remaining: --"
    )

    priority_label.config(
        text="Priority Road: None"
    )

    traffic_level_label.config(
        text="Traffic Level: --"
    )

    green_time_label.config(
        text="Green Time: --"
    )

    emergency_status_label.config(
        text="Emergency Priority: --",
        fg="gray"
    )

    start_button.config(
        state="normal"
    )

    stop_button.config(
        state="disabled"
    )


# ============================================================
# EXIT
# ============================================================

def exit_program():

    global running

    running = False

    root.destroy()


# ============================================================
# CREATE CSV
# ============================================================

create_csv()


# ============================================================
# MAIN WINDOW
# ============================================================

root = tk.Tk()

root.title(
    "Traffic Signal Monitoring System"
)

# IMPORTANT:
# Smaller height so buttons are visible
root.geometry(
    "1150x780"
)

root.minsize(
    1000,
    700
)

root.configure(
    bg="#eeeeee"
)


# ============================================================
# TITLE
# ============================================================

title_label = tk.Label(
    root,
    text="TRAFFIC SIGNAL MONITORING SYSTEM",
    font=("Arial", 22, "bold"),
    bg="#eeeeee"
)

title_label.pack(
    pady=(8, 2)
)


subtitle_label = tk.Label(
    root,
    text="Advanced OS / Real-Time OS Monitoring Project",
    font=("Arial", 11),
    bg="#eeeeee"
)

subtitle_label.pack()


# ============================================================
# ROAD FRAME
# ============================================================

roads_frame = tk.Frame(
    root,
    bg="#eeeeee"
)

roads_frame.pack(
    pady=8
)


# Lists
vehicle_labels = []
density_labels = []
emergency_labels = []
signal_labels = []


# ============================================================
# FOUR ROAD CARDS
# ============================================================

for i, road in enumerate(ROADS):

    frame = tk.LabelFrame(
        roads_frame,
        text=road,
        font=("Arial", 12, "bold"),
        width=250,
        height=190,
        bg="white",
        padx=8,
        pady=5
    )

    frame.grid(
        row=0,
        column=i,
        padx=5
    )

    frame.pack_propagate(False)

    # Signal
    signal_label = tk.Label(
        frame,
        text="RED",
        font=("Arial", 18, "bold"),
        bg="white",
        fg="red"
    )

    signal_label.pack(
        pady=6
    )

    signal_labels.append(
        signal_label
    )

    # Vehicles
    vehicle_label = tk.Label(
        frame,
        text="Vehicles: 0",
        font=("Arial", 11),
        bg="white"
    )

    vehicle_label.pack(
        pady=3
    )

    vehicle_labels.append(
        vehicle_label
    )

    # Density
    density_label = tk.Label(
        frame,
        text="Density: LOW",
        font=("Arial", 11, "bold"),
        bg="white",
        fg="green"
    )

    density_label.pack(
        pady=3
    )

    density_labels.append(
        density_label
    )

    # Emergency
    emergency_label = tk.Label(
        frame,
        text="Normal Traffic",
        font=("Arial", 10, "bold"),
        bg="white",
        fg="gray"
    )

    emergency_label.pack(
        pady=5
    )

    emergency_labels.append(
        emergency_label
    )


# ============================================================
# INFORMATION FRAME
# ============================================================

info_frame = tk.LabelFrame(
    root,
    text="Traffic Monitoring Information",
    font=("Arial", 11, "bold"),
    bg="white",
    padx=8,
    pady=5
)

info_frame.pack(
    fill="x",
    padx=30,
    pady=5
)


priority_label = tk.Label(
    info_frame,
    text="Priority Road: None",
    font=("Arial", 10, "bold"),
    bg="white"
)

priority_label.pack(
    side="left",
    padx=12
)


traffic_level_label = tk.Label(
    info_frame,
    text="Traffic Level: --",
    font=("Arial", 10),
    bg="white"
)

traffic_level_label.pack(
    side="left",
    padx=12
)


green_time_label = tk.Label(
    info_frame,
    text="Green Time: --",
    font=("Arial", 10),
    bg="white"
)

green_time_label.pack(
    side="left",
    padx=12
)


emergency_status_label = tk.Label(
    info_frame,
    text="Emergency Priority: --",
    font=("Arial", 10, "bold"),
    bg="white",
    fg="gray"
)

emergency_status_label.pack(
    side="left",
    padx=12
)


# ============================================================
# COUNTDOWN
# ============================================================

countdown_label = tk.Label(
    root,
    text="Green Time Remaining: --",
    font=("Arial", 14, "bold"),
    bg="#eeeeee"
)

countdown_label.pack(
    pady=4
)


# ============================================================
# GRAPH TITLE
# ============================================================

graph_title = tk.Label(
    root,
    text="LIVE TRAFFIC DENSITY",
    font=("Arial", 12, "bold"),
    bg="#eeeeee"
)

graph_title.pack(
    pady=2
)


# ============================================================
# GRAPH FRAME
# ============================================================

graph_frame = tk.Frame(
    root,
    bg="white",
    height=100
)

graph_frame.pack(
    fill="x",
    padx=100,
    pady=3
)

graph_frame.pack_propagate(False)


# ============================================================
# SYSTEM STATUS
# ============================================================

status_label = tk.Label(
    root,
    text="SYSTEM STOPPED",
    font=("Arial", 11, "bold"),
    fg="red",
    bg="#eeeeee"
)

status_label.pack(
    pady=3
)


# ============================================================
# BUTTON FRAME
# ============================================================

button_frame = tk.Frame(
    root,
    bg="#eeeeee"
)

button_frame.pack(
    pady=5
)


# ============================================================
# START BUTTON
# ============================================================

start_button = tk.Button(
    button_frame,
    text="START SYSTEM",
    font=("Arial", 11, "bold"),
    width=18,
    height=2,
    bg="#90ee90",
    command=start_system
)

start_button.grid(
    row=0,
    column=0,
    padx=8
)


# ============================================================
# STOP BUTTON
# ============================================================

stop_button = tk.Button(
    button_frame,
    text="STOP SYSTEM",
    font=("Arial", 11, "bold"),
    width=18,
    height=2,
    bg="#ff9999",
    command=stop_system,
    state="disabled"
)

stop_button.grid(
    row=0,
    column=1,
    padx=8
)


# ============================================================
# EXIT BUTTON
# ============================================================

exit_button = tk.Button(
    button_frame,
    text="EXIT",
    font=("Arial", 11, "bold"),
    width=18,
    height=2,
    bg="#dddddd",
    command=exit_program
)

exit_button.grid(
    row=0,
    column=2,
    padx=8
)


# ============================================================
# CLOSE WINDOW
# ============================================================

root.protocol(
    "WM_DELETE_WINDOW",
    exit_program
)


# ============================================================
# RUN PROGRAM
# ============================================================

root.mainloop()