from periphery import GPIO
gpio = GPIO("/dev/gpiochip0", 1, "out")
gpio.write(True)