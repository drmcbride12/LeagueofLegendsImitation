import os
import pyautogui
import datetime
from pynput import mouse, keyboard
from PIL import Image
import time

# Create a directory for screenshots if it doesn't exist
screenshot_dir = "screenshots"
os.makedirs(screenshot_dir, exist_ok=True)

ctrl_pressed = False
last_key_press_time = {}

def take_action_screenshot(action, x, y):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S%f")[:-3]  # Milliseconds precision
    filename = f"{timestamp},{action},{x},{y}.png"  # Change file extension to .png
    # Save the screenshot in the screenshots folder
    filepath = os.path.join(screenshot_dir, filename)
    
    # Take the screenshot
    screenshot = pyautogui.screenshot()
    
    # Resize the screenshot to (128x128)
    screenshot = screenshot.resize((128, 128), Image.LANCZOS)
    
    # Save the image as PNG without compression
    screenshot.save(filepath, format="PNG")  # PNG format is lossless by default
    
    print(f"Saved: {filepath}")

def on_click(x, y, button, pressed):
    if pressed:
        action = f"{button} click"
        take_action_screenshot(action, x, y)

def on_press(key):
    global ctrl_pressed, last_key_press_time
    try:
        current_time = time.time()

        if key in (keyboard.Key.ctrl_l, keyboard.Key.ctrl_r):
            ctrl_pressed = True
            return

        if not ctrl_pressed:
            key_str = str(key)
            if key_str in last_key_press_time:
                elapsed_time = current_time - last_key_press_time[key_str]
                if elapsed_time < 0.1:
                    return

            last_key_press_time[key_str] = current_time

            # Get the current mouse position
            x, y = pyautogui.position()
            action = f"keypress-{key}"
            take_action_screenshot(action, x, y)
    except AttributeError:
        pass  # Special keys (like ctrl) will throw this error

def on_release(key):
    global ctrl_pressed
    if key in (keyboard.Key.ctrl_l, keyboard.Key.ctrl_r):
        ctrl_pressed = False

# Setting up the listeners
mouse_listener = mouse.Listener(on_click=on_click)
keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)

mouse_listener.start()
keyboard_listener.start()

mouse_listener.join()
keyboard_listener.join()
