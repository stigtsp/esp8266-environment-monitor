import time
import machine
import tmp102

i2c = machine.I2C(scl=machine.Pin(5), sda=machine.Pin(4))
sensor = tmp102.Tmp102(i2c, 0x48)

while True:
    print("temp: sensor.temperature")
    time.sleep_ms(3000)
