
import os
import time
import json
from datetime import datetime

LOG_DIR = "F:/linealert-sync-drive/beadvol_logs"
SESSION_FILE = os.path.join(LOG_DIR, f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.beadvol")

# Create log directory if not present
os.makedirs(LOG_DIR, exist_ok=True)

# Simulated raw USB packets (replace with live capture later)
simulated_packets = [
    {"src": "1-1", "dst": "host", "event": "DEVICE_CONNECT", "ts": time.time()},
    {"src": "host", "dst": "1-1", "event": "ENUMERATION_REQUEST", "ts": time.time() + 1},
    {"src": "1-1", "dst": "host", "event": "ENUMERATION_RESPONSE", "ts": time.time() + 2},
    {"src": "1-1", "dst": "host", "event": "HID_INPUT", "data": "0x1a", "ts": time.time() + 3},
]

def save_bead(bead):
    with open(SESSION_FILE, "a") as f:
        f.write(json.dumps(bead) + "\n")

def run_logger():
    print(f"[+] Logging to {SESSION_FILE}")
    for packet in simulated_packets:
        bead = {
            "id": f"bead-{int(packet['ts'] * 1000)}",
            "timestamp": packet["ts"],
            "type": packet.get("event", "UNKNOWN"),
            "src": packet.get("src", "unknown"),
            "dst": packet.get("dst", "unknown"),
            "payload": packet.get("data", None),
        }
        save_bead(bead)
        print(f"[+] Logged {bead['type']} bead")
        time.sleep(0.5)

if __name__ == "__main__":
    run_logger()
