from periphery import PWM
import time

class SERVO():
    def __init__(self, pwmchip, pwmchannel) -> None:
        self.pwm = PWM(pwmchip, pwmchannel)
        self.pwm.frequency = 50
        self.pwm.duty_cycle = 0.025
        self.pwm.polarity = "inversed"
        self.angle = 0
        pass
    
    def set_angle(self, angle:int):
        if angle < 0 or angle > 180:
            print("角度应在0到180度之间")
            return False
        self.angle = angle
        self.pwm.duty_cycle = 0.025 + (0.1 * (self.angle/180))

    def enable(self):
        self.pwm.enable()

    def disable(self):
        self.pwm.disable()
    
    def close(self):
        self.pwm.close()