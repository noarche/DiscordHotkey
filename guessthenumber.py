import pyautogui
import tkinter as tk
import keyboard
import pygetwindow as gw
import time
import random

is_paused = False

def send_random_numbers():
    global is_paused
    number_range = entry.get().split('-')
    if len(number_range) != 2:
        return  # Invalid input

    start, end = int(number_range[0]), int(number_range[1])

    if start > end:
        return  # Invalid range

    active_window = gw.getActiveWindow()
    
    numbers = list(range(start, end + 1))
    random.shuffle(numbers)  # Shuffle the list to send random numbers
    
    for num in numbers:
        if is_paused:
            break
        message = str(num)
        if active_window.title.startswith("Discord"):
            pyautogui.write(message, interval=0.1)
            pyautogui.press('enter')
            pyautogui.press('enter')
        else:
            active_window.activate()
            pyautogui.write(message, interval=0.1)
            pyautogui.press('enter')
            pyautogui.press('enter')
        time.sleep(1.5)  # Add a 0.5-second delay between messages

def toggle_pause():
    global is_paused
    is_paused = not is_paused

def set_hotkey():
    hotkey_button.config(state="disabled")
    hotkey_label.config(text="Press a key combination...")
    hotkey_label.update()
    key = keyboard.read_event(suppress=True).name
    if key:
        hotkey_label.config(text=f"Hotkey: {key}")
        hotkey_label.update()
        keyboard.on_press_key(key, hotkey_triggered)

def hotkey_triggered(e):
    send_random_numbers()

root = tk.Tk()
root.title("Random Number Sender")

entry = tk.Entry(root)
entry.pack()

send_button = tk.Button(root, text="Send Random Numbers", command=send_random_numbers)
send_button.pack()

pause_button = tk.Button(root, text="Pause/Resume", command=toggle_pause)
pause_button.pack()

hotkey_button = tk.Button(root, text="Set Hotkey", command=set_hotkey)
hotkey_button.pack()

hotkey_label = tk.Label(root, text="Hotkey: pause")
hotkey_label.pack()

root.mainloop()
