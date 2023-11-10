import pyautogui
import tkinter as tk
import keyboard
import pygetwindow as gw
import time
import re

def send_message():
    message = entry.get()

    # Check if the checkbox is selected and the entered text is a number
    if use_number_checkbox_var.get() and message.isdigit():
        # Reset the current_number if using the entered number
        current_number = int(message)
    else:
        # Use the previous value of current_number
        current_number = getattr(send_message, "current_number", 0)

    # Check if the repeat checkbox is selected and the repeat count is a positive number
    repeat_count = repeat_count_var.get() if repeat_send_var.get() and repeat_count_var.get() > 0 else 1

    for _ in range(repeat_count):
        # Check if there is no number detected or the text starts with '/'
        if not re.search(r'\d', message) or message.startswith('/'):
            original_send_message(message)
        else:
            active_window = gw.getActiveWindow()
            if active_window.title.startswith("Discord"):
                pyautogui.write(str(current_number), interval=0.3)
                pyautogui.press('enter')
                time.sleep(0.8)
                pyautogui.press('enter')
                time.sleep(0.8)
                pyautogui.press('enter')
            else:
                active_window.activate()
                pyautogui.write(str(current_number), interval=0.3)
                pyautogui.press('enter')
                time.sleep(0.6)
                pyautogui.press('enter')
                time.sleep(0.6)
                pyautogui.press('enter')

            # Increment the current_number by 1
            current_number += 1

        # Sleep for 5 seconds if repeat message is enabled
        if repeat_send_var.get():
            time.sleep(5.0)

    # Save the current_number for the next iteration
    send_message.current_number = current_number

def original_send_message(message):
    active_window = gw.getActiveWindow()
    if active_window.title.startswith("Discord"):
        pyautogui.write(message, interval=0.3)
        pyautogui.press('enter')
        time.sleep(0.8)
        pyautogui.press('enter')
        time.sleep(0.8)
        pyautogui.press('enter')
    else:
        active_window.activate()
        pyautogui.write(message, interval=0.3)
        pyautogui.press('enter')
        time.sleep(0.6)
        pyautogui.press('enter')
        time.sleep(0.6)
        pyautogui.press('enter')

def set_hotkey():
    hotkey_button.config(state="disabled")
    hotkey_label.config(text="Press a key combination...")
    hotkey_label.update()
    key = keyboard.read_event(suppress=True).name
    if key:
        hotkey_label.config(text=f"Hotkey: {key}")
        hotkey_label.update()

        # Remove any existing hotkey
        keyboard.unhook_all()

        # Set the new hotkey
        keyboard.add_hotkey(key, hotkey_triggered)

def hotkey_triggered():
    send_message()

root = tk.Tk()
root.title("Message Sender")

entry = tk.Entry(root)
entry.pack()

# Checkbox to indicate if the entered text is a number
use_number_checkbox_var = tk.BooleanVar()
use_number_checkbox = tk.Checkbutton(root, text="Use Entered Number as Starting Point", variable=use_number_checkbox_var)
use_number_checkbox.pack()

# Checkbox to enable repeat message sending
repeat_send_var = tk.BooleanVar()
repeat_send_checkbox = tk.Checkbutton(root, text="Repeat Send Message", variable=repeat_send_var)
repeat_send_checkbox.pack()

# Entry for the number of times to repeat sending message
repeat_count_var = tk.IntVar()
repeat_count_label = tk.Label(root, text="Repeat Count:")
repeat_count_label.pack()

repeat_count_entry = tk.Entry(root, textvariable=repeat_count_var)
repeat_count_entry.pack()

send_button = tk.Button(root, text="Send (Enter)", command=send_message)
send_button.pack()

hotkey_button = tk.Button(root, text="Set Hotkey", command=set_hotkey)
hotkey_button.pack()

hotkey_label = tk.Label(root, text="Hotkey: not set")
hotkey_label.pack()

root.mainloop()

