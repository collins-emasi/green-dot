import time
import dht
import machine
from machine import deepsleep

from lora_lib import configure_lora_module, send_msghex

# Define firmware parameters
UPLINK_INTERVAL = 60000         # In milliseconds
FIRST_TIME = True

# Configure DHT22 Sensor
temp_sensor = dht.DHT22(machine.Pin(6))

# Loop after joined network
while True:
    if FIRST_TIME:
        # Configure LoRa Module
        status = configure_lora_module()
        FIRST_TIME = False

    # Read sensor data
    humidity = temp_sensor.humidity()
    temperature = temp_sensor.temperature()

    # Convert into hex for transmission
    sensor_data_hex = f'{int(humidity):04x}{int(temperature):04x}'

    # Transmit data
    send_msghex(sensor_data_hex)

    # Deep sleep for 1 minute (adjust as needed)
    print("Going into deep sleep...")
    time.sleep_ms(1000)  # Ensure print statement is displayed
    deepsleep(UPLINK_INTERVAL)  # Sleep for 1 minute (60000 milliseconds)