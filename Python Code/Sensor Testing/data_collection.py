import serial
from datetime import datetime
import os

MINUTES = 5


# process raw sensor data for csv file
def process_data(raw_data):
    temp = ((((raw_data[3] & 0x0F) << 16) | (raw_data[4] << 8) | raw_data[5]) * 360) / 1048576 - 58
    humidity = ((raw_data[1] << 12) | (raw_data[2] << 4) | (raw_data[3] >> 4)) * 100 / 1048576
    t_and_h = (temp, humidity)
    return t_and_h


# UART
port = "COM3"  # default pico uart baud rate
baud = 115200
serial_conn = serial.Serial(port, baud)
# print(serial_conn)

# Time
now = datetime.now()
date = (now.month, now.day, now.year)
time_stamp = (now.hour, now.minute)

# File Name
file_name = f"T_H_Data {date[0]}_{date[1]}_{date[2]} {time_stamp[0]}_{time_stamp[1]}.txt"
file_directory = f"C:\\Users\\ryans\\OneDrive\\Documents\\Weatherwise Project\\Research\\Temperature and Humidity Research\\Data Collection"
file_path = os.path.join(file_directory, file_name)

file = open(file_path, "a", encoding="utf-8")
file.write("Time (s), Temperature (°F), Humidity (%)\n")

for t in range(1, 60 * MINUTES + 1):  # take data for a minute
    serial_data = serial_conn.read(16).decode("utf-8").strip()
    print(f"{serial_data}")
    file.write(f"{t}, {serial_data}\n")  # sec, temp, humidity

file.close()
serial_conn.close()
print(f"Done!\nTime elapsed: {MINUTES} minute(s).")
