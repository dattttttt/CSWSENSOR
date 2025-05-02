# temp_humidity_listener.py
import serial
from datetime import datetime

TEMP_SENSOR_ID = "0502E7A1"

def extract_sender_id(raw):
    if len(raw) >= 22:
        return ''.join(f"{b:02X}" for b in raw[15:19])
    return None

with serial.Serial("COM3", 57600, timeout=1) as ser:
    while True:
        raw = ser.read(32)
        if len(raw) < 22:
            continue

        raw_hex = raw.hex().upper()
        sender_id = extract_sender_id(raw)

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{now} → RAW: {raw_hex}")

        if sender_id == TEMP_SENSOR_ID:
            print(f"{now} → Nhiệt độ/Độ ẩm từ cảm biến {sender_id}")
        else:
            print(f"{now} → Thiết bị không khớp ID ({sender_id})")
