ESP8266 Environmental Sensor in Micropython
===========================================

To get started:

1. Install `micropython` on your ESP8266.
2. `pip3 install adafruit-ampy`
3. Create a `config.json`
3. `AMPY_PORT=/dev/ttyUSB0 make upload`

Wiring:
------
TMP36 on A0,3.3v,Gnd
CCS811 on D2,D3,3.3v,Gnd,(wake to gnd)

Note: 
----
You might need to supply a different i2c address for the CCS811 depending on
your module.





