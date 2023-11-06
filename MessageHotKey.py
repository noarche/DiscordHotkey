import pyautogui
import tkinter as tk
import keyboard
import pygetwindow as gw

def send_message():
    message = entry.get()
    active_window = gw.getActiveWindow()
    if active_window.title.startswith("Discord"):
        pyautogui.write(message, interval=0.1)
        pyautogui.press('enter')  
        pyautogui.press('enter')  
    else:
        active_window.activate()
        pyautogui.write(message, interval=0.1)
        pyautogui.press('enter')
        pyautogui.press('enter')

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
    send_message()

root = tk.Tk()
root.title("Message Sender")

entry = tk.Entry(root)
entry.pack()

send_button = tk.Button(root, text="Send (Enter)", command=send_message)
send_button.pack()

hotkey_button = tk.Button(root, text="Set Hotkey", command=set_hotkey)
hotkey_button.pack()

hotkey_label = tk.Label(root, text="Hotkey: pause")
hotkey_label.pack()

root.mainloop()
