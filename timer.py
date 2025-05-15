from tkinter import *
import time  # time library
import winsound  # Windows sound


root = Tk()  # creates a window
root.title("Timer")  # Creates a title
root.geometry("400x600")  # Decide the size/resolution of the window
root.config(bg="#2E2E2E")
root.resizable(False, False)    # it helps to do not size the window

heading = Label(root, text="Timer", font="arial 30 bold", bg="#2E2E2E",fg="#ea3548")
heading.pack(pady=10)

Label(root, font=("arial", 15, "bold"), text="Current time:", bg="#2E2E2E", fg="#FFFFFF").place(x=65, y=70)


def clock():
    clock_time = time.strftime('%H:%M:%S %p')
    current_time.config(text=clock_time)
    current_time.after(1000, clock)


current_time = Label(root, font=("arial", 15, "bold"), text="", fg="#000", bg="#fff")
current_time.place(x=190, y=70)
clock()
# It creat the exact time

hrs = StringVar()
Entry(root, textvariable=hrs, width=2, font="arial 50", fg="#000", bg="#fff", bd=0).place(x=30, y=155)
hrs.set("00")

mins = StringVar()
Entry(root, textvariable=mins, width=2, font="arial 50", fg="#000", bg="#fff", bd=0).place(x=150, y=155)
mins.set("00")

sec = StringVar()
Entry(root, textvariable=sec, width=2, font="arial 50", fg="#000", bg="#fff", bd=0).place(x=270, y=155)
sec.set("00")

Label(root, text="hours", font="arial 12", bg="#2E2E2E", fg="#FFFFFF").place(x=105, y=200)
Label(root, text="min", font="arial 12", bg="#2E2E2E", fg="#FFFFFF").place(x=225, y=200)
Label(root, text="sec", font="arial 12", bg="#2E2E2E", fg="#FFFFFF").place(x=345, y=200)

timer_running = False  # Flag to control the timer
stop_flag = False  # Flag to signal a stop request
paused = False  # Flag to control the pause state



def Timer():
    global timer_running
    global stop_flag
    global paused

    if not timer_running:
        try:
            times = int(hrs.get()) * 3600 + int(mins.get()) * 60 + int(sec.get())  # Conversion to total seconds
        except ValueError:
            return  # Handle cases where input is not a valid integer

        timer_running = True
        stop_flag = False
        paused = False  # Reset paused state when a new timer starts
        pause_button.place(x=200, y=450)  # Show pause button
        resume_button.place_forget()  # Hide resume button


        def update_timer(remaining_time):
            times = int(hrs.get()) * 3600 + int(mins.get()) * 60 + int(sec.get())
            global timer_running
            global stop_flag
            global paused
            if stop_flag:
                timer_running = False
                return

            if not paused:
                minute ,second=(remaining_time//60, remaining_time %60)

                hour=0
                if minute>60:
                  hour,minute=(minute//60,minute%60)

                sec.set(str(second).zfill(2))
                mins.set(str(minute).zfill(2))
                hrs.set(str(hour).zfill(2))
                if remaining_time>0:
                    root.after(1000, update_timer, remaining_time - 1)

                if(times==0):
                    timer_running = False
                    winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
                    sec.set("00")
                    mins.set("00")
                    hrs.set("00")
                    pause_button.place_forget() # Hide pause button when timer ends
                    resume_button.place_forget() # Hide resume button when timer ends
        
            else:
                root.after(100, update_timer, remaining_time) # Check again after 100 milliseconds


        update_timer(times)


def Stop():
    global stop_flag
    global timer_running
    stop_flag = True
    timer_running = False
    hrs.set("00")
    mins.set("00")
    sec.set("00")
    
def Pause():
    global paused
    paused = True
    pause_button.place_forget() # Hide pause button
    resume_button.place(x=200, y=450) # Show resume button


def Resume():
    global paused
    paused = False
    resume_button.place_forget() # Hide resume button
    pause_button.place(x=200, y=450) # Show pause button



button = Button(root, text="Start", bg="#ea3548", bd =0,fg="#FFFFFF", width=20, height=2, font="arial 10 bold", command=Timer)
button.place(x=30, y=400)

stop_button = Button(root, text="Stop", bg="#ea3548", bd=0, fg="#fff", width=20, height=2, font="arial 10 bold", command=Stop)
stop_button.place(x=200, y=400)

pause_button = Button(root, text="Pause", bg="#ea3548", bd=0, fg="#fff", width=20, height=2, font="arial 10 bold", command=Pause)
pause_button.place_forget() # Initially placed below the Stop button, but will be hidden

resume_button = Button(root, text="Resume", bg="#ea3548", bd=0, fg="#fff", width=20, height=2, font="arial 10 bold", command=Resume)
resume_button.place_forget() # Initially hidden


root.mainloop()