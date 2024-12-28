import binascii
import socket



#channel_name = 'vcan0'
#socketID = socket.socket(socket.AF_CAN, socket.SOCK_RAW, socket.CAN_RAW)

#while
#error = socketID.bind((channel_name,))
#print(binascii.hexlify(socketID.recv(16)))
#print(socket.CAN_ERR_FLAG)

import can
import time

def monitor_bus(interface):
    bus = can.Bus(interface, bustype='socketcan')
    print("Monitoring CAN bus...")
    while True:
        try:
            message = bus.recv(1)  # Wait 1 second for a message
            if message:
                if message.is_error_frame:
                    print(f"Error Frame Detected: {message}")
            else:
                print("No message received. Checking state...")
        except can.exceptions.BusError as e:
            print(f"Bus Error: {e}")
        except Exception as ex:
            print(f"Other Error: {ex}")

if __name__ == "__main__":
    monitor_bus("vcan0")  # Replace 'can0' with your CAN interface
