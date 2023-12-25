from ws2812 import WS2812
import utime
import machine

power = machine.Pin(11,machine.Pin.OUT)

BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
WHITE = (255, 255, 255)
COLORS = (BLACK, RED, YELLOW, GREEN, CYAN, BLUE, PURPLE, WHITE)

rgb_led = WS2812(12,1)  #WS2812(pin_num,led_count)

def blink_rgb_led(color):
    power.value(1)
    rgb_led.pixels_fill(color)
    rgb_led.pixels_show()
    utime.sleep(0.5)
    power.value(0)
