import time
try:
    from pwm import PWM
except:
    from pycode.pwm import PWM
from threading import Timer
class WHEEL():
    def __init__(self, pwm1:PWM, pwm2:PWM) -> None:
        self.pwm1 = pwm1
        self.pwm2 = pwm2
        self.velocity = 0.5
        pass

    def edit_velocity(self, vel):
        self.velocity = vel
        self.pwm1.edit_duty_cycle(1 - self.velocity)
        self.pwm2.edit_duty_cycle(1 - self.velocity)
        # if self.pwm1.isable:
        #     self.pwm1.edit_duty_cycle(1 - self.velocity)
        # if self.pwm2.isable:
        #     self.pwm2.edit_duty_cycle(1 - self.velocity)

    def forward(self):
        self.pwm1.enable()
        self.pwm2.full_duty()
        pass

    def back(self):
        self.pwm1.full_duty()
        self.pwm2.enable()
        pass

    def standby(self):
        self.pwm1.full_duty()
        self.pwm2.full_duty()
        pass

    def brake(self):
        self.pwm1.zero_duty()
        self.pwm2.zero_duty()
        time.sleep(0.1)
        self.standby()
        pass

    def close(self):
        self.pwm1.close()
        self.pwm2.close()
    
class DRIVER():
    def __init__(self, 
                 wheel1_pwm1_gpiochip, wheel1_pwm1_gpioline,
                 wheel1_pwm2_gpiochip, wheel1_pwm2_gpioline,
                 wheel2_pwm1_gpiochip, wheel2_pwm1_gpioline,
                 wheel2_pwm2_gpiochip, wheel2_pwm2_gpioline,
                 wheel3_pwm1_gpiochip, wheel3_pwm1_gpioline,
                 wheel3_pwm2_gpiochip, wheel3_pwm2_gpioline,
                 wheel4_pwm1_gpiochip, wheel4_pwm1_gpioline,
                 wheel4_pwm2_gpiochip, wheel4_pwm2_gpioline
                 ) -> None:
        self.wheel1 = WHEEL(PWM(wheel1_pwm1_gpiochip, wheel1_pwm1_gpioline),
                            PWM(wheel1_pwm2_gpiochip, wheel1_pwm2_gpioline))
        self.wheel2 = WHEEL(PWM(wheel2_pwm1_gpiochip, wheel2_pwm1_gpioline),
                            PWM(wheel2_pwm2_gpiochip, wheel2_pwm2_gpioline))
        self.wheel3 = WHEEL(PWM(wheel3_pwm1_gpiochip, wheel3_pwm1_gpioline),
                            PWM(wheel3_pwm2_gpiochip, wheel3_pwm2_gpioline))
        self.wheel4 = WHEEL(PWM(wheel4_pwm1_gpiochip, wheel4_pwm1_gpioline),
                            PWM(wheel4_pwm2_gpiochip, wheel4_pwm2_gpioline))
        self.state = "stop"
        pass
    def stop(self):
        self.wheel1.standby()
        self.wheel2.standby()
        self.wheel3.standby()
        self.wheel4.standby()
        self.state = "stop"
        pass
    def close(self):
        self.wheel1.close()
        self.wheel2.close()
        self.wheel3.close()
        self.wheel4.close()
        self.state = "close"

    def move_forward(self, s=None):
        if self.state == "move_forward":
            print(f"当前已处于{self.state}状态！")
        self.wheel1.forward()
        self.wheel2.forward()
        self.wheel3.forward()
        self.wheel4.forward()
        self.state = "move_forward"
        if not (s is None):
            Timer(s, self.stop, ()).start()
        pass
    
    def move_back(self, s=None):
        if self.state == "move_back":
            print(f"当前已处于{self.state}状态！")
        self.wheel1.back()
        self.wheel2.back()
        self.wheel3.back()
        self.wheel4.back()
        self.state = "move_back"
        if not (s is None):
            Timer(s, self.stop, ()).start()
        pass

    def move_left(self, s=None):
        if self.state == "move_left":
            print(f"当前已处于{self.state}状态！")
        self.wheel1.back()
        self.wheel2.forward()
        self.wheel3.forward()
        self.wheel4.back()
        self.state = "move_left"
        if not (s is None):
            Timer(s, self.stop, ()).start()
        pass
    
    def move_right(self, s=None):
        if self.state == "move_right":
            print(f"当前已处于{self.state}状态！")
        self.wheel1.forward()
        self.wheel2.back()
        self.wheel3.back()
        self.wheel4.forward()
        self.state = "move_right"
        if not (s is None):
            Timer(s, self.stop, ()).start()
        pass

    def turn_clockwise(self, s=None):
        if self.state == "turn_clockwise":
            print(f"当前已处于{self.state}状态！")
        self.wheel1.forward()
        self.wheel2.back()
        self.wheel3.forward()
        self.wheel4.back()
        self.state = "turn_clockwise"
        if not (s is None):
            Timer(s, self.stop, ()).start()
        pass

    def turn_counterclockwise(self, s=None):
        if self.state == "turn_counterclockwise":
            print(f"当前已处于{self.state}状态！")
        self.wheel1.back()
        self.wheel2.forward()
        self.wheel3.back()
        self.wheel4.forward()
        self.state = "turn_counterclockwise"
        if not (s is None):
            Timer(s, self.stop, ()).start()
        pass

    def move_forward_left(self, s=None):
        if self.state == "move_forward_left":
            print(f"当前已处于{self.state}状态！")
        self.wheel1.standby()
        self.wheel2.forward()
        self.wheel3.forward()
        self.wheel4.standby()
        self.state = "move_forward_left"
        if not (s is None):
            Timer(s, self.stop, ()).start()
        pass
    
    def move_forward_right(self, s=None):
        if self.state == "move_forward_right":
            print(f"当前已处于{self.state}状态！")
        self.wheel1.forward()
        self.wheel2.standby()
        self.wheel3.standby()
        self.wheel4.forward()
        self.state = "move_forward_right"
        if not (s is None):
            Timer(s, self.stop, ()).start()
        pass

    def move_back_left(self, s=None):
        if self.state == "move_back_left":
            print(f"当前已处于{self.state}状态！")
        self.wheel1.back()
        self.wheel2.standby()
        self.wheel3.standby()
        self.wheel4.back()
        self.state = "move_back_left"
        if not (s is None):
            Timer(s, self.stop, ()).start()
        pass
    
    def move_back_right(self, s=None):
        if self.state == "move_back_right":
            print(f"当前已处于{self.state}状态！")
        self.wheel1.standby()
        self.wheel2.back()
        self.wheel3.back()
        self.wheel4.standby()
        self.state = "move_back_right"
        if not (s is None):
            Timer(s, self.stop, ()).start()
        pass

    def setVel(self, vel):
        self.wheel1.edit_velocity(vel)
        self.wheel1.edit_velocity(vel)
        self.wheel2.edit_velocity(vel)
        self.wheel3.edit_velocity(vel)
        self.wheel4.edit_velocity(vel)