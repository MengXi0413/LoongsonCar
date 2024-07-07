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
driver1.stop()
# driver1.move_forward(1)
# driver1.move_forward(1)
# driver1.move_forward(3)
# driver1.turn_clockwise()
# time.sleep(2)
# driver1.turn_counterclockwise()
# # driver1.move_left()
# # time.sleep(1)
# # driver1.move_right()
# # time.sleep(1)
# # driver1.move_back()
# time.sleep(2)
# driver1.stop()
# driver1.wheel2.forward()
# a = input("--------------------")
# driver1.wheel3.forward()
# a = input("--------------------")
# driver1.wheel4.forward()
# a = input("--------------------")
# driver1.move_forward()
# print("--------")
# time.sleep(3)
# driver1.stop()
# print("--------")
# time.sleep(3)
# driver1.move_forward()
# print("--------")
# time.sleep(3)
# driver1.stop()
# driver1.close()
# print("--------")
# time.sleep(3)
# driver1.move_forward()
# pwm0 = PWM("/dev/gpiochip0",40,period=5000000,duty_cycle=0.5)
# pwm0.enable()
# # pwm0.disable()
# pwm0.edit_duty_cycle(0.9)
# # a = input("please enter to disable pwm\n")
# # pwm0.disable()
# b = True
# while True:
#     a = input("输入周期和占空比\n").split(" ")
#     pwm0.edit_period(int(a[0]))
#     pwm0.edit_duty_cycle(float(a[1] ))
#     c = input("键入已暂停")
#     pwm0.disable()

