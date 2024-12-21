from machine import Pin, ADC, I2C
import time

class AHT21:
    def __init__(self, i2c_chan, scl_pin, sda_pin, freq):
        self.AHT21_ADDR		= 0x38
        self.AHT21_INIT_CMD = b'\xBE\x08\x00'
        self.AHT21_STAT_CMD = b'\x71'
        self.AHT21_MEASURE_CMD = b'\xAC\x33\x00'
        
        self.i2c_channel = i2c_chan
        self.i2c = I2C(id=i2c_chan,scl=scl_pin,sda=sda_pin,freq=freq)        
        
    def init(self):
        print("running initialization")
        time.sleep(0.1) # wait 100 ms at startup
        self.i2c.writeto(self.AHT21_ADDR,self.AHT21_INIT_CMD)
        aht21_stat = self.check_status()
        if aht21_stat:
            print(f"AHT21 on SPI{self.i2c_channel} is working correctly")
        else:
            print(f"AHT21 on SPI{self.i2c_channel} initialization failed")
            
            
    def check_status(self):
        status = self.i2c.readfrom(self.AHT21_ADDR,1)[0]
        return status & 0x18 == 0x18 # True/False
    
    def trig_measure(self):
        self.i2c.writeto(self.AHT21_ADDR, self.AHT21_MEASURE_CMD)
    
    def read_sensor_data(self):
        raw_sensor_data = self.i2c.readfrom(self.AHT21_ADDR,7)
        return raw_sensor_data
    
    def process_data(self, raw_data):
        temp = ((((raw_data[3] & 0x0F) << 16) | (raw_data[4] << 8) | raw_data[5]) * 360) / 1048576 - 58
        humidity = ((raw_data[1] << 12) | (raw_data[2] << 4) | (raw_data[3] >> 4)) * 100 / 1048576
        t_and_h = (temp, humidity)
        return t_and_h
    
    def th_measure(self):
        time.sleep(0.01) # wait 10 ms before measuring data
        self.trig_measure()
        time.sleep(0.08)
        raw_data = self.read_sensor_data()
        t_and_h = self.process_data(raw_data)
        return t_and_h

    def th_measure_raw(self):
        time.sleep(0.01)  # wait 10 ms before measuring data
        self.trig_measure()
        time.sleep(0.08)
        raw_data = self.read_sensor_data()
        return raw_data
        