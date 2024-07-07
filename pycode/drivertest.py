from driver import DRIVER
import time
gpiochip = "/dev/gpiochip0"
driver1 = DRIVER(
    gpiochip, 2,
    gpiochip, 3,
    gpiochip, 56,
    gpiochip, 58,
    gpiochip, 38,
    gpiochip, 41,
    gpiochip, 57,
    gpiochip, 59)
driver1.move_forward()
time.sleep(1)
driver1.stop()
driver1.setVel(0.05)
driver1.move_forward()
time.sleep(1)
driver1.stop()

