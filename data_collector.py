import os
import pyautogui
import datetime
from pynput import mouse, keyboard
from PIL import Image

# Create a directory for screenshots if it doesn't exist
screenshot_dir = "screenshots"
os.makedirs(screenshot_dir, exist_ok=True)

def take_action_screenshot(action, x, y):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S%f")[:-3]  # Milliseconds precision
    filename = f"{timestamp},{action},{x},{y}.jpg"  # Change file extension to .jpg
    # Save the screenshot in the screenshots folder
    filepath = os.path.join(screenshot_dir, filename)
    
    # Take the screenshot
    screenshot = pyautogui.screenshot()
    
    # Resize the screenshot to 720p (1280x720)
    screenshot = screenshot.resize((1280, 720), Image.LANCZOS)
    
    # Compress the image
    screenshot = screenshot.convert('RGB')
    screenshot.save(filepath, optimize=True, quality=30)  # Adjust the quality as needed
    
    print(f"Saved: {filepath}")

def on_click(x, y, button, pressed):
    if pressed:
        action = f"{button} click"
        take_action_screenshot(action, x, y)

def on_press(key):
    try:
        # Get the current mouse position
        x, y = pyautogui.position()
        action = f"keypress-{key}"
        take_action_screenshot(action, x, y)
    except AttributeError:
        pass  # Special keys (like ctrl) will throw this error

# Setting up the listeners
mouse_listener = mouse.Listener(on_click=on_click)
keyboard_listener = keyboard.Listener(on_press=on_press)

mouse_listener.start()
keyboard_listener.start()

mouse_listener.join()
keyboard_listener.join()
