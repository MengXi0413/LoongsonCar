from periphery import GPIO
import threading
import time

class PWM():
    def __init__(self, GPIO_CHIP, GPIO_LINE, period=1000000, duty_cycle=0.85, isgpio=False, gpio:GPIO=None):
        if(duty_cycle > 1):
            duty_cycle = 0.5
            print("[DUTY_CYCLE ERROR]: duty_cycle is bigger than 1.0")
            return
        if not isgpio:
            self.gpio = GPIO(GPIO_CHIP, GPIO_LINE, "out")
        else:
            self.gpio = gpio
        self.gpio.write(False)
        self.GPIO_CHIP = GPIO_CHIP
        self.period = period
        self.isable = False
        self.duty_cycle = duty_cycle
        self.down_time = (period*duty_cycle)/1000000000
        self.up_time = (self.period/1000000000)-self.down_time

    def _updata(self):
        self.down_time = (self.period*self.duty_cycle)/1000000000
        self.up_time = (self.period/1000000000)-self.down_time

    def enable(self):
        self.isable = True
        def thread1():
            try:
                while self.isable:
                    self.gpio.write(True)
                    time.sleep(self.up_time)
                    self.gpio.write(False)
                    time.sleep(self.down_time)
            except Exception as e:
                print(e)
                self.gpio.close()
                print(f"[PWM ERROR]:pwm[GPIO_CHIP is {self.GPIO_CHIP}]")     
        thread_func = threading.Thread(target=thread1)
        thread_func.start()
        
            
    def disable(self):
        self.isable = False
        self.gpio.write(False)
        
    def close(self):
        self.isable = False
        self.gpio.write(False)
        self.gpio.close()

    def edit_period(self, new_period):
        self.period = new_period
        self._updata()
    
    def edit_duty_cycle(self, new_duty_cycle):
        self.duty_cycle = new_duty_cycle
        self._updata()

    def full_duty(self):
        self.disable()
        self.gpio.write(False)
    
    def zero_duty(self):
        self.disable()
        self.gpio.write(True)

# class PWMConsole():
#     def __init__(self, gpioList, period=1000000, duty_cycle=0.85, isgpio=False, gpio:GPIO=None):
#         if(duty_cycle > 1):
#             duty_cycle = 0.5
#             print("[DUTY_CYCLE ERROR]: duty_cycle is bigger than 1.0")
#             return
#         self.pwmList = []
#         for chip, line in gpioList:
#             self.pwmList.append(GPIO(chip, line, "out"))
        
#         for pwm in self.pwmList:
#             pwm.write(False)

#         self.period = period
#         self.isable = False
#         self.duty_cycle = duty_cycle
#         self.down_time = (period*duty_cycle)/1000000000
#         self.up_time = (self.period/1000000000)-self.down_time

#     def _updata(self):
#         self.down_time = (self.period*self.duty_cycle)/1000000000
#         self.up_time = (self.period/1000000000)-self.down_time

#     def write_true(self):
#         for pwm in self.pwmList:
#             pwm.write(True)
    
#     def write_False(self):
#         for pwm in self.pwmList:
#             pwm.write(False)

#     def enable(self):
#         self.isable = True
#         def thread1():
#             try:
#                 while self.isable:
#                     self.write_true()
#                     time.sleep(self.up_time)
#                     self.write_False()
#                     time.sleep(self.down_time)
#             except Exception as e:
#                 print(e)
#                 self.gpio.close()
#         thread_func = threading.Thread(target=thread1)
#         thread_func.start()
        
            
#     def disable(self):
#         self.isable = False
#         self.write_False()
        
#     def close(self):
#         self.isable = False
#         self.write_False()
#         for pwm in self.pwmList:
#             pwm.close()
    

#     def edit_period(self, new_period):
#         self.period = new_period
#         self._updata()
    
#     def edit_duty_cycle(self, new_duty_cycle):
#         self.duty_cycle = new_duty_cycle
#         self._updata()
