import network
import time
import machine
import ujson
import ubinascii
import sys
from umqtt.robust import MQTTClient
import CCS811
from machine import ADC

with open('config.json') as fp:
    config = ujson.loads(fp.read())

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(config['wifi']['ssid'],config['wifi']['psk'])

while not station.isconnected():
    machine.idle()

ap_if = network.WLAN(network.AP_IF)
if ap_if.active():
  ap_if.active(False)

CLIENT_ID = ubinascii.hexlify(machine.unique_id())

c = MQTTClient(client_id = CLIENT_ID,
               server     = config['mqtt']['server'],
               user       = config['mqtt']['user'],
               password   = config['mqtt']['password'],
               port       = config['mqtt']['port'],
               ssl        = config['mqtt']['ssl']
)

c.connect()

topic_prefix = config['mqtt']['topic_prefix']

# CCS811 sensor
i2c = machine.I2C(scl=machine.Pin(5), sda=machine.Pin(4))
s = CCS811.CCS811(i2c, addr=91)

adc = ADC(0) #  TMP36 sensor

def publish(c, k, v):
    c.publish(topic_prefix + k, str(v), True)

while True:

    if s.data_ready():
        print('eCO2: %d ppm, TVOC: %d ppb' % (s.eCO2, s.tVOC))
        publish(c, "eCO2", s.eCO2)
        publish(c, "tVOC", s.tVOC)
    temp = adc.read() / 10
    print('Temp: %s' % temp)
    publish(c,"temp", temp)

    time.sleep_ms(3000)

c.disconnect()
