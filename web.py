import threading
import time
from flask import Flask, render_template, request
from pycode.driver import DRIVER
from pycode.sounddir import SOUNDDIR
from pycode.Visual import VISUAL

s = SOUNDDIR(40, 37, 34262)
s.calDirOnce()
# import time
gpiochip = "/dev/gpiochip0"
driver1 = DRIVER(
    gpiochip, 2,
    gpiochip, 3,
    gpiochip, 56,
    gpiochip, 58,
    gpiochip, 1,
    gpiochip, 41,
    gpiochip, 57,
    gpiochip, 59)
driver1.setVel(0.3)
visual = VISUAL(driver1)
app = Flask(__name__)
turndire = True
isai = False
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/onmousedown', methods=['POST'])
def onmousedown():
    # s.calDirOnce()
    # print(s.dir)
    global isai
    if isai:
        return ""
    move_type = request.get_json()["type"]
    if move_type == "f":
        driver1.move_forward()
    elif move_type == "fl":
        driver1.move_forward_left()
    elif move_type == "fr":
        driver1.move_forward_right()
    elif move_type == "l":
        driver1.move_left()
    elif move_type == "c":
        global turndire
        if turndire:
            driver1.turn_clockwise()
        else:
            driver1.turn_counterclockwise()
    elif move_type == "r":
        driver1.move_right()
    elif move_type == "bl":
        driver1.move_back_left()
    elif move_type == "b":
        driver1.move_back()
    elif move_type == "br":
        driver1.move_back_right()
    return ""

@app.route('/onmouseup', methods=['POST'])
def onmouseup():
    driver1.stop()
    return ""

@app.route('/changeTurnDire', methods=['POST'])
def changeTurnDire():
    global turndire
    turndire = not turndire
    return ""

@app.route('/aiMode', methods=['POST'])
def aiMode():
    global isai
    if not isai:
        isai = True
        visual.start()
    else:
        isai = False
        visual.close()
        driver1.stop()
    # print(1111)
    return ""

@app.route('/pickBall', methods=['POST'])
def pickBall():
    print(1111)
    return ""

@app.route('/returnBall', methods=['POST'])
def returnBall():
    s.calDirOnce()
    # driver1.setVel(0.15)
    driver1.move_back()
    time_start = time.time()
    def func():
        while time.time() - time_start < 8:
            s.calDirOnce()
            # print(s.dir)
            if s.dir < 10:
                # print("too closer")
                break
            time.sleep(0.05)
            """"""
        driver1.stop()
    # driver1.move_forward()
    thread_func = threading.Thread(target=func)
    thread_func.start()
    return ""

app.run(host="192.168.43.28",port=5000)

