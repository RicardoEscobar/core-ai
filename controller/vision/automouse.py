import time
import pyautogui

def click_mouse_at_intervals(interval, duration):
    end_time = time.time() + duration
    while time.time() < end_time:
        pyautogui.click(button='left', interval=interval)
        # pyautogui.sleep(interval)
        print("clicked")

def click_mouse_1sec(interval, duration):
    end_time = time.time() + duration
    while time.time() < end_time:
        pyautogui.mouseDown(button='left')
        pyautogui.sleep(1)  # Keep the button pressed for a second
        pyautogui.mouseUp(button='left')
        time.sleep(interval - 1)  # Subtract the time the button was pressed
        print("clicked")

# Example usage:
interval_seconds = 2  # Click every 2 seconds
click_duration = 10  # Click for a total of 10 seconds
click_mouse_1sec(interval_seconds, click_duration)
