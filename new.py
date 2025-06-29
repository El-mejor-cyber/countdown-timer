from tkinter import *
import tkinter.ttk as ttk  # Import for Notebook widget
import time
import winsound
import tkinter.messagebox

root = Tk()
root.title("Timer & Stopwatch")
root.geometry("400x700")
root.config(bg="#2E2E2E")
root.resizable(False, False)

heading = Label(root, text="Utilities", font="arial 30 bold", bg="#2E2E2E", fg="#ea3548")
heading.pack(pady=10)

main_frame = Frame(root, bg="#2E2E2E")
main_frame.pack(expand=True, fill="both", padx=10, pady=5)

# --- Create a Notebook (Tabs) for organization ---
notebook_style = ttk.Style()
notebook_style.configure('TNotebook.Tab', font=('arial', '12', 'bold'), padding=[15, 5])
notebook_style.configure('TNotebook', background='#2E2E2E', borderwidth=0)
notebook_style.map(
    "TNotebook.Tab",
    background=[("selected", "#424242"), ("active", "#555555")], 
    foreground=[("selected", "black"), ("!selected", "gray")]  
)
notebook = ttk.Notebook(main_frame, style='TNotebook') 
notebook.pack(expand=True, fill="both") 

# --- Create Frames for each tab ---
timer_frame = Frame(notebook, bg="#2E2E2E")
stopwatch_frame = Frame(notebook, bg="#2E2E2E")

timer_frame.pack(fill="both", expand=True)
stopwatch_frame.pack(fill="both", expand=True)

notebook.add(timer_frame, text="Timer")
notebook.add(stopwatch_frame, text="Stopwatch")

 #TIMER TAB CODE 


# Note: All widgets are now children of `timer_frame` instead of `root`
Label(timer_frame, font=("arial", 15, "bold"), text="Current time: ", bg="#2E2E2E", fg="#FFFFFF").place(x=65, y=10)

def clock():
    clock_time = time.strftime('%H:%M:%S %p')
    current_time.config(text=clock_time)
    current_time.after(1000, clock)

current_time = Label(timer_frame, font=("arial", 15, "bold"), text="", fg="#000", bg="#fff")
current_time.place(x=195, y=10)
clock()

hrs_var = StringVar()
Entry(timer_frame, textvariable=hrs_var, width=2, font="arial 50", fg="#000", bg="#fff", bd=0).place(x=30, y=85)
hrs_var.set("00")

mins_var = StringVar()
Entry(timer_frame, textvariable=mins_var, width=2, font="arial 50", fg="#000", bg="#fff", bd=0).place(x=150, y=85)
mins_var.set("00")

sec_var = StringVar()
Entry(timer_frame, textvariable=sec_var, width=2, font="arial 50", fg="#000", bg="#fff", bd=0).place(x=270, y=85)
sec_var.set("00")

Label(timer_frame, text="hours", font="arial 12", bg="#2E2E2E", fg="#FFFFFF").place(x=105, y=130)
Label(timer_frame, text="min", font="arial 12", bg="#2E2E2E", fg="#FFFFFF").place(x=225, y=130)
Label(timer_frame, text="sec", font="arial 12", bg="#2E2E2E", fg="#FFFFFF").place(x=345, y=130)

activity_label = Label(timer_frame, text="Activity Name:", font="arial 12", bg="#2E2E2E", fg="#FFFFFF")
activity_label.place(x=30, y=180)
activity_entry = Entry(timer_frame, width=25, font="arial 12", bg="#fff", fg="#000")
activity_entry.place(x=150, y=180)

duration_label = Label(timer_frame, text="Duration (H:M:S):", font="arial 12", bg="#2E2E2E", fg="#FFFFFF")
duration_label.place(x=30, y=210)
duration_entry = Entry(timer_frame, width=15, font="arial 12", bg="#fff", fg="#000")
duration_entry.place(x=180, y=210)

custom_buttons_frame = Frame(timer_frame, bg="#2E2E2E")
custom_buttons_frame.place(x=10, y=250, width=380, height=150)

custom_activities = {}
button_row = 0
button_col = 0

def refresh_custom_buttons():
    global button_col, button_row
    for widget in custom_buttons_frame.winfo_children():
        widget.destroy()
    button_row, button_col = 0, 0
    for activity, duration in custom_activities.items():
        new_button = Button(custom_buttons_frame, text=activity, bg="#424242", fg="#FFFFFF", bd=0, width=10, height=2,
                             font="arial 10 bold", command=lambda act=activity: start_custom_timer(custom_activities[act]))
        new_button.grid(row=button_row, column=button_col, padx=5, pady=5)
        button_col += 1
        if button_col > 2:
            button_col = 0
            button_row += 1

def add_activity():
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
            if not tkinter.messagebox.askyesno("Activity Exists", f"Overwrite '{activity}'?", parent=root):
                return
        custom_activities[activity] = total_seconds
        refresh_custom_buttons()
        activity_entry.delete(0, END)
        duration_entry.delete(0, END)
    except ValueError:
        tkinter.messagebox.showerror("Input Error", "Invalid duration format. Use H:M:S.", parent=root)
    except Exception as e:
        tkinter.messagebox.showerror("Error", f"An unexpected error occurred: {e}", parent=root)

add_button = Button(timer_frame, text="Add Activity", bg="#ea3548", bd=0, fg="#FFFFFF", width=15, height=1, font="arial 10 bold", command=add_activity)
add_button.place(x=130, y=430)

timer_running = False
stop_flag = False
paused = False
current_after_id = None

def start_custom_timer(duration):
    global timer_running, stop_flag, paused, current_after_id
    if timer_running and current_after_id:
        root.after_cancel(current_after_id)
    timer_running = True
    stop_flag = False
    paused = False
    pause_button.place(x=200, y=480)
    resume_button.place_forget()
    update_timer(duration)

def update_timer(remaining_time):
    global current_after_id, timer_running, stop_flag, paused
    if stop_flag:
        timer_running = False
        pause_button.place(x=200, y=480)
        resume_button.place_forget()
        return
    if not paused:
        if remaining_time >= 0:
            hour = remaining_time // 3600
            minute = (remaining_time % 3600) // 60
            second = remaining_time % 60
            hrs_var.set(str(hour).zfill(2))
            mins_var.set(str(minute).zfill(2))
            sec_var.set(str(second).zfill(2))
            current_after_id = root.after(1000, update_timer, remaining_time - 1)
        else:
            timer_running = False
            winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
            tkinter.messagebox.showinfo("Timer Finished", "The timer has finished!", parent=root)
            hrs_var.set("00"); mins_var.set("00"); sec_var.set("00")
            pause_button.place(x=200, y=480)
            resume_button.place_forget()
    else:
        current_after_id = root.after(100, update_timer, remaining_time)

def Stop():
    global stop_flag, timer_running, current_after_id
    stop_flag = True
    timer_running = False
    if current_after_id:
        root.after_cancel(current_after_id)
    hrs_var.set("00"); mins_var.set("00"); sec_var.set("00")
    

def Pause():
    global paused
    paused = True
    pause_button.place_forget()
    resume_button.place(x=200, y=480)

def Resume():
    global paused
    paused = False
    resume_button.place_forget()
    pause_button.place(x=200, y=480)

button = Button(timer_frame, text="Start", bg="#4CAF50", bd=0, fg="#FFFFFF", width=20, height=2, font="arial 10 bold", command=lambda: start_custom_timer(int(hrs_var.get()) * 3600 + int(mins_var.get()) * 60 + int(sec_var.get())))
button.place(x=30, y=480)

stop_button = Button(timer_frame, text="Stop", bg="#F44336", bd=0, fg="#FFFFFF", width=20, height=2, font="arial 10 bold", command=Stop)
stop_button.place(x=200, y=530)

pause_button = Button(timer_frame, text="Pause", bg="#FFC107", bd=0, fg="#000000", width=20, height=2, font="arial 10 bold", command=Pause)
resume_button = Button(timer_frame, text="Resume", bg="#2196F3", bd=0, fg="#FFFFFF", width=20, height=2, font="arial 10 bold", command=Resume)
pause_button.place(x=200, y=480)
resume_button.place_forget()


# STOPWATCH TAB CODE 


# --- Stopwatch State Variables ---
stopwatch_running = False
stopwatch_start_time = 0
elapsed_time_before_pause = 0
stopwatch_after_id = None
lap_num = 1

# --- Stopwatch Display ---
stopwatch_display = Label(stopwatch_frame, text="00:00:00.0", font=("arial", 60, "bold"), bg="#2E2E2E", fg="#FFFFFF")
stopwatch_display.pack(pady=20)

# --- Lap Times Display ---
lap_frame = Frame(stopwatch_frame, bg="#2E2E2E")
lap_frame.pack(pady=10, fill=BOTH, expand=True)

lap_box = Listbox(lap_frame, font=("arial", 12), bg="#424242", fg="#FFFFFF", bd=0, highlightthickness=0, selectbackground="#ea3548")
lap_box.pack(side=LEFT, fill=BOTH, expand=True, padx=(20,0))

lap_scrollbar = Scrollbar(lap_frame, orient=VERTICAL, command=lap_box.yview)
lap_scrollbar.pack(side=RIGHT, fill=Y, padx=(0,20))
lap_box.config(yscrollcommand=lap_scrollbar.set)

# --- Stopwatch Functions ---
def update_stopwatch():
    global stopwatch_after_id
    if stopwatch_running:
        current_elapsed = time.time() - stopwatch_start_time
        total_elapsed = elapsed_time_before_pause + current_elapsed

        # Format time: MM:SS.Tenths
        minutes = int(total_elapsed // 60)
        seconds = int(total_elapsed % 60)
        tenths = int((total_elapsed * 10) % 10)
        
        # You can add hours if needed:
        hours = int(total_elapsed // 3600)
        minutes_in_hour = int((total_elapsed % 3600) // 60)
        
        stopwatch_display.config(text=f"{hours:02d}:{minutes_in_hour:02d}:{seconds:02d}.{tenths}")
        
        stopwatch_after_id = stopwatch_frame.after(100, update_stopwatch)

def start_stopwatch():
    global stopwatch_running, stopwatch_start_time
    stopwatch_running = True
    stopwatch_start_time = time.time()
    update_stopwatch()
    # Update button states
    start_stop_button.config(text="Stop", command=stop_stopwatch, bg="#F44336")
    lap_reset_button.config(text="Lap", command=lap_stopwatch, state=NORMAL, bg="#2196F3")

def stop_stopwatch():
    global stopwatch_running, elapsed_time_before_pause, stopwatch_after_id
    stopwatch_running = False
    elapsed_time_before_pause += time.time() - stopwatch_start_time
    if stopwatch_after_id:
        stopwatch_frame.after_cancel(stopwatch_after_id)
    # Update button states
    start_stop_button.config(text="Start", command=start_stopwatch, bg="#4CAF50")
    lap_reset_button.config(text="Reset", command=reset_stopwatch, state=NORMAL, bg="#FFC107", fg="#000000")
    
def reset_stopwatch():
    global stopwatch_running, elapsed_time_before_pause, stopwatch_after_id, lap_num
    if stopwatch_running: # Stop it first if it's running
        stop_stopwatch()
    
    elapsed_time_before_pause = 0
    lap_num = 1
    stopwatch_display.config(text="00:00:00.0")
    lap_box.delete(0, END) # Clear lap times
    # Update button states
    lap_reset_button.config(state=DISABLED, bg="#424242", fg="#FFFFFF") # Disable reset until started
    start_stop_button.config(text="Start", command=start_stopwatch, bg="#4CAF50")

def lap_stopwatch():
    global lap_num
    if stopwatch_running:
        lap_time = stopwatch_display.cget("text")
        lap_box.insert(END, f"  Lap {lap_num}:   {lap_time}")
        lap_box.yview_moveto(1) # Auto-scroll to the bottom
        lap_num += 1

# --- Stopwatch Control Buttons ---
button_frame = Frame(stopwatch_frame, bg="#2E2E2E")
button_frame.pack(pady=20, fill=X, side=BOTTOM)
button_frame.columnconfigure((0, 1), weight=1) # Make columns expand equally

start_stop_button = Button(button_frame, text="Start", bg="#4CAF50", bd=0, fg="#FFFFFF", width=15, height=2, font="arial 10 bold", command=start_stopwatch)
start_stop_button.grid(row=0, column=0, padx=10)

lap_reset_button = Button(button_frame, text="Reset", bg="#424242", bd=0, fg="#FFFFFF", width=15, height=2, font="arial 10 bold", command=reset_stopwatch, state=DISABLED)
lap_reset_button.grid(row=0, column=1, padx=10)

# --- Start Main Event Loop ---
root.mainloop()
