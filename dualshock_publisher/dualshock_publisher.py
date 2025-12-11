import pygame
import zmq
import time
import json
import os
from dualshock_mappings import AXIS_MAP, BUTTON_MAP, HAT_MAP

# Initialise Pygame
pygame.init()
pygame.joystick.init()

# Check for joysticks
joystick = None
if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print(f"Initialised Joystick: {joystick.get_name()}")
else:
    print("WARNING: No joystick found. Publisher will run without joystick input.")

# Setup ZeroMQ publisher
context = zmq.Context()
publisher = context.socket(zmq.PUB)
zmq_host = os.environ.get('ZMQ_HOST', '*')
zmq_port = os.environ.get('ZMQ_PORT', '5556')
publisher.bind(f"tcp://{zmq_host}:{zmq_port}")

print(f"ZeroMQ publisher bound to tcp://{zmq_host}:{zmq_port}")

try:
    while True:
        pygame.event.pump() # Process pygame events

        axes = {}
        buttons = {}
        hats = {}
        controller_name = "No Controller"

        if joystick:
            controller_name = joystick.get_name()
            # Get joystick axis values
            for i in range(joystick.get_numaxes()):
                axis_name = AXIS_MAP.get(i, f"axis_{i}")
                axes[axis_name] = joystick.get_axis(i)

            # Get joystick button values
            for i in range(joystick.get_numbuttons()):
                button_name = BUTTON_MAP.get(i, f"button_{i}")
                buttons[button_name] = bool(joystick.get_button(i)) # Convert to boolean

            # Get joystick hat values (D-pad)
            for i in range(joystick.get_numhats()):
                hat_name = HAT_MAP.get(i, f"hat_{i}")
                hats[hat_name] = joystick.get_hat(i)

        # Create a message
        message = {
            "timestamp": time.time(),
            "controller_name": controller_name,
            "axes": axes,
            "buttons": buttons,
            "hats": hats
        }

        # Convert message to string and publish
        publisher.send_json(message)
        time.sleep(0.01) # Delay to prevent busy-waiting

except KeyboardInterrupt:
    print("Exiting.")
finally:
    if joystick:
        joystick.quit()
    pygame.quit()
    publisher.close()
    context.term()
