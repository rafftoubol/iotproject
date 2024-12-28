import can
import time
import subprocess
import re


def get_can_bus_state(interface: str) -> str:
    """
    Returns the state of the given CAN interface (e.g., 'UNKNOWN', 'DOWN', 'UP').
    It parses the output of the 'ip link show dev <interface>' command.
    """
    try:
        result = subprocess.run(
            ["ip", "link", "show", "dev", interface],
            capture_output=True,
            text=True,
            check=True
        )
        # Typical output line for vcan0 might look like:
        # 4: vcan0: <NOARP,UP,LOWER_UP> mtu 72 qdisc noqueue state UNKNOWN mode DEFAULT group default qlen 1000
        lines = result.stdout.splitlines()
        if len(lines) > 1:
            # The second line generally has the link info we need:
            line = lines[1]
        else:
            # If only one line is returned, use that
            line = lines[0] if lines else ""
        
        # Use a regex to find 'state XYZ'
        match = re.search(r"\sstate\s+(\S+)", line)
        if match:
            return match.group(1)
        else:
            return "UNKNOWN"
    except subprocess.CalledProcessError:
        # If 'ip' command fails for some reason, fall back to UNKNOWN
        return "UNKNOWN"


if __name__ == "__main__":
    # Make sure the vcan0 interface is created and brought up beforehand:
    #
    #   sudo modprobe vcan
    #   sudo ip link add dev vcan0 type vcan
    #   sudo ip link set vcan0 up

    bus = can.interface.Bus(interface='socketcan', channel='vcan0')

    msg = can.Message(arbitration_id=0x111, data=[0x11, 0x22, 0x33], is_extended_id=False, is_rx=False)

    try:
        while True:
            bus.send(msg)
            # Fetch and print the bus state on each loop
            bus_state = get_can_bus_state('vcan0')
            print(f"Sent: {msg}, Bus state: {bus_state}")
            time.sleep(0.01)  # Send message every 10ms
    except KeyboardInterrupt:
        print("Stopped sending messages.")
