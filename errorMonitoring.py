import can

bus = can.interface.Bus(bustype='socketcan', channel='vcan0')

print("Monitoring CAN bus...")
try:
    while True:
        msg = bus.recv(timeout=1.0)
        if msg:
            print(f"Received message: {msg}")
except KeyboardInterrupt:
    print("Monitoring stopped.")
