# Dualshock-ZMQ

## Dualshock Publisher Application

This is my containerised application that captures input from a Dualshock controller and publishes it via ZeroMq.

### ZeroMQ Message Format

The Dualshock Publisher broadcasts controller input as JSON messages over ZeroMQ. Each message is a dictionary containing the following keys:

*   **`timestamp`**: A float representing the time the message was generated (Python's `time.time()`).
*   **`controller_name`**: A string identifying the detected Dualshock controller (e.g., "Wireless Controller").
*   **`axes`**: A dictionary where keys are axis names (as defined in `dualshock_mappings.py`) and values are float readings from -1.0 to 1.0 (or 0.0 to 1.0 for triggers).
    *   Example: `"left_stick_x": 0.5432`
*   **`buttons`**: A dictionary where keys are button names (as defined in `dualshock_mappings.py`) and values are boolean (`true`/`false`) indicating if the button is currently pressed.
    *   Example: `"cross": true`
*   **`hats`**: A dictionary where keys are hat names (as defined in `dualshock_mappings.py`) and values are tuples representing the D-pad state. The tuple contains two integers, (x, y), where x is -1 for left, 1 for right, and 0 for neutral; y is -1 for down, 1 for up, and 0 for neutral.
    *   Example: `"dpad": (0, 1)` (D-pad Up pressed)

### Setup and Run with Docker Compose

1.  **Ensure Docker is running:** 

2.  **Connect your Dualshock controller:** Via USB or Bluetooth.

3.  **Build and run the container:** Run:
    ```bash
    docker compose up --build -d
    ```

4.  **Verify the publisher:** The ZeroMQ publisher runs inside the container. By default, it binds to `tcp://*:5556`. You can connect to this address from another application to receive controller input data (e.g., test with `dualshock_subscriber.py` from your machine, which connects to `tcp://localhost:5556` by default).

5.  **Stop the container:** To stop the running container, use:
    ```bash
    docker compose down
    ```

### Accessing Controller Input

The application needs access to `/dev/input` on the host system to read joystick events. The `docker-compose.yml` file is configured to mount this directory into the container and runs the container in `privileged` mode to do so.

### Customising Controller Mappings

The specific mappings for axes, buttons, and hats can vary between different Dualshock controller models. `dualshock_publisher/dualshock_mappings.py` is used to define these mappings.

1.  **Find your controller's mappings:**
    Use `dualshock_mapper_utility` to identify the raw input for your specific controller:
    ```bash
    python Dualshock/dualshock_publisher/dualshock_mapper_utility.py
    ```
2.  Play with your controller. 

3.  **Edit `dualshock_publisher/dualshock_mappings.py`:**
    Open `dualshock_publisher/dualshock_mappings.py` and update the `AXIS_MAP`, `BUTTON_MAP`, and `HAT_MAP` dictionaries with your mappings.

4.  **Restart the publisher container:** 
