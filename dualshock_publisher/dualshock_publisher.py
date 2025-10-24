import pygame
import zmq
import time

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
            axes[f"axis_{i}"] = joystick.get_axis(i)

        # Get joystick button values
        buttons = {}
        for i in range(joystick.get_numbuttons()):
            buttons[f"button_{i}"] = joystick.get_button(i)

        # Get joystick hat values (D-pad)
        hats = {}
        for i in range(joystick.get_numhats()):
            hats[f"hat_{i}"] = joystick.get_hat(i)

        # Create a message (you can customize the format)
        message = {
            "timestamp": time.time(),
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
