import tkinter as tk
import time
import threading
paused = False

def countdown(count, label, color):
    global paused
    while count >= 0 and not paused:
        minutes, seconds = divmod(count, 60)
        label.config(text=f"{minutes:02d}:{seconds:02d}", fg=color)
        label.update()
        time.sleep(1)
        count -= 1

def toggle_pause():
    global paused
    paused = not paused
    pause_button.config(text="▶" if paused else "||")

def close_window():
    window.destroy()

def create_window():
    global window, label, pause_button
    window = tk.Tk()
    window.title("Timer")
    window.overrideredirect(True)
    window.resizable(False, False)
    window.geometry("125x25+0+400")
    window.wm_attributes('-topmost', True)

    frame = tk.Frame(window)
    frame.pack(pady=2, padx=2)

    label = tk.Label(frame, font=("Arial Bold", 20), text="20:00")
    label.pack(side="left")

    pause_button = tk.Button(frame, text="||", command=toggle_pause, fg="black")
    pause_button.pack(side="left", padx=(0, 5))

    close_button = tk.Button(frame, text="X", command=close_window, fg="black")
    close_button.pack(side="left")

    return label

def countdown_cycle(label):
    while True:
        if not paused:
            countdown(120, label, "black")
            countdown(1200, label, "red")

def main():
    label = create_window()

    timer_thread = threading.Thread(target=countdown_cycle, args=(label,))
    timer_thread.daemon = True
    timer_thread.start()

    window.mainloop()

if __name__ == "__main__":
    main()
