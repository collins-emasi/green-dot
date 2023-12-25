import time
from machine import Pin
import rp2

@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
def uart_program():
    # Configuration
    pull(noblock)
    set(pins, 1) [1]
    
    # Wait for start bit
    wait(1, pin, 0) [1]

    # Shift in data
    in_(pins, 8) [8]

    # Wait for stop bit
    wait(1, pin, 1) [1]

    # Signal completion
    irq(rel(0))

# Create two StateMachine instances for TX and RX
sm_tx = rp2.StateMachine(0, uart_program, freq=2000000, set_base=Pin(18), in_base=Pin(19))
sm_rx = rp2.StateMachine(1, uart_program, freq=2000000, set_base=Pin(20), in_base=Pin(21))

# Set the IRQ handlers to print received data
sm_rx.irq(lambda p: print("Received:", sm_rx.get()))
sm_tx.irq(lambda p: print("Transmitted"))

# Start the StateMachines
sm_rx.active(1)
sm_tx.active(1)

# Function to send a byte
def uart_send_byte(data):
    sm_tx.put(data)
    time.sleep_us(100)  # Allow time for transmission to complete

# Function to receive a byte
def uart_receive_byte():
    while not sm_rx.irq().flags():
        pass  # Wait for reception to complete
    return sm_rx.get()