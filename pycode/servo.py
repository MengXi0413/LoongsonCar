from periphery import PWM
import time

class SERVO():
    """自定义的180°舵机类
    
    使用periphery.PWM实现
    """
    def __init__(self, pwmchip:int=0, pwmchannel:int=0) -> None:
        """初始化SERVO
        
        pwmchip: pwmchip 默认为0 可通过 ls /sys/class/pwm 查看
        pwmchannel: pwmchannel 默认为0 是pwmchip下包含的pwmchannel
        """
        self.pwm = PWM(pwmchip, pwmchannel)
        self.pwm.frequency = 50
        self.pwm.duty_cycle = 0.025
        self.pwm.polarity = "inversed"
        self.angle = 0
        pass
    
    def set_angle(self, angle:int) -> bool:
        """设置舵机角度
        
        angle: 角度，单位 度，应介于0-180°之间
        """
        if angle < 0 or angle > 180:
            print("角度应在0到180度之间")
            return False
        self.angle = angle
        self.pwm.duty_cycle = 0.025 + (0.1 * (self.angle/180))
        return True

    def enable(self) -> None:
        """激活SERVO
        
        实际为激活舵机对应的PWM，在设置角度之前应该先调用此方法来激活PWM
        """
        self.pwm.enable()

    def disable(self) -> None:
        """停用SERVO
        
        实际为停用舵机对应的PWM
        """
        self.pwm.disable()
    
    def close(self) -> None:
        """关闭SERVO
        
        实际为关闭舵机对应的PWM，关闭之前默认调用disable()
        """
        self.disable()
        self.pwm.close()
