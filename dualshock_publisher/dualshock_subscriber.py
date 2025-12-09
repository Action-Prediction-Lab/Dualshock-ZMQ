import zmq
import json

context = zmq.Context()
subscriber = context.socket(zmq.SUB)

# Connect to the publisher running in the Docker container
subscriber.connect("tcp://localhost:5556")

# Subscribe to all messages (empty subscription)
subscriber.setsockopt_string(zmq.SUBSCRIBE, "")

print("ZeroMQ subscriber connected to tcp://localhost:5556")
print("Waiting for Dualshock controller input...")

try:
    while True:
        message = subscriber.recv_json()
        print(f"Received: {json.dumps(message, indent=2)}")
except KeyboardInterrupt:
    print("Exiting subscriber.")
finally:
    subscriber.close()
    context.term()
