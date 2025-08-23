import pyautogui
import tkinter as tk
from tkinter import ttk, messagebox
import keyboard
import pygetwindow as gw
import time
import re
import configparser
import os

# Make use_number_checkbox_var global
use_number_checkbox_var = None

# Delay configuration variables
typing_delay_var = None
send_delay_var = None
repeat_delay_var = None

# Config loader
def load_settings():
    config = configparser.ConfigParser()
    defaults = {
        'typing_delay': '0.1',
        'send_delay': '0.1',
        'repeat_delay': '2.0',
        'default_message': '/fish',
        'repeat_enabled': 'no',
        'repeat_count': '1'
    }

    if os.path.exists('settings.ini'):
        config.read('settings.ini')
        if 'Delays' in config:
            defaults['typing_delay'] = config['Delays'].get('typing_delay', defaults['typing_delay'])
            defaults['send_delay'] = config['Delays'].get('send_delay', defaults['send_delay'])
            defaults['repeat_delay'] = config['Delays'].get('repeat_delay', defaults['repeat_delay'])
        if 'General' in config:
            defaults['default_message'] = config['General'].get('default_message', defaults['default_message'])
            defaults['repeat_enabled'] = config['General'].get('repeat_enabled', defaults['repeat_enabled'])
            defaults['repeat_count'] = config['General'].get('repeat_count', defaults['repeat_count'])
    return defaults

def format_time(seconds):
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    if minutes > 0:
        return f"{minutes}m {secs}s"
    else:
        return f"{secs}s"

def send_message():
    global use_number_checkbox_var

    message = entry.get()

    # Get user-configured delays
    typing_delay = typing_delay_var.get() if typing_delay_var.get() > 0 else 0.1
    send_delay = send_delay_var.get() if send_delay_var.get() > 0 else 0.1
    repeat_delay = repeat_delay_var.get() if repeat_delay_var.get() > 0 else 2.0

    if use_number_checkbox_var.get() and message.isdigit():
        current_number = int(message)
    else:
        current_number = getattr(send_message, "current_number", 0)

    repeat_count = repeat_count_var.get() if repeat_send_var.get() and repeat_count_var.get() > 0 else 1

    per_message_time = (send_delay * 2 + typing_delay + repeat_delay)
    progress_bar["maximum"] = repeat_count
    progress_bar["value"] = 0
    progress_bar["mode"] = "determinate"
    remaining_label["text"] = f"Time remaining: {format_time(repeat_count * per_message_time)}"

    for _ in range(repeat_count):
        if not re.search(r'\d', message) or message.startswith('/'):
            original_send_message(message, typing_delay, send_delay)
        else:
            active_window = gw.getActiveWindow()
            if active_window.title.startswith("Discord"):
                pyautogui.write(str(current_number), interval=typing_delay)
                pyautogui.press('enter')
                time.sleep(send_delay)
                pyautogui.press('enter')
                time.sleep(send_delay)
                pyautogui.press('enter')
            else:
                active_window.activate()
                pyautogui.write(str(current_number), interval=typing_delay)
                pyautogui.press('enter')
                time.sleep(send_delay)
                pyautogui.press('enter')
                time.sleep(send_delay)
                pyautogui.press('enter')

            current_number += 1

        progress_bar["value"] += 1
        remaining_time = max(0, (repeat_count - progress_bar['value']) * per_message_time)
        remaining_label["text"] = f"Time remaining: {format_time(remaining_time)}"
        root.update()

        if repeat_send_var.get():
            time.sleep(repeat_delay)

    send_message.current_number = current_number
    progress_bar["mode"] = "indeterminate"
    progress_bar["value"] = 0
    remaining_label["text"] = "Time remaining: N/A"

def original_send_message(message, typing_delay=0.1, send_delay=0.1):
    active_window = gw.getActiveWindow()
    if active_window.title.startswith("Discord"):
        pyautogui.write(message, interval=typing_delay)
        pyautogui.press('enter')
        time.sleep(send_delay)
        pyautogui.press('enter')
        time.sleep(send_delay)
        pyautogui.press('enter')
    else:
        active_window.activate()
        pyautogui.write(message, interval=typing_delay)
        pyautogui.press('enter')
        time.sleep(send_delay)
        pyautogui.press('enter')
        time.sleep(send_delay)
        pyautogui.press('enter')

def set_hotkey():
    global use_number_checkbox_var
    hotkey_button.config(state="disabled")
    hotkey_label.config(text="Press a key combination...")
    hotkey_label.update()
    key = keyboard.read_event(suppress=True).name
    if key:
        hotkey_label.config(text=f"Hotkey: {key}")
        hotkey_label.update()
        keyboard.unhook_all()
        keyboard.add_hotkey(key, lambda: hotkey_triggered())
        use_number_checkbox_var = repeat_send_var

def hotkey_triggered():
    global use_number_checkbox_var
    send_message()

def show_about():
    messagebox.showinfo("About", "MessageHotKey by Noarche\nhttps://github.com/noarche/DiscordHotkey\nBuild Date: May 30 2024")

def save_settings():
    config = configparser.ConfigParser()
    config['Delays'] = {
        'typing_delay': str(typing_delay_var.get()),
        'send_delay': str(send_delay_var.get()),
        'repeat_delay': str(repeat_delay_var.get())
    }
    config['General'] = {
        'default_message': entry.get(),
        'repeat_enabled': 'yes' if repeat_send_var.get() else 'no',
        'repeat_count': str(repeat_count_var.get())
    }
    with open('settings.ini', 'w') as configfile:
        config.write(configfile)
    messagebox.showinfo("Settings", "Settings saved successfully!")

# Load settings from ini
settings = load_settings()

# Main Window
root = tk.Tk()
root.title("Discord Message Hotkey")
root.geometry("200x410")
root.resizable(False, False)
root.configure(bg='black')

# About Button
about_button = tk.Button(root, text="About", command=show_about, bg='black', fg='purple')
about_button.pack()

# Message Entry
entry = tk.Entry(root, bg='gray', fg='blue')
entry.insert(0, settings['default_message'])
entry.pack()

# Repeat Checkbox
repeat_send_var = tk.BooleanVar(value=(settings['repeat_enabled'].lower() == 'yes'))
repeat_send_checkbox = tk.Checkbutton(root, text="Repeat Send Message", variable=repeat_send_var, bg='black', fg='red')
repeat_send_checkbox.pack()

# Repeat Count
repeat_count_var = tk.IntVar(value=int(settings['repeat_count']))
repeat_count_label = tk.Label(root, text="Repeat Count:", bg='black', fg='red')
repeat_count_label.pack()
repeat_count_entry = tk.Entry(root, textvariable=repeat_count_var, bg='black', fg='red')
repeat_count_entry.pack()

# Delay Config
typing_delay_var = tk.DoubleVar(value=float(settings['typing_delay']))
send_delay_var = tk.DoubleVar(value=float(settings['send_delay']))
repeat_delay_var = tk.DoubleVar(value=float(settings['repeat_delay']))

tk.Label(root, text="Typing Delay (s):", bg='black', fg='yellow').pack()
tk.Entry(root, textvariable=typing_delay_var, bg='gray', fg='yellow').pack()

tk.Label(root, text="Send Delay (s):", bg='black', fg='yellow').pack()
tk.Entry(root, textvariable=send_delay_var, bg='gray', fg='yellow').pack()

tk.Label(root, text="Repeat Delay (s):", bg='black', fg='yellow').pack()
tk.Entry(root, textvariable=repeat_delay_var, bg='gray', fg='yellow').pack()

# Hotkey Button
hotkey_button = tk.Button(root, text="Set Hotkey", command=set_hotkey, bg='black', fg='cyan')
hotkey_button.pack()

# Hotkey Label
hotkey_label = tk.Label(root, text="Hotkey: not set", bg='black', fg='cyan')
hotkey_label.pack()

# Progress Bar
progress_bar = ttk.Progressbar(root, mode='indeterminate', length=150)
progress_bar.pack()

# Time Remaining Label
remaining_label = tk.Label(root, text="Time remaining: N/A", bg='black', fg='green')
remaining_label.pack()

# Save Settings Button
save_button = tk.Button(root, text="Save Settings", command=save_settings, bg='black', fg='lime')
save_button.pack()

root.mainloop()
