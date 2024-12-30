import tkinter as tk
import time
import threading

paused = False
work_time = 0
break_time = 0

def countdown(count, label, color, flash_color=None):
    global paused
    while count >= 0 and not paused:
        minutes, seconds = divmod(count, 60)
        label.config(text=f"{minutes:02d}:{seconds:02d}", fg=color)
        label.update()
        time.sleep(1)
        count -= 1
    if flash_color:
        flash_screen(flash_color)

def flash_screen(color):
    flash_window = tk.Toplevel()
    screen_width = flash_window.winfo_screenwidth()
    screen_height = flash_window.winfo_screenheight()
    flash_window.geometry(f"{screen_width}x{screen_height}+0+0")
    flash_window.config(bg=color)
    flash_window.attributes('-topmost', True)
    flash_window.attributes('-alpha', 1.0)
    flash_window.update_idletasks() 
    flash_window.update()           
    flash_window.focus_force()     
    flash_window.geometry(f"{screen_width}x{screen_height}+0+0")

    def destroy_flash():
        flash_window.destroy()

    flash_window.after(1000, destroy_flash)

def toggle_pause(event=None):
    global paused
    paused = not paused
    pause_button.config(text="▶" if paused else "||")

def close_window():
    window.destroy()

def start_timer(event=None):
    global work_time, break_time
    try:
        break_time = int(break_time_entry.get()) * 60
        work_time = int(work_time_entry.get()) * 60
    except ValueError:
        if work_time_entry.get() == "":
            flash_entry(work_time_entry)
        if break_time_entry.get() == "":
            flash_entry(break_time_entry)
        return

    frame_entry.pack_forget()
    frame_label.pack(pady=2, padx=2)
    timer_thread = threading.Thread(target=countdown_cycle)
    timer_thread.daemon = True
    timer_thread.start()

def ask_break_time(event=None):
    global break_time_entry
    try:
        work_time = int(work_time_entry.get()) * 60
    except ValueError:
        flash_entry(work_time_entry)
        return
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

    window_height = 25
    screen_height = window.winfo_screenheight()
    y = (screen_height - window_height) // 2
    window.geometry(f"122x{window_height}+0+{y}")
    window.wm_attributes('-topmost', True)
    window.attributes('-alpha', 0.70)

    frame_top = tk.Frame(window)
    frame_top.pack(side="top", fill="x")

    close_button = tk.Button(frame_top, text="X", command=close_window, fg="black",
                             borderwidth=0, highlightthickness=0)
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
            countdown(work_time, label, "black", "red")
            countdown(break_time, label, "green", "green")

def main():
    create_window()
    window.bind("<Return>", lambda event: toggle_pause())
    window.bind("<space>", lambda event: toggle_pause())
    window.mainloop()

if __name__ == "__main__":
    main()