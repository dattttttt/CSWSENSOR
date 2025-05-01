from pymongo import MongoClient
import serial
from datetime import datetime
import time

TO_HOP_MAP = {
    0x82: "Tổ hợp 1",
    0x88: "Tổ hợp 2",
    0x81: "Tổ hợp 3",
    0x84: "Tổ hợp 4",
    0x8A: "Tổ hợp 5",
    0x85: "Tổ hợp 6",
    0x89: "Tổ hợp 7",
    0x86: "Tổ hợp 8",
}

def decode(byte_val):
    return TO_HOP_MAP.get(byte_val, f"Không rõ (0x{byte_val:02X})")

client = MongoClient("mongodb://localhost:27017/")
col = client['csw']['tohop_logs']

with serial.Serial("COM3", 57600, timeout=1) as ser:
    while True:
        raw = ser.read(32)
        if len(raw) < 16:
            continue
        byte = raw[11]
        tohop = decode(byte)
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        col.insert_one({"tohop": tohop, "time": now})
        print(f"{now} → {tohop}")
        time.sleep(0.5)
