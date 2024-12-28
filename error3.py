import can

def monitor_can(bus_name):
    bus = can.Bus(interface="socketcan", channel=bus_name)
    print(f"Listening on {bus_name}...")

    while True:
        msg = bus.recv()
        if not msg:
            continue

        print(f"CAN ID: 0x{msg.arbitration_id:X}")
        if msg.is_error_frame:
            print("Error frame detected!")
        elif msg.is_extended_id:
            print("Extended frame detected (EFF).")
        else:
            print("Standard frame detected.")

if __name__ == "__main__":
    monitor_can("vcan0")  # Replace 'can0' with your CAN interface
