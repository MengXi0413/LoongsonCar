from periphery import GPIO
import time
import threading
class SOUNDDIR():
    def __init__(self, trigPin, echoPin, v) -> None:
        self.trig = GPIO("/dev/gpiochip0", trigPin, "out")
        self.echo = GPIO("/dev/gpiochip0", echoPin, "in")
        self.vel = v
        self.dir = None
        self.trig.write(False)
        self.isable = False
        pass
    def enable(self):
        self.isable = True
        def func():
            while self.isable:
                self.trig.write(True)
                time.sleep(0.00001)
                self.trig.write(False)
                while not self.echo.read():
                    """"""
                time_start = time.time()
                while self.echo.read():
                    """"""
                time_end = time.time()
                sec = time_end - time_start
                self.dir = (self.vel * sec)/2
                time.sleep(0.1)
        thread_func = threading.Thread(target=func)
        thread_func.start()
    
    def disable(self):
        self.isable = False
    
    def getDir(self):
        return self.dir
    
    def calDirOnce(self):
        def func():
            self.trig.write(True)
            time.sleep(0.00001)
            self.trig.write(False)
            time_start = time.time()
            while not self.echo.read() and (time.time() - time_start < 2):
                """"""
            time_start = time.time()
            while self.echo.read() and (time.time() - time_start < 2):
                """"""
            time_end = time.time()
            sec = time_end - time_start
            self.dir = (self.vel * sec)/2
            return self.dir
        thread_func = threading.Thread(target=func)
        thread_func.start()


