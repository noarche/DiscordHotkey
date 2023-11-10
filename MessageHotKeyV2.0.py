import pyautogui
import tkinter as tk
import keyboard
import pygetwindow as gw
import time
import re

# Initialize the start number and skip value
current_number = 0
skip_value = 2

def send_message():
    global current_number
    message = entry.get()

    # Check if the checkbox is selected and the entered text is a number
    if use_number_checkbox_var.get() and message.isdigit():
        current_number = int(message) - skip_value

    # Check if there is no number detected or the text starts with '/'
    if not re.search(r'\d', message) or message.startswith('/'):
        original_send_message()
        return

    active_window = gw.getActiveWindow()
    if active_window.title.startswith("Discord"):
        pyautogui.write(str(current_number + skip_value), interval=0.3)
        pyautogui.press('enter')
        time.sleep(0.8)
        pyautogui.press('enter')
        time.sleep(0.8)
        pyautogui.press('enter')
    else:
        active_window.activate()
        pyautogui.write(str(current_number + skip_value), interval=0.3)
        pyautogui.press('enter')
        time.sleep(0.6)
        pyautogui.press('enter')
        time.sleep(0.6)
        pyautogui.press('enter')

    # Increment the current_number by the skip_value
    current_number += skip_value

    # Disable the checkbox if it's enabled
    if use_number_checkbox_var.get():
        use_number_checkbox.deselect()

def original_send_message():
    message = entry.get()
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

send_button = tk.Button(root, text="Send (Enter)", command=send_message)
send_button.pack()

hotkey_button = tk.Button(root, text="Set Hotkey", command=set_hotkey)
hotkey_button.pack()

hotkey_label = tk.Label(root, text="Hotkey: not set")
hotkey_label.pack()

root.mainloop()
