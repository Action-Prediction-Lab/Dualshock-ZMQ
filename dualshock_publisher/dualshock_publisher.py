import pygame
import zmq
import time
import json
from dualshock_mappings import AXIS_MAP, BUTTON_MAP, HAT_MAP

# Initialize Pygame
pygame.init()
pygame.joystick.init()

# Check for joysticks
if pygame.joystick.get_count() == 0:
    print("No joystick found.")
    exit()

# Initialize the first joystick
joystick = pygame.joystick.Joystick(0)
joystick.init()

print(f"Initialized Joystick: {joystick.get_name()}")

# Setup ZeroMQ publisher
context = zmq.Context()
publisher = context.socket(zmq.PUB)
publisher.bind("tcp://*:5556") # Bind to port 5556

print("ZeroMQ publisher bound to tcp://*:5556")

try:
    while True:
        pygame.event.pump() # Process pygame events

        # Get joystick axis values
        axes = {}
        for i in range(joystick.get_numaxes()):
            axis_name = AXIS_MAP.get(i, f"axis_{i}")
            axes[axis_name] = joystick.get_axis(i)

        # Get joystick button values
        buttons = {}
        for i in range(joystick.get_numbuttons()):
            button_name = BUTTON_MAP.get(i, f"button_{i}")
            buttons[button_name] = bool(joystick.get_button(i)) # Convert to boolean

        # Get joystick hat values (D-pad)
        hats = {}
        for i in range(joystick.get_numhats()):
            hat_name = HAT_MAP.get(i, f"hat_{i}")
            hats[hat_name] = joystick.get_hat(i)

        # Create a message
        message = {
            "timestamp": time.time(),
            "controller_name": joystick.get_name(),
            "axes": axes,
            "buttons": buttons,
            "hats": hats
        }

        # Convert message to string and publish
        publisher.send_json(message)
        # print(f"Published: {message}") # Uncomment for debugging

        time.sleep(0.01) # Small delay to prevent busy-waiting

except KeyboardInterrupt:
    print("Exiting.")
finally:
    joystick.quit()
    pygame.quit()
    publisher.close()
    context.term()
