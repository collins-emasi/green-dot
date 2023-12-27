import time
from machine import UART

from credentials import *
from led import blink_rgb_led, BLUE, RED, CYAN, PURPLE

# Set your UART parameters (baudrate, etc.)
uart = UART(0, baudrate=9600)  # UART0, tx=GPIO17, rx=GPIO16
uart.init(9600, bits=8, parity=None, stop=1)

def send_at_command(command, response_timeout=1000):
    uart.write(command + b'\r\n')
    time.sleep_ms(response_timeout)
    return uart.read().decode('utf-8')

def read_all_ids():
    response = send_at_command(b'AT+ID')
    print(response)

def read_all_keys():
    response = send_at_command(b'AT+KEY')
    print(response)

def read_id(identifier):
    command = b'AT+ID=' + identifier
    response = send_at_command(command)
    print(response)

def set_id(identifier, value):
    command = b'AT+ID=' + identifier + b', "' + value + b'"'
    response = send_at_command(command)
    print(response)

def set_key(identifier, value):
    command = b'AT+KEY=' + identifier + b', "' + value + b'"'
    response = send_at_command(command)
    print(response)

def set_class(lwclass):
    command = b'AT+CLASS=' + lwclass
    response = send_at_command(command)
    print(response)

def enter_dfu_mode(state):
    command = b'AT+DFU=' + state
    response = send_at_command(command)
    print(response)

def set_work_mode(mode):
    command = b'AT+MODE=' + mode
    response = send_at_command(command)
    print(response)

def set_addr_mode(mode):
    command = b'AT+ADDR=' + mode
    response = send_at_command(command)
    print(response)

def send_msg(data):
    command = b'AT+MSG=' + data
    response = send_at_command(command)
    print(response)

def soft_reset():
    response = send_at_command(b'AT+RESET')
    print(response)

def send_cmsg(data, timeout=5000):
    command = b'AT+CMSG=' + data
    response = send_at_command(command)
    if "FPENDING" in response:
        print("Downlink Received!")
    print(response)

def send_msghex(hex_data, timeout=5000):
    command = b'AT+MSGHEX=' + hex_data
    response = send_at_command(command)
    if "ERROR" not in response:
        blink_rgb_led(PURPLE)
    if "FPENDING" in response:
        print("Downlink Received!")
    print(response)

def join_network(timeout=10000):
    command = b'AT+JOIN'
    response = send_at_command(command, response_timeout=timeout)
    if "Joined already" in response:
        read_all_ids()
        print(response)
        blink_rgb_led(CYAN)
        return True
    elif "Network joined" in response:
        print(response)
        read_all_ids()
        blink_rgb_led(BLUE)
        return True
    elif "Join failed" in response:
        print(response)
        blink_rgb_led(RED)
        return False

def configure_lora_module():
    set_work_mode("LWOTAA")

    # Set OTAA parameters
    # set_id("AppEui", JoinEui.encode())
    # set_key("APPKEY", APPKEY.encode())
    # set_id("DevEui", DevEui.encode())

    # Join the network using OTAA
    status = join_network()
    return status