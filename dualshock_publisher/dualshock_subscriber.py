import zmq
import json
import os

context = zmq.Context()
subscriber = context.socket(zmq.SUB)

# Connect to the publisher running in the Docker container
zmq_host = os.environ.get('ZMQ_HOST', 'localhost')
zmq_port = os.environ.get('ZMQ_PORT', '5556')
subscriber.connect(f"tcp://{zmq_host}:{zmq_port}")

# Subscribe to all messages (empty subscription)
subscriber.setsockopt_string(zmq.SUBSCRIBE, "")

print(f"ZeroMQ subscriber connected to tcp://{zmq_host}:{zmq_port}")
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
