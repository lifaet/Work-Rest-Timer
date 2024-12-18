import tkinter as tk
import time
import threading

paused = False
work_time = 0
break_time = 0

def countdown(count, label, color):
    global paused
    while count >= 0 and not paused:
        minutes, seconds = divmod(count, 60)
        label.config(text=f"{minutes:02d}:{seconds:02d}", fg=color)
        label.update()
        time.sleep(1)
        count -= 1

def toggle_pause(event=None):
    global paused
    paused = not paused
    pause_button.config(text="▶" if paused else "||")

def close_window():
    window.destroy()

def start_timer(event=None):
    global work_time, break_time
    if break_time_entry.get() == "":
        flash_entry(break_time_entry)
        return
    break_time = int(break_time_entry.get()) * 60
    work_time = int(work_time_entry.get()) * 60
    frame_entry.pack_forget()
    frame_label.pack(pady=2, padx=2)
    timer_thread = threading.Thread(target=countdown_cycle)
    timer_thread.daemon = True
    timer_thread.start()

def ask_break_time(event=None):
    global break_time_entry
    if work_time_entry.get() == "":
        flash_entry(work_time_entry)
        return
    work_time = int(work_time_entry.get()) * 60
    label_prompt.config(text="Break:")
    work_time_entry.grid_forget()
    break_time_entry = tk.Entry(frame_entry, width=5)
    break_time_entry.grid(row=0, column=1, padx=(0, 10))
    break_time_entry.bind("<Return>", start_timer)
    break_time_entry.bind("<space>", start_timer)
    submit_button.config(command=start_timer)
    break_time_entry.focus()

def flash_entry(entry):
    entry.config(bg="red")
    window.after(500, lambda: entry.config(bg="white"))

def ask_work_time():
    global work_time_entry, label_prompt, submit_button
    label_prompt = tk.Label(frame_entry, text="Work:")
    label_prompt.grid(row=0, column=0)
    work_time_entry = tk.Entry(frame_entry, width=5)
    work_time_entry.grid(row=0, column=1, padx=(0, 10))
    work_time_entry.bind("<Return>", ask_break_time)
    work_time_entry.bind("<space>", ask_break_time)
    submit_button = tk.Button(frame_entry, text="N", command=ask_break_time)
    submit_button.grid(row=0, column=2)
    work_time_entry.focus()

def create_window():
    global window, label, pause_button, frame_label, frame_entry
    window = tk.Tk()
    window.title("Timer")
    window.overrideredirect(True)
    window.resizable(False, False)
    window.geometry("122x25+0+400")
    window.wm_attributes('-topmost', True)

    frame_top = tk.Frame(window)
    frame_top.pack(side="top", fill="x")

    close_button = tk.Button(frame_top, text="X", command=close_window, fg="black")
    close_button.pack(side="right")

    frame_entry = tk.Frame(frame_top)
    frame_entry.pack(pady=0, padx=2)
    ask_work_time()

    frame_label = tk.Frame(frame_top)
    frame_label.pack_forget()

    label = tk.Label(frame_label, font=("Arial Bold", 20), text="00:00")
    label.pack(side="left")

    pause_button = tk.Button(frame_label, text="||", command=toggle_pause, fg="black")
    pause_button.pack(side="left")

def countdown_cycle():
    global work_time, break_time
    while True:
        if not paused:
            countdown(break_time, label, "green")
            countdown(work_time, label, "black")
            
def main():
    create_window()
    window.bind("<Return>", lambda event: toggle_pause())
    window.bind("<space>", lambda event: toggle_pause())
    window.mainloop()

if __name__ == "__main__":
    main()
