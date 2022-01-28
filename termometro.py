from lib.mlx90614 import MLX90614
from machine import SoftI2C, Pin,I2C
import time

i2c =SoftI2C(scl=Pin(23), sda=Pin(2),freq = 100000)
sensor = MLX90614(i2c)

while True:
    print(sensor.read_object_temp())
    time.sleep_ms(1000)