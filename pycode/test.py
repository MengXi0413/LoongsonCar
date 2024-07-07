# from periphery import GPIO
# gpio = GPIO("/dev/gpiochip0", 1, "out")
# gpio.write(False)


# from Visual import VISUAL
# v = VISUAL()
# v.start()
import time
from servo import SERVO
s1 = SERVO(0,0)
s2 = SERVO(1,0)
s2.enable()
s2.set_angle(60)
s1.enable()
s1.set_angle(60)
while True:
    s2.set_angle(60)
    s1.set_angle(60)
    a = (input("度数："))
    if a == "1":
        break
    s1.set_angle(120)
    s2.set_angle(0)
    a = (input("度数："))
    if a == "1":
        break
    