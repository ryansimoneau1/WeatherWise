from machine import Pin, ADC, I2C, UART
from aht21 import AHT21
import time

# UART Constants
START = 0xA0
NOTED = 0xC0 # acknowledge from controller
STOP = 0xE0

print(type(START))

uart = UART(0)
uart.init(baudrate=115200,bits=8,parity=None,stop=1)

adc0 = ADC(Pin(26))

led = Pin(25, Pin.OUT)

aht21 = AHT21(1,Pin(15),Pin(14),250000)
aht21.init()

uart_rx = 0
while uart_rx != START:	# wait for command to start recording data
    data = uart.read()
    if data is not None:
        uart_rx = int.from_bytes(data, "little")
    led.on()
    time.sleep(2)
    led.toggle()
    time.sleep(0.2)
    
# acknowledge start
uart.write(bytes(NOTED))
for _ in range(0,15): # visual feedback
    led.toggle()
    time.sleep(0.05)
   
MINUTES = 0
while MINUTES < 1:
    data = uart.read(1)
    if uart_rx is not None:
        MINUTES = int.from_bytes(data, "little")
    
    led.off()
    time.sleep(2)
    led.toggle()
    time.sleep(0.2)
print(MINUTES)

for t in range(1, 60*MINUTES):
    led.toggle()
    
    sensor_data = aht21.th_measure_raw()
    
#     file.write(f"{t}, {sensor_data[0]: .2f}, {sensor_data[1]: .2f}\n") # sec, temp, humidity
#     print(f"Temperature: {sensor_data[0]: .2f}°F, Humidity: {sensor_data[1]: .2f}%")
    uart.write(bytes(sensor_data))
    time.sleep(1)
    
# print(f"Done!\nTime elapsed: {MINUTES} minute(s).")    
    
while True:
    led.toggle()
    time.sleep(0.20)
    
    