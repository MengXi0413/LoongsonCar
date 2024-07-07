from Visual import VISUAL
# from visualdriver import VISUALDRIVER
# from driver import DRIVER
# import time
# gpiochip = "/dev/gpiochip0"
# driver1 = DRIVER(
#     gpiochip, 2,
#     gpiochip, 3,
#     gpiochip, 56,
#     gpiochip, 58,
#     gpiochip, 38,
#     gpiochip, 41,
#     gpiochip, 57,
#     gpiochip, 59)

v = VISUAL()
v.start()
# count = v.count
# while True:
#     if not count == v.count:
#         continue

#     if abs(v.max_r_gap) > v.max_gap:
#         if v.max_r_gap < 0:
#             driver1.turn_counterclockwise()
#         if v.max_r_gap == 0:
#             driver1.stop()
#         else:
#             driver1.turn_clockwise()
#     else:
#         driver1.stop()