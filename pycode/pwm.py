from periphery import GPIO
import threading
import time

class PWM():
    """自定义的PWM类
    
    通过periphery.GPIO模拟实现PWM功能
    """
    def __init__(self, GPIO_CHIP:str="/dev/gpiochip0", GPIO_LINE:int=0, period:int=1000000, duty_cycle:float=0.85, isgpio:bool=False, gpio:GPIO=None) -> None:
        """初始化PWM

        GPIO_CHIP: gpiochip 默认为/dev/gpiochip0 具体可以至/dev/目录下查看
        GPIO_LINE: gpioline 默认为0 可以使用 sudo gpioinfo 查看，一般与开发板手册上对引脚的标注一致
        period: 周期 默认为1000000 单位 纳秒
        duty_cycle: 占空比 默认为0.85 即一个周期中低电平所占比例
        isgpio: 默认为False 如果实例化PWM时传入gpiochip与gpioline则设置为False，如果传入GPIO实例则设置为True，此时gpio参数应该为一个GPIO实例
        gpio: 一个GPIO实例
        """
        if(duty_cycle > 1):
            duty_cycle = 0.85
            print("占空比不能大于1.0，以调整至默认值0.85")
            # return
        if not isgpio:
            self.gpio = GPIO(GPIO_CHIP, GPIO_LINE, "out")
        else:
            self.gpio = gpio
        self.gpio.write(False)
        self.GPIO_CHIP = GPIO_CHIP
        self.GPIO_LINE = GPIO_LINE
        self.period = period
        self.isable = False
        self.duty_cycle = duty_cycle
        self.down_time = (period*duty_cycle)/1000000000
        self.up_time = (self.period/1000000000)-self.down_time

    def _updata(self) -> None:
        """更新周期以及占空比"""
        self.down_time = (self.period*self.duty_cycle)/1000000000
        self.up_time = (self.period/1000000000)-self.down_time

    def enable(self) -> None:
        """激活PWM
        
        使用threading.Thread创建线程，避免堵塞运行，使用self.isable变量控制激活状态
        """
        self.isable = True
        def thread1():
            try:
                while self.isable:
                    self.gpio.write(True)
                    time.sleep(self.up_time)
                    self.gpio.write(False)
                    time.sleep(self.down_time)
            except Exception as e:
                # print(e)
                self.close()
                print(f"GPIO_CHIP:{self.GPIO_CHIP} GPIO_LINE:{self.GPIO_LINE}激活PWM时发生错误,已关闭PWM。错误信息：\n{e}")     
        thread_func = threading.Thread(target=thread1)
        thread_func.start()
        
            
    def disable(self) -> None:
        """停用PWM
        
        通过设置 self.isable = False 来关闭在enable()中创建的线程，同时将引脚覆写为低电平
        """
        self.isable = False
        self.gpio.write(False)
        
    def close(self):
        """关闭PWM

        首先停用PWM然后释放资源，该PWM彻底关闭，无法再通过enable()启动PWM
        """
        self.isable = False
        self.gpio.write(False)
        self.gpio.close()

    def edit_period(self, new_period:int) -> None:
        """更改周期
        
        new_period: 新的周期大小，单位 纳秒
        """
        self.period = new_period
        self._updata()
    
    def edit_duty_cycle(self, new_duty_cycle:float) -> None:
        """更改占空比

        如果要将占空比设置为0或者1.0来实现持续高低电平，请使用full_duty()以及zero_duty()实现
        new_duty_cycle: 新的占空比大小
        """
        # print(f"更改占空比{new_duty_cycle}")
        self.duty_cycle = new_duty_cycle
        self._updata()

    def full_duty(self) -> None:
        """将PWM设置为满占空
        
        调用disable()再将引脚覆写为低电平，并没有对self.duty_cycle进行修改
        可通过enable()直接重新启动PWM
        """
        self.disable()
        self.gpio.write(False)
    
    def zero_duty(self) -> None:
        """将PWM设置为零占空
        
        调用disable()再将引脚覆写为高电平，并没有对self.duty_cycle进行修改
        可通过enable()直接重新启动PWM
        """
        self.disable()
        self.gpio.write(True)
