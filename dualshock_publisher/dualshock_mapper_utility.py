import pygame
import time

# Initialise Pygame
pygame.init()
pygame.joystick.init()

# Check for joysticks
if pygame.joystick.get_count() == 0:
    print("No joystick found. Please connect a Dualshock controller.")
    exit()

# Initialise the first joystick
joystick = pygame.joystick.Joystick(0)
joystick.init()

print(f"Detected Joystick: {joystick.get_name()}")
print("Move sticks, press buttons, and use the D-pad to see raw input values.")
print("Press Ctrl+C to exit.")

try:
    while True:
        for event in pygame.event.get():
            if event.type == pygame.JOYAXISMOTION:
                print(f"Axis {event.axis}: {event.value:.4f}")
            elif event.type == pygame.JOYBUTTONDOWN:
                print(f"Button {event.button} DOWN")
            elif event.type == pygame.JOYBUTTONUP:
                print(f"Button {event.button} UP")
            elif event.type == pygame.JOYHATMOTION:
                print(f"Hat {event.hat}: {event.value}")
        time.sleep(0.01)

except KeyboardInterrupt:
    print("\nExiting mapper utility.")
finally:
    joystick.quit()
    pygame.quit()
