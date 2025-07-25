
import time
import os
import datetime
from random import randint



import pyautogui
from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener
from pynput.mouse import Controller

# Global variable to track last user activity
last_active_time = time.time()

# Get the primary monitor size
import pyautogui
from pynput.mouse import Controller


# Find center of main monitor in case we need to re-align later.
screen_width, screen_height = pyautogui.size()
center = (screen_width // 2, screen_height // 2)
mouse = Controller()
print("Primary monitor center: ", center)


def read_config():
    config = {
        'activity_timeout': 120,    # Time before mouse starts to jiggle, Default 120 Seconds.
        'random_jiggle': False,      # Use random intervals between mouse jiggles, Default is false.
        'random_jiggle_maximum_time': 120,
        'random_jiggle_minimum_time': 15 
    }
    
    try:
        with open('config.txt', 'r') as file:
            print("Configuration file found! Reading config...")
            for line in file:
                line.strip()
                if not line or '=' not in line:
                    continue

                # Get Activity_timeout value
                if line.startswith('activity_timeout'):
                    try:
                        config['activity_timeout'] = int(line.split('=')[1].strip())
                        print(f"Activity Timeout found: {config['activity_timeout']} Seconds")
                        continue
                    except ValueError:
                        print(f"Error: Invalid value in config.txt for activity_timeout: {line}")
                        continue

                # Get random_jiggle value from config.txt, 1 for True, 0 for False. Also set random_jiggle parameters.
                if line.startswith('random_jiggle'):
                    field = line.split('=')

                    if field[0] == 'random_jiggle':
                        try:
                            config['random_jiggle'] = bool(int(field[1].strip()))
                        except ValueError:
                            print(f"\nError: Invalid value in config.txt for random_jiggle: {line}Using default value {config['random_jiggle']}") 
                        continue


                    elif field[0] == 'random_jiggle_maximum_time':
                        try:
                            config['random_jiggle_maximum_time'] = int(field[1].strip())
                        except ValueError:
                            print(f"\nError: Invalid value in config.txt for random_jiggle_maximum_time: {line}Using default value {config['random_jiggle_maximum_time']}")
                        continue


                    elif field[0] == 'random_jiggle_minimum_time':
                        try:
                            config['random_jiggle_minimum_time'] = int(field[1].strip())
                        except ValueError:
                            print(f"\nError: Invalid value in config.txt for random_jiggle_maximum_time: {line}Using default value {config['random_jiggle_minimum_time']}")
                        continue
                    
            if config['random_jiggle']:
                print(f"Random intervals between jiggles is Enabled!\nMin/Max time between Jiggles is {config['random_jiggle_minimum_time']}s/{config['random_jiggle_maximum_time']}s")

            else:
                print(f"No Random Jiggle parameters set, using defaults...")

                # Print the configuration
                print("Starting Jiggler with the following configuration:")
                for param in config:
                    print("\t" + param + ":" + str(config[param]))
            return config 
                

    except FileNotFoundError: #Use Default values specified above if no config is found.
        print(f"Error: Config file not found in {os.getcwd()}\n")
        print(f'Using Default Params:')
        for param in config:
            print("\t" + param + ":" + str(config[param]))
        return config

def on_move(x, y):
    # Function to update the last activity time when mouse moves.
    global last_active_time
    last_active_time = time.time()

def on_click(x, y, button, pressed):
    # Function to update the last activity time when mouse clicks.
    global last_active_time
    last_active_time = time.time()

def on_scroll(x, y, dx, dy):
    #Function to update the last activity time when mouse scrolls.
    global last_active_time
    last_active_time = time.time()

def on_press(key):
    #Function to update the last activity time when a key is pressed.
    global last_active_time
    last_active_time = time.time()

def jiggle_cursor():
    #Function to jiggle the mouse slightly.
    print("Jiggling Cursor...")
    pyautogui.move(10, 0)  # Move the mouse 10 pixels to the right
    pyautogui.move(-10, 0)  # Move the mouse 10 pixels back to the left
    print(f"Cursor Jiggled at {datetime.datetime.now()}")

def monitor_activity(config):
    global last_active_time
    
    activity_timeout = config['activity_timeout']
    random_jiggle = config['random_jiggle']
    random_jiggle_maxtime = config['random_jiggle_maximum_time']
    random_jiggle_mintime = config['random_jiggle_minimum_time']

    next_jiggle_time = activity_timeout

    print("============================================================================")
    print(f'Jiggler started at {datetime.datetime.now()}')
    print("============================================================================")

    while True:
        # After waiting, check if the user has been inactive for the configured timeout
        current_time = time.time()

        if random_jiggle:
            if current_time - last_active_time > next_jiggle_time:
                try:
                    jiggle_cursor()
                except:
                    print("Mouse moved too far to the right! Re-aligning to center...\n")
                    mouse.position = center
                    jiggle_cursor()
                next_jiggle_time = randint(random_jiggle_mintime, random_jiggle_maxtime)
                print(f"Next jiggle {next_jiggle_time + 5}  seconds after inactivity...")
                time.sleep(next_jiggle_time)   # Sleep for the random interval before checking activity again
                

        elif current_time - last_active_time > activity_timeout:
            jiggle_cursor() 
            time.sleep(next_jiggle_time)
        
        time.sleep(next_jiggle_time) #Wait before re-evaluating so computer doesnt blow up

if __name__ == "__main__":
    config = read_config()
    with MouseListener(on_move=on_move, on_click=on_click, on_scroll=on_scroll) as mouse_listener:
        with KeyboardListener(on_press=on_press) as keyboard_listener:
            monitor_activity(config)
