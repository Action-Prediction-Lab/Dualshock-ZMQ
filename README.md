# Dualshock

## Dualshock Publisher Application

This application captures input from a Dualshock controller and publishes it via ZeroMQ.

### Setup and Run with Docker Compose

1.  **Ensure Docker is running:** Make sure Docker Desktop or Docker Engine is installed and running on your system.

2.  **Connect your Dualshock controller:** Connect your Dualshock controller to your computer via USB or Bluetooth.

3.  **Build and run the container:** Navigate to the root directory of this project in your terminal and run:
    ```bash
    docker-compose up --build -d
    ```
    The `--build` flag will build the Docker image (if not already built or if changes were made to the Dockerfile/context), and `-d` will run the container in detached mode.
    
    **Live Code Changes:** Due to the volume mount, any changes you make to `dualshock_publisher.py` on your host machine will be immediately reflected inside the running container without needing to rebuild the image.

4.  **Verify the publisher:** The ZeroMQ publisher will be running inside the container, binding to `tcp://*:5556`. You can connect to this address from another application to receive controller input data (test with `dualshock_subscriber.py` from your local machine). 

5.  **Stop the container:** To stop the running container, use:
    ```bash
    docker-compose down
    ```

### Accessing Controller Input

The application requires access to `/dev/input` on the host system to read joystick events. The `docker-compose.yml` file is configured to mount this directory into the container and runs the container in `privileged` mode to facilitate this access.