from typing import Union
from periphery import GPIO
import time
import threading
class SOUNDDIR():
    """自定义的超声波测距类

    使用periphery.GPIO来实现与传感器通信
    """
    def __init__(self, trigPin:int, echoPin:int, v:Union[int, float], GPIO_CHIP:str="/dev/gpiochip0") -> None:
        """初始化超声波测距
        
        trigPin: 激活引脚的GPIO_LINE 可以使用 sudo gpioinfo 查看，一般与开发板手册上对引脚的标注一致
        echoPin: 数据接收引脚的GPIO_LINE 可以使用 sudo gpioinfo 查看，一般与开发板手册上对引脚的标注一致
        v: 声速 单位cm/s
            声速温度公式: c=(33145+61t/℃)cm/s (其中330.45是在0℃)
                0℃声速:   33045CM/SC
                20℃声速:  34262CM/S
                40℃声速:  35485CM/S
            0℃-40℃声速误差7%左右。实际应用，如果需要精确距离值，必需要考虑温
            度影响，做温度补偿。
        GPIO_CHIP: gpiochip 默认为/dev/gpiochip0 具体可以至/dev/目录下查看
        """
        self.trig = GPIO(GPIO_CHIP, trigPin, "out")
        self.echo = GPIO(GPIO_CHIP, echoPin, "in")
        self.vel = v
        self.dir = None
        self.trig.write(False)
        self.isable = False
        pass
    def enable(self) -> None:
        """启动测距
        
        调用该方法后会创建一个线程不断进行测距，更新self.dir
        """
        self.isable = True
        def func():
            while self.isable:
                self.trig.write(True)
                time.sleep(0.00001)
                self.trig.write(False)
                time_start = time.time()
                while not self.echo.read() and (time.time() - time_start < 2):
                    """如果两秒内echoPin引脚没有传回低电平则跳出循环"""
                time_start = time.time()
                while self.echo.read() and (time.time() - time_start < 2):
                    """如果两秒内echoPin引脚没有传回高电平则跳出循环"""
                time_end = time.time()
                sec = time_end - time_start
                self.dir = (self.vel * sec)/2
                time.sleep(0.1)
        thread_func = threading.Thread(target=func)
        thread_func.start()
    
    def disable(self) -> None:
        """停用测距
        
        通过 self.isable = False 关闭enable()创建的线程
        """
        self.isable = False
    
    def getDir(self) -> float:
        """获取测距结果
        
        似乎没有什么用
        """
        return self.dir
    
    def calDirOnce(self) -> None:
        """进行一次测距

        创建线程并进行一次测距
        调用该方法后如果立即调用self.dir可能会出现数值未更新的情况, 可以适当延迟后后再读取self.dir的数值
        """
        def func():
            self.trig.write(True)
            time.sleep(0.00001)
            self.trig.write(False)
            time_start = time.time()
            while not self.echo.read() and (time.time() - time_start < 2):
                """如果两秒内echoPin引脚没有传回低电平则跳出循环"""
            time_start = time.time()
            while self.echo.read() and (time.time() - time_start < 2):
                """如果两秒内echoPin引脚没有传回高电平则跳出循环"""
            time_end = time.time()
            sec = time_end - time_start
            self.dir = (self.vel * sec)/2
            # return self.dir
        thread_func = threading.Thread(target=func)
        thread_func.start()


