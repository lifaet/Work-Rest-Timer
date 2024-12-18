import tkinter as tk
import time
import threading

def countdown_cycle():
    while True:
        countdown(60, label, "red")
        countdown(1200, label, "black")

def countdown(count, label, color):
    while count >= 0:
        minutes, seconds = divmod(count, 60)
        label.config(text=f"{minutes:02d}:{seconds:02d}", fg=color)
        time.sleep(1)
        count -= 1

def close_window():
    window.destroy()

window = tk.Tk()
window.title("Timer")
window.overrideredirect(True)
window.resizable(False, False)
window.geometry("90x25+0+400")
window.wm_attributes('-topmost', True)
close_button = tk.Button(window, text="X", command=close_window, fg="black")
close_button.pack(side="right", anchor="ne")
label = tk.Label(window, font=("Arial Bold", 20), text="25:00")
label.pack(pady=2, padx=2)
timer_thread = threading.Thread(target=countdown_cycle)

timer_thread.start()
window.mainloop()