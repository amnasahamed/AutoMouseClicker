import tkinter as tk
from tkinter import ttk, messagebox
import pyautogui
import threading
import time
from datetime import datetime

# ------------------
# GLOBALS & SETTINGS
# ------------------
BACKGROUND_COLOR = "#F8F8F8"   # Light gray-ish background, reminiscent of macOS
ACCENT_COLOR     = "#007AFF"   # A typical "iOS blue" accent color
FONT_FAMILY      = "Helvetica" # Or "San Francisco" if you have it installed
FONT_SIZE_LABEL  = 11
FONT_SIZE_ENTRY  = 11
FONT_SIZE_BUTTON = 11

# We'll store scheduled tasks in a list of dictionaries
# Each task: {"hour": int, "minute": int, "second": int, "x": int, "y": int}
scheduled_tasks = []
automation_running = False

# ---------------
# HELPER FUNCTIONS
# ---------------
def pick_coordinates():
    """
    Captures current mouse position using PyAutoGUI and updates the coordinate fields.
    """
    # Minimize the root window so user can see the screen easily.
    root.iconify()
    messagebox.showinfo(
        title="Pick Coordinates",
        message="Place your mouse at the desired location. Click OK or press Enter to capture coordinates."
    )
    x, y = pyautogui.position()
    x_entry.delete(0, tk.END)
    x_entry.insert(0, str(x))
    y_entry.delete(0, tk.END)
    y_entry.insert(0, str(y))
    # Restore the window
    root.deiconify()


def add_task():
    """
    Adds a new click task to the schedule and updates the Treeview.
    """
    try:
        hour = int(hour_var.get())
        minute = int(minute_var.get())
        second = int(second_var.get())
        x_coord = int(x_entry.get())
        y_coord = int(y_entry.get())

        # Basic validation
        if not (0 <= hour < 24):
            raise ValueError("Hour must be between 0 and 23.")
        if not (0 <= minute < 60):
            raise ValueError("Minute must be between 0 and 59.")
        if not (0 <= second < 60):
            raise ValueError("Second must be between 0 and 59.")

        # Add to the global scheduled_tasks list
        task = {
            "hour": hour,
            "minute": minute,
            "second": second,
            "x": x_coord,
            "y": y_coord
        }
        scheduled_tasks.append(task)

        # Insert into Treeview
        task_tree.insert(
            "",
            tk.END,
            values=(f"{hour:02d}:{minute:02d}:{second:02d}", f"({x_coord}, {y_coord})")
        )

        # Clear entries for a fresh start
        minute_var.set("")
        second_var.set("")
        x_entry.delete(0, tk.END)
        y_entry.delete(0, tk.END)

        # Provide feedback
        messagebox.showinfo("Task Added", f"Task scheduled at {hour:02d}:{minute:02d}:{second:02d} for ({x_coord}, {y_coord}).")

    except ValueError as e:
        messagebox.showerror("Invalid Input", str(e))


def remove_task():
    """
    Removes the selected task from the schedule and Treeview.
    """
    selected_item = task_tree.selection()
    if not selected_item:
        messagebox.showwarning("No Selection", "Please select a task to remove.")
        return

    # Remove from Treeview
    for item in selected_item:
        # Find the task in scheduled_tasks
        item_values = task_tree.item(item, "values")  # e.g., ("HH:MM:SS", "(x, y)")
        task_time, coords = item_values
        # parse "HH:MM:SS" => hour, minute, second
        hh, mm, ss = [int(x) for x in task_time.split(":")]
        # parse "(x, y)"
        coords_str = coords.strip("()")
        xx, yy = [int(c) for c in coords_str.split(",")]

        # Remove from scheduled_tasks
        for t in scheduled_tasks[:]:
            if (t["hour"] == hh and t["minute"] == mm and t["second"] == ss and
                    t["x"] == xx and t["y"] == yy):
                scheduled_tasks.remove(t)

        # Remove item from Treeview
        task_tree.delete(item)


def start_automation():
    """
    Starts the background thread that checks and executes scheduled clicks.
    """
    global automation_running
    if automation_running:
        messagebox.showinfo("Already Running", "Automation is already running.")
        return

    automation_running = True

    def run_clicks():
        while automation_running:
            now = datetime.now()
            current_hour = now.hour
            current_minute = now.minute
            current_second = now.second

            # Copy the list to avoid modification issues during iteration
            for task in scheduled_tasks[:]:
                if (task["hour"] == current_hour and
                    task["minute"] == current_minute and
                    task["second"] == current_second):
                    # Perform the click
                    pyautogui.moveTo(task["x"], task["y"])
                    pyautogui.click()
                    # Remove the task so it doesn't repeat
                    scheduled_tasks.remove(task)

                    # Also remove from Treeview
                    for item in task_tree.get_children():
                        vals = task_tree.item(item, "values")
                        time_str, coords_str = vals
                        hh, mm, ss = [int(x) for x in time_str.split(":")]
                        coords_str = coords_str.strip("()")
                        xx, yy = [int(c) for c in coords_str.split(",")]
                        if (hh == task["hour"] and mm == task["minute"] and ss == task["second"] and
                                xx == task["x"] and yy == task["y"]):
                            task_tree.delete(item)
                            break
            time.sleep(1)

    thread = threading.Thread(target=run_clicks, daemon=True)
    thread.start()
    messagebox.showinfo("Automation Started", "Tasks will run in the background.")


def stop_automation():
    """
    Stops the background automation thread.
    """
    global automation_running
    if not automation_running:
        messagebox.showinfo("Not Running", "Automation is not currently running.")
        return

    automation_running = False
    messagebox.showinfo("Automation Stopped", "No more scheduled clicks will be performed.")

# -----------------
# MAIN APPLICATION
# -----------------
root = tk.Tk()
root.title("Apple-Inspired Auto Clicker")

# Configure the root window's background
root.configure(bg=BACKGROUND_COLOR)

# Make the window a bit bigger and centered
window_width, window_height = 600, 500
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_coord = (screen_width // 2) - (window_width // 2)
y_coord = (screen_height // 2) - (window_height // 2)
root.geometry(f"{window_width}x{window_height}+{x_coord}+{y_coord}")

# Use ttk style to get more modern widgets
style = ttk.Style()
style.theme_use("clam")

# Customize a bit of the style
style.configure("TFrame", background=BACKGROUND_COLOR)
style.configure("TLabel", background=BACKGROUND_COLOR, font=(FONT_FAMILY, FONT_SIZE_LABEL))
style.configure("TButton", font=(FONT_FAMILY, FONT_SIZE_BUTTON), foreground="white", background=ACCENT_COLOR)
style.map("TButton",
          background=[("active", "#005BBB"), ("disabled", "#cccccc")])

# ---------------
# TOP TITLE FRAME
# ---------------
title_frame = ttk.Frame(root)
title_frame.pack(fill="x", pady=(20, 10))

title_label = ttk.Label(
    title_frame,
    text="Automatic Mouse Clicker",
    font=(FONT_FAMILY, 18, "bold"),
    foreground="#333333"
)
title_label.pack()

subtitle_label = ttk.Label(
    title_frame,
    text="Simple, intuitive, and elegant—schedule clicks with ease",
    font=(FONT_FAMILY, 12),
    foreground="#555555"
)
subtitle_label.pack()

# ---------------
# SCHEDULING FRAME
# ---------------
schedule_frame = ttk.Frame(root)
schedule_frame.pack(pady=10, padx=20, fill="x")

# Time inputs
time_label = ttk.Label(schedule_frame, text="Schedule Time (H:M:S):")
time_label.grid(row=0, column=0, padx=(0, 10), pady=(0,5), sticky="w")

hour_var = tk.StringVar()
minute_var = tk.StringVar()
second_var = tk.StringVar()

hour_entry = ttk.Entry(schedule_frame, width=5, textvariable=hour_var, font=(FONT_FAMILY, FONT_SIZE_ENTRY))
hour_entry.grid(row=0, column=1, padx=2, pady=5, sticky="w")
hour_entry.insert(0, "0")

minute_entry = ttk.Entry(schedule_frame, width=5, textvariable=minute_var, font=(FONT_FAMILY, FONT_SIZE_ENTRY))
minute_entry.grid(row=0, column=2, padx=2, pady=5, sticky="w")
minute_entry.insert(0, "0")

second_entry = ttk.Entry(schedule_frame, width=5, textvariable=second_var, font=(FONT_FAMILY, FONT_SIZE_ENTRY))
second_entry.grid(row=0, column=3, padx=2, pady=5, sticky="w")
second_entry.insert(0, "0")

# Coordinate inputs
coord_label = ttk.Label(schedule_frame, text="Click Coordinates (X,Y):")
coord_label.grid(row=1, column=0, padx=(0,10), pady=(5,0), sticky="w")

x_entry = ttk.Entry(schedule_frame, width=8, font=(FONT_FAMILY, FONT_SIZE_ENTRY))
x_entry.grid(row=1, column=1, padx=2, pady=5, sticky="w")

y_entry = ttk.Entry(schedule_frame, width=8, font=(FONT_FAMILY, FONT_SIZE_ENTRY))
y_entry.grid(row=1, column=2, padx=2, pady=5, sticky="w")

pick_btn = ttk.Button(schedule_frame, text="Pick Coordinates", command=pick_coordinates)
pick_btn.grid(row=1, column=3, padx=5, pady=5)

# Add Task Button
add_task_btn = ttk.Button(schedule_frame, text="Add to Schedule", command=add_task)
add_task_btn.grid(row=2, column=0, columnspan=4, pady=(10,0), sticky="ew")

# --------
# TASK LIST
# --------
list_frame = ttk.Frame(root)
list_frame.pack(pady=10, padx=20, fill="both", expand=True)

task_label = ttk.Label(list_frame, text="Scheduled Tasks:")
task_label.pack(anchor="w")

columns = ("Time", "Coordinates")
task_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=8)
task_tree.heading("Time", text="Time (H:M:S)")
task_tree.heading("Coordinates", text="Coordinates (X, Y)")
task_tree.pack(fill="both", expand=True, pady=5)

# Remove Task Button
remove_task_btn = ttk.Button(list_frame, text="Remove Selected Task", command=remove_task)
remove_task_btn.pack(anchor="e", pady=(0, 10))

# ---------------
# CONTROL BUTTONS
# ---------------
control_frame = ttk.Frame(root)
control_frame.pack(pady=(0, 20))

start_btn = ttk.Button(control_frame, text="Start Automation", command=start_automation)
start_btn.grid(row=0, column=0, padx=10)

stop_btn = ttk.Button(control_frame, text="Stop Automation", command=stop_automation)
stop_btn.grid(row=0, column=1, padx=10)

# ------------
# MAINLOOP
# ------------
root.mainloop()
