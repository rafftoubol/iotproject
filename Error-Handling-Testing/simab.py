import can
import threading
import time
import os

def send_conflicting_frames(interface, node_id):
    """
    Sends CAN frames with overlapping IDs to simulate contention.
    """
    bus = can.Bus(interface, bustype="socketcan")
    msg_id = 0x111  # Overlapping arbitration ID

    while True:
        try:
            # Construct CAN message
            msg = can.Message(arbitration_id=msg_id, data=[node_id] * 8, is_extended_id=False)
            bus.send(msg)
            print(f"Node {node_id} sent: {msg}")
            time.sleep(0.01)  # Adjust rate to increase contention
        except can.CanError as e:
            print(f"Node {node_id} error: {e}")

def monitor_error_frames(interface):
    """
    Monitors the CAN bus for error frames.
    """
    bus = can.Bus(interface, bustype="socketcan")
    print(f"Monitoring error frames on {interface}...")
    
    while True:
        msg = bus.recv(timeout=1)  # Wait for a message
        if msg is None:
            continue

        if msg.is_error_frame:
            print(f"Error frame detected! ID: 0x{msg.arbitration_id:X}, Data: {msg.data.hex()}")

def monitor_bus_state(interface):
    """
    Monitors the vCAN interface for error states.
    """
    while True:
        state = os.popen(f"ip -details link show {interface}").read()
        if "state BUS-OFF" in state:
            print(f"BUS-OFF detected on {interface}!")
            break
        time.sleep(0.5)

def main():
    interface = "vcan0"

    # Set up vCAN interface
    os.system(f"sudo modprobe vcan")
    os.system(f"sudo ip link add dev {interface} type vcan")
    os.system(f"sudo ip link set up {interface}")
    os.system(f"sudo ip link set {interface} type can berr-reporting on")  # Enable error reporting
    print(f"vCAN {interface} initialized.")

    # Start two threads sending conflicting frames
    threading.Thread(target=send_conflicting_frames, args=(interface, 1), daemon=True).start()
    threading.Thread(target=send_conflicting_frames, args=(interface, 2), daemon=True).start()

    # Start error frame monitoring
    threading.Thread(target=monitor_error_frames, args=(interface,), daemon=True).start()

    # Monitor the bus state
    monitor_bus_state(interface)

if __name__ == "__main__":
    main()
