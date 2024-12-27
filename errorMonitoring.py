import socket
import struct

# Define CAN interface
CAN_INTERFACE = "vcan0"

# Create a CAN socket
s = socket.socket(socket.AF_CAN, socket.SOCK_RAW, socket.CAN_RAW)
s.bind((CAN_INTERFACE,))

# Monitor CAN traffic and error notifications
print(f"Monitoring CAN interface: {CAN_INTERFACE}")
try:
    while True:
        # Receive a frame
        frame, addr = s.recvfrom(16)
        
        # Unpack CAN frame header
        can_id, length = struct.unpack("=IB3x", frame[:8])
        data = frame[8:8+length]
        
        if can_id & socket.CAN_ERR_FLAG:
            print(f"[ERROR] CAN Error Frame: CAN ID {hex(can_id)}")
        else:
            print(f"[MESSAGE] CAN ID: {hex(can_id)}, Data: {data}")

except KeyboardInterrupt:
    print("Monitoring stopped.")