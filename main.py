import time
import dht
import machine
from machine import Pin, I2C, deepsleep

import SHT31
from lora_lib import configure_lora_module, send_msghex

# Define firmware parameters
UPLINK_INTERVAL = 60000         # In milliseconds
FIRST_TIME = True

# PB7 -> Green  (SDA)
# PB6 -> Yellow (SCL)

# Configure DHT22 Sensor
i2c = I2C(id=1, scl=Pin(7), sda=Pin(6), freq =400000)
sensor = SHT31.SHT31(i2c, addr=0x44)

# Loop after joined network
while True:
    if FIRST_TIME:
        # Configure LoRa Module
        status = configure_lora_module()
        FIRST_TIME = False

    # Read sensor data
    temp_humi = sensor.get_temp_humi()
    humidity = temp_humi[1]
    temperature = temp_humi[0]

    # Convert into hex for transmission
    sensor_data_hex = f'{int(humidity * 100):04x}{int(temperature * 100):04x}'

    # Transmit data
    send_msghex(sensor_data_hex)

    # Sleep for UPLINK INTERVAL (adjust as needed)
    print(f"Temperature: {temperature}")
    print(f"Humidity: {humidity}")
    time.sleep_ms(UPLINK_INTERVAL) 