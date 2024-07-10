import threading
import time
import cv2
from flask import Flask, render_template, request, Response, make_response
from pycode.driver import DRIVER
from pycode.sounddir import SOUNDDIR
from pycode.visualv1 import VISUAL
import numpy as np
from pycode.servo import SERVO
s1 = SERVO(0,0)
s2 = SERVO(1,0)
s2.enable()
s2.set_angle(180)
s1.enable()
s1.set_angle(0)

s = SOUNDDIR(40, 37, 34262)
s.calDirOnce()
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
driver1.setVel(0.5)
visual = VISUAL(driver1, mode=1, target="blue")
visual.start()
app = Flask(__name__)
turndire = True
isai = False
    
#相机推流
def gen(camera):
    print(1)
    while True:
        frame = camera.get_frame()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
#相机喂流
@app.route('/video_feed')
def video_feed():
    print(2)
    return Response(gen(visual),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


# if __name__ == '__main__':
#     app.run(host='0.0.0.0', debug=False)

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
        visual.isai = isai
    else:
        isai = False
        visual.isai = isai
        driver1.stop()
    # print(1111)
    return ""

@app.route('/pickBall', methods=['POST'])
def pickBall():
    s2.set_angle(180)
    s1.set_angle(0)
    time.sleep(3)
    s2.set_angle(90)
    s1.set_angle(90)
    return ""

@app.route('/returnBall', methods=['POST'])
def returnBall():
    
    
    s.calDirOnce()
    # print(s.dir)
    driver1.setVel(0.15)
    driver1.move_back()
    time_start = time.time()
    def func():
        while time.time() - time_start < 8:
            s.calDirOnce()
            # print(s.dir)
            if s.dir < 10:
                s2.set_angle(180)
                s1.set_angle(0)
                time.sleep(3)
                s2.set_angle(90)
                s1.set_angle(90)
                # print("too closer")
                break
            time.sleep(0.05)
            """"""
        driver1.stop()
    # driver1.move_forward()
    thread_func = threading.Thread(target=func)
    thread_func.start()
    return ""
@app.route('/red', methods=['POST'])
def red():
    visual.target = "red"
    return ""
@app.route('/purple', methods=['POST'])
def purple():
    visual.target = "purple"
    return ""
@app.route('/blue', methods=['POST'])
def blue():
    visual.target = "blue"
    return ""
@app.route('/yellow', methods=['POST'])
def yellow():
    visual.target = "yellow"
    return ""

@app.route('/color', methods=['POST'])
def color():
    visual.mode = 1
    return ""
@app.route('/number', methods=['POST'])
def number():
    visual.mode = 2
    return ""
@app.route('/brack', methods=['POST'])
def brack():
    driver1.stop()
    return ""
@app.route('/over', methods=['POST'])
def over():
    exit(0)
    return ""
app.run(host="0.0.0.0",port=5000)

