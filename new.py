from tkinter import *
import time  # time library
import winsound  # Windows sound
import tkinter.messagebox # Import messagebox module

root = Tk()  # creates a window
root.title("Timer")  # Creates a title
root.geometry("400x700")  # Increased window height to accommodate new elements
root.config(bg="#2E2E2E")
root.resizable(False, False)    # it helps to do not size the window

heading = Label(root, text="Timer", font="arial 30 bold", bg="#2E2E2E", fg="#ea3548")
heading.pack(pady=10)

Label(root, font=("arial", 15, "bold"), text="Current time: ", bg="#2E2E2E", fg="#FFFFFF").place(x=65, y=70)

def clock():
    clock_time = time.strftime('%H:%M:%S %p')
    current_time.config(text=clock_time)
    current_time.after(1000, clock)

current_time = Label(root, font=("arial", 15, "bold"), text="", fg="#000", bg="#fff")
current_time.place(x=195, y=70)
clock()
# It creat the exact time

hrs_var = StringVar()
Entry(root, textvariable=hrs_var, width=2, font="arial 50", fg="#000", bg="#fff", bd=0).place(x=30, y=155)
hrs_var.set("00")

mins_var = StringVar()
Entry(root, textvariable=mins_var, width=2, font="arial 50", fg="#000", bg="#fff", bd=0).place(x=150, y=155)
mins_var.set("00")

sec_var = StringVar()
Entry(root, textvariable=sec_var, width=2, font="arial 50", fg="#000", bg="#fff", bd=0).place(x=270, y=155)
sec_var.set("00")

Label(root, text="hours", font="arial 12", bg="#2E2E2E", fg="#FFFFFF").place(x=105, y=200)
Label(root, text="min", font="arial 12", bg="#2E2E2E", fg="#FFFFFF").place(x=225, y=200)
Label(root, text="sec", font="arial 12", bg="#2E2E2E", fg="#FFFFFF").place(x=345, y=200)

# Section for adding custom activities
activity_label = Label(root, text="Activity Name:", font="arial 12", bg="#2E2E2E", fg="#FFFFFF")
activity_label.place(x=30, y=250)
activity_entry = Entry(root, width=25, font="arial 12", bg="#fff", fg="#000")
activity_entry.place(x=150, y=250)

duration_label = Label(root, text="Duration (H:M:S):", font="arial 12", bg="#2E2E2E", fg="#FFFFFF")
duration_label.place(x=30, y=280)
duration_entry = Entry(root, width=15, font="arial 12", bg="#fff", fg="#000")
duration_entry.place(x=180, y=280)

custom_buttons_frame = Frame(root, bg="#2E2E2E")
custom_buttons_frame.place(x=10, y=320, width=380, height=150) # Frame to hold custom buttons

custom_activities = {} # Dictionary to store activity names and durations
button_row = 0
button_col = 0

def refresh_custom_buttons():
    global button_col, button_row
    # Destroy all existing buttons in the frame
    for widget in custom_buttons_frame.winfo_children():
        widget.destroy()

    # Reset grid counters
    button_row = 0
    button_col = 0

    # Recreate buttons from the custom_activities dictionary
    for activity, duration in custom_activities.items():
        new_button = Button(custom_buttons_frame, text=activity, bg="#424242", fg="#FFFFFF", bd=0, width=10, height=2,
                             font="arial 10 bold", command=lambda act=activity: start_custom_timer(custom_activities[act]))
        new_button.grid(row=button_row, column=button_col, padx=5, pady=5)

        button_col += 1
        if button_col > 2:
            button_col = 0
            button_row += 1

def add_activity():
    global button_col
    global button_row
    activity = activity_entry.get().strip()
    duration_str = duration_entry.get().strip()

    if not activity:
        tkinter.messagebox.showwarning("Input Error", "Please enter an activity name.", parent=root)
        return

    try:
        h, m, s = map(int, duration_str.split(':'))
        total_seconds = h * 3600 + m * 60 + s
        if total_seconds <= 0:
            tkinter.messagebox.showwarning("Input Error", "Duration must be greater than 0.", parent=root)
            return

        if activity in custom_activities:
            response = tkinter.messagebox.askyesno("Activity Exists",
                                                   f"Activity '{activity}' already exists. Overwrite duration?",
                                                   parent=root)
            if not response:
                return

        custom_activities[activity] = total_seconds
        refresh_custom_buttons()

        activity_entry.delete(0, END)
        duration_entry.delete(0, END)

    except ValueError:
        tkinter.messagebox.showerror("Input Error", "Invalid duration format. Please use H:M:S (e.g., 01:30:00).", parent=root)
    except Exception as e:
        tkinter.messagebox.showerror("Error", f"An unexpected error occurred: {e}", parent=root)

add_button = Button(root, text="Add Activity", bg="#ea3548", bd=0, fg="#FFFFFF", width=15, height=1, font="arial 10 bold", command=add_activity)
add_button.place(x=130, y=500)

timer_running = False   # Flag to control the timer
stop_flag = False   # Flag to signal a stop request
paused = False  # Flag to control the pause state
current_after_id = None # Keep track of the after ID to cancel previous timers

def start_custom_timer(duration):
    global timer_running
    global stop_flag
    global paused
    global current_after_id

    # Cancel any previously scheduled root.after call if a timer is already running
    if timer_running:
        if current_after_id is not None:
            root.after_cancel(current_after_id)
            current_after_id = None
        # Also ensure the visual state is reset properly
        hrs_var.set("00")
        mins_var.set("00")
        sec_var.set("00")


    timer_running = True
    stop_flag = False
    paused = False
    # Ensure pause/resume buttons are correctly shown/hidden on start
    pause_button.place(x=200, y=550)
    resume_button.place_forget()


    def update_timer(remaining_time):
        global current_after_id
        global timer_running
        global stop_flag
        global paused

        if stop_flag:
            timer_running = False
            pause_button.place(x=200, y=550)
            resume_button.place_forget()
            current_after_id = None
            return

        if not paused:
            hour = remaining_time // 3600
            minute = (remaining_time % 3600) // 60
            second = remaining_time % 60

            hrs_var.set(str(hour).zfill(2))
            mins_var.set(str(minute).zfill(2))
            sec_var.set(str(second).zfill(2))

            if remaining_time > 0:
                current_after_id = root.after(1000, update_timer, remaining_time - 1)
            else: # Timer finished
                timer_running = False
                winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
                hrs_var.set("00")
                mins_var.set("00")
                sec_var.set("00")
                pause_button.place_forget()
                resume_button.place_forget()
                current_after_id = None
        else:
            current_after_id = root.after(100, update_timer, remaining_time)

    update_timer(duration)

def Stop():
    global stop_flag
    global timer_running
    global current_after_id

    stop_flag = True
    timer_running = False

    if current_after_id is not None:
        root.after_cancel(current_after_id)
        current_after_id = None

    hrs_var.set("00")
    mins_var.set("00")
    sec_var.set("00")
    pause_button.place_forget() # When stopped, both pause and resume should be hidden
    resume_button.place_forget()

def Pause():
    global paused
    paused = True
    pause_button.place_forget()
    resume_button.place(x=200, y=550) # Adjusted placement

def Resume():
    global paused
    paused = False

# --- MODIFIED BUTTON COLORS ---
button = Button(root, text="Start", bg="#4CAF50", bd=0, fg="#FFFFFF", width=20, height=2, font="arial 10 bold", command=lambda: start_custom_timer(int(hrs_var.get()) * 3600 + int(mins_var.get()) * 60 + int(sec_var.get())))
button.place(x=30, y=550) # Adjusted placement

stop_button = Button(root, text="Stop", bg="#F44336", bd=0, fg="#FFFFFF", width=20, height=2, font="arial 10 bold", command=Stop)
stop_button.place(x=200, y=600) # Keep stop button at the original place

pause_button = Button(root, text="Pause", bg="#FFC107", bd=0, fg="#000000", width=20, height=2, font="arial 10 bold", command=Pause) # Changed fg to black for contrast
pause_button.place(x=200, y=550) # Initially hidden (adjusted placement handled by start_custom_timer)

resume_button = Button(root, text="Resume", bg="#2196F3", bd=0, fg="#FFFFFF", width=20, height=2, font="arial 10 bold", command=Resume)
resume_button.place_forget() # Initially hidden

root.mainloop()