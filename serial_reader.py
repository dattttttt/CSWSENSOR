import serial
from pymongo import MongoClient
from datetime import datetime
import time

client = MongoClient("mongodb://localhost:27017/")
db = client["csw"]
tohop_col = db["tohop_logs"]
door_col = db["door_logs"]
temp_col = db["temp_logs"]

# ID cảm biến
BUTTON_ID = "002E5809"
DOOR_ID = "051D12C3"
TEMP_ID = "0502E7A1"

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

def decode_to_hop(byte_val):
    return TO_HOP_MAP.get(byte_val, f"Không rõ (0x{byte_val:02X})")

with serial.Serial("COM3", 57600, timeout=1) as ser:
    while True:
        raw = ser.read(32)
        if len(raw) < 28:
            continue

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{now} → RAW: {raw.hex().upper()}")

        sender_id = ''.join(f"{b:02X}" for b in raw[7:11])
        if sender_id == BUTTON_ID:
            tohop = decode_to_hop(raw[18])
            print(f"{now} → Nút: {tohop}")
            tohop_col.insert_one({"tohop": tohop, "time": now})

        elif sender_id == DOOR_ID:
            status = raw[27]
            state = "Đóng" if status == 0x00 else "Mở" if status == 0x80 else f"Không rõ (0x{status:02X})"
            print(f"{now} → Cửa: {state}")
            door_col.insert_one({"trang_thai": state, "time": now})

        elif sender_id == TEMP_ID:
            temp_raw = raw[-4]
            humi_raw = raw[-3]
            temperature = round((temp_raw * 40.0) / 250, 2)
            humidity = round((humi_raw * 100.0) / 250, 2)
            print(f"{now} → Nhiệt độ: {temperature}°C | Độ ẩm: {humidity}%")
            temp_col.insert_one({
                "temperature": temperature,
                "humidity": humidity,
                "time": now
            })

        else:
            print(f"{now} → Thiết bị lạ: {sender_id}")

        time.sleep(0.5)
