import pyautogui
import tkinter as tk
from tkinter import ttk, messagebox
import keyboard
import pygetwindow as gw
import time
import re

# Make use_number_checkbox_var global
use_number_checkbox_var = None

def send_message():
    global use_number_checkbox_var  # Access the global variable

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

    # Configure progress bar for repeating messages
    progress_bar["maximum"] = repeat_count
    progress_bar["value"] = 0
    progress_bar["mode"] = "determinate"
    remaining_label["text"] = f"Time remaining: {repeat_count * 2.5} seconds"

    for _ in range(repeat_count):
        # Check if there is no number detected or the text starts with '/'
        if not re.search(r'\d', message) or message.startswith('/'):
            original_send_message(message)
        else:
            active_window = gw.getActiveWindow()
            if active_window.title.startswith("Discord"):
                pyautogui.write(str(current_number), interval=0.2)
                pyautogui.press('enter')
                time.sleep(0.2)
                pyautogui.press('enter')
                time.sleep(0.2)
                pyautogui.press('enter')
            else:
                active_window.activate()
                pyautogui.write(str(current_number), interval=0.2)
                pyautogui.press('enter')
                time.sleep(0.2)
                pyautogui.press('enter')
                time.sleep(0.2)
                pyautogui.press('enter')

            # Increment the current_number by 1
            current_number += 1

        # Update progress bar and time remaining
        progress_bar["value"] += 1
        remaining_label["text"] = f"Time remaining: {max(0, (repeat_count - progress_bar['value']) * 2.5)} seconds"
        root.update()  # Update the GUI to show the progress

        # Sleep for 5 seconds if repeat message is enabled
        if repeat_send_var.get():
            time.sleep(2.2)

    # Save the current_number for the next iteration
    send_message.current_number = current_number

    # Reset progress bar and time remaining
    progress_bar["mode"] = "indeterminate"
    progress_bar["value"] = 0
    remaining_label["text"] = "Time remaining: N/A"

def original_send_message(message):
    active_window = gw.getActiveWindow()
    if active_window.title.startswith("Discord"):
        pyautogui.write(message, interval=0.1)
        pyautogui.press('enter')
        time.sleep(0.1)
        pyautogui.press('enter')
        time.sleep(0.1)
        pyautogui.press('enter')
    else:
        active_window.activate()
        pyautogui.write(message, interval=0.1)
        pyautogui.press('enter')
        time.sleep(0.1)
        pyautogui.press('enter')
        time.sleep(0.1)
        pyautogui.press('enter')

def set_hotkey():
    global use_number_checkbox_var  # Access the global variable
    hotkey_button.config(state="disabled")
    hotkey_label.config(text="Press a key combination...")
    hotkey_label.update()
    key = keyboard.read_event(suppress=True).name
    print(f"Selected hotkey: {key}")  # Add this line for debugging
    if key:
        hotkey_label.config(text=f"Hotkey: {key}")
        hotkey_label.update()

        # Remove any existing hotkey
        keyboard.unhook_all()

        # Set the new hotkey
        keyboard.add_hotkey(key, lambda: hotkey_triggered())
        use_number_checkbox_var = repeat_send_var  # Fix here
        print("Hotkey set successfully")  # Add this line for debugging

def hotkey_triggered():
    global use_number_checkbox_var  # Access the global variable
    print("Hotkey triggered")  # Add this line for debugging
    send_message()

def show_about():
    messagebox.showinfo("About", "MessageHotKey by Noarche\nhttps://github.com/noarche/DiscordHotkey\nBuild Date: May 30 2024\n\nAbout:\nThis application automates discord bots that require competative task such as games by entering the bot command/trigger.\n\nHelp:\nEnter your message or trigger/command.\nIf you do not check the repeat box the message is only sent once every time you press the hotkey.\nSetting Hotkey: After pressing 'Set Hotkey' button press a key on your keyboard. This will be set as the hotkey to start sending messages.")

# Create the main window
root = tk.Tk()
root.title("Message Sender")
root.geometry("160x210")
root.resizable(False, False)  # Make the window not resizable
root.configure(bg='black')

# Button to show about info
about_button = tk.Button(root, text="About", command=show_about, bg='black', fg='purple')
about_button.pack()

# Entry for the message
entry = tk.Entry(root, bg='gray', fg='blue')
entry.insert(0, "enter message here")  # Set default text
entry.pack()

# Checkbox to enable repeat message sending
repeat_send_var = tk.BooleanVar()
repeat_send_checkbox = tk.Checkbutton(root, text="Repeat Send Message", variable=repeat_send_var, bg='black', fg='red')
repeat_send_checkbox.pack()

# Entry for the number of times to repeat sending message
repeat_count_var = tk.IntVar()
repeat_count_label = tk.Label(root, text="Repeat Count:", bg='black', fg='red')
repeat_count_label.pack()

repeat_count_entry = tk.Entry(root, textvariable=repeat_count_var, bg='black', fg='red')
repeat_count_entry.pack()

# Button to set the hotkey
hotkey_button = tk.Button(root, text="Set Hotkey", command=set_hotkey, bg='black', fg='cyan')
hotkey_button.pack()

# Label to display the current hotkey
hotkey_label = tk.Label(root, text="Hotkey: not set", bg='black', fg='cyan')
hotkey_label.pack()


# Progress bar for repeat messages
progress_bar = ttk.Progressbar(root, mode='indeterminate', length=150)
progress_bar.pack()

# Label to display time remaining
remaining_label = tk.Label(root, text="Time remaining: N/A", bg='black', fg='green')
remaining_label.pack()




# Run the main loop
root.mainloop()
