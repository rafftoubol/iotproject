import can
import time

bus = can.interface.Bus(bustype='socketcan', channel='vcan0')

msg = can.Message(arbitration_id=0x123, data=[0x11, 0x22], is_extended_id=False)
try:
    while True:
        bus.send(msg)
        print(f"Victim sent: {msg}")
        time.sleep(0.01)  # Send message every 10ms
except KeyboardInterrupt:
    print("Victim stopped.")
