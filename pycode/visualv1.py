import cv2
import numpy as np
import threading
import numpy as np
try:
    from driver import DRIVER
except:
    from pycode.driver import DRIVER

class VISUAL():
    """自定义的视觉识别

    该类可以通过视觉识别控制一个DRIVER实例
    用于识别小车前方网球并控制小车向网球靠近
    """
    def __init__(self, driver:DRIVER, mode=0, target="blue") -> None:
        """初始化视觉识别
        
        driver: DRIVER类实例
        mode: 视觉识别模式
        target: 色块识别目标
        """
        self.driver = driver
        self.mode = mode
        self._mode = mode
        self.isAllPick = False
        self.noBall = True
        self.target = target
        self.isai = False
        self.isStart = False
        self.max_r_gap = -1
        self.max_size = -1
        self.max_gap = -1
        self.isable = True
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, 320)
        self.cap.set(4, 240)
        ret, frame = self.cap.read()
        self.height, self.width = frame.shape[:2]
        self.x_center = self.width // 2
        self.max_size = max(self.height, self.width)
        self.max_gap = int(self.width * 0.1)
        ret, jpeg = cv2.imencode('.jpg', frame)
        self.framedata = jpeg.tobytes()
        self.tennisLowDist = np.array([24, 99, 54])
        self.tennisHighDist = np.array([100, 255, 212])
        self.rectKernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        self.templates = []
        for i in range(1, 10):
            template = cv2.imread(("pycode/numbers/"+ str(i) + ".jpg"),cv2.IMREAD_GRAYSCALE)
            template = cv2.threshold(template , 60, 255, cv2.THRESH_BINARY_INV)[1]
            template = cv2.resize(template, (32,48))
            self.templates.append(template)
        self.kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))

        pass
    def get_sum (self, img):
        s = 0
        height, width = img.shape[:2]
        for y in range(height):
            for x in range(width):
                pixel_sum = int(img[y, x])
                s += pixel_sum

        return s

    def match_num(self, img):
        img = cv2.resize(img, (32,48))
        small = 1
        cha = self.get_sum((cv2.absdiff(self.templates[0],img)))
        for i in range(1,9):
            imgSub = cv2.absdiff(self.templates[i], img)
            rate = self.get_sum(imgSub)
            if rate < cha:
                cha = rate
                small = i+1
        return small
    def changeMode(self, mode):
        self.mode = mode
        ''''''
    def start(self) -> None:
        """启动视觉识别"""
        self.isable = True
        def thread_cam():
            while self.isable:
                ret, frame = self.cap.read()
                if not ret:
                    break
                if self._mode == 0:
                    r_list = []
                    huatu = frame.copy()
                    huatu[:, :, 1] = 0
                    huatu[:, :, 2] = 0
                    huatu[:, :, 0] = 0
                    img = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                    img = cv2.GaussianBlur(img, (3, 3), 0)
                    mask = cv2.inRange(img, self.tennisLowDist, self.tennisHighDist)
                    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, self.kernel)
                    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, self.kernel)
                    _, contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                    if len(contours) != 0:
                        for i in range(len(contours)):
                            cv2.drawContours(huatu, contours, i, (255, 255, 255), 1) 
                        gray1 = cv2.cvtColor(huatu, cv2.COLOR_BGR2GRAY)
                        circles = cv2.HoughCircles(gray1, cv2.HOUGH_GRADIENT, 1, 100, param1=50, param2=15, minRadius=1,maxRadius=200)
                    else:
                        circles = None
                    if circles is not None:
                        self.noBall = False
                        circles = np.round(circles[0, :]).astype("int")
                        drawn_circles = []
                        for (x, y, r) in circles:
                            overlap = False
                            for (dx, dy, dr) in drawn_circles:
                                distance = np.sqrt((x - dx) ** 2 + (y - dy) ** 2)
                                if distance < r + dr: 
                                    overlap = True
                                    break
                            if not overlap:
                                r_list.append(x)
                                r_list.append(self.max_size + r)
                                cv2.circle(frame, (x, y), 1, (0, 0, 255), 2)
                                cv2.circle(frame, (x, y), r, (0, 255, 0), 2)
                                drawn_circles.append((x, y, r))
                        if not r_list == []: 
                            max_r_x = r_list[r_list.index(max(r_list))-1]
                            self.max_r_gap = max_r_x - self.x_center
                        else:
                            self.noBall = True
                            self.max_r_gap = None
                            self.driver.setVel(0.15)
                            self.driver.turn_clockwise()
                    else:
                        self.max_r_gap = None
                        self.noBall = True
                        self.driver.setVel(0.15)
                        self.driver.turn_clockwise()
                    
                    if self.isai:
                        if not self.max_r_gap is None:
                            '''检测得到最大圆心距'''
                            if abs(self.max_r_gap) > self.max_gap:
                                '''球在目标范围外'''
                                self.driver.setVel(0.08)
                                a = (abs(self.max_r_gap) / (self.width /2))
                                b = ((max(r_list) - self.max_size) / (self.width * 0.15))
                                time = 0.1 * a
                                if time < 0:
                                    time = 0
                                if time > 0.1:
                                    time = 0.1
                                if self.max_r_gap > 0:
                                    '''球在右侧'''
                                    self.driver.turn_clockwise(time)
                                elif self.max_r_gap < 0:
                                    '''球在左侧'''
                                    self.driver.turn_counterclockwise(time)
                                else:
                                    '''球在中间'''
                                    self.driver.move_forward()
                            else:
                                """球在目标范围内"""
                                self.driver.setVel(0.15)
                                self.driver.move_forward()
                        else:
                            '''检测不到最大圆心距'''
                            self.driver.setVel(0.15)
                            self.driver.stop()

                    ret, jpeg = cv2.imencode('.jpg', frame)
                    self.framedata =  jpeg.tobytes()
                elif self._mode == 1:
                    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    frame_ths = cv2.threshold(frame_gray, 50, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
                    img_closed = cv2.morphologyEx(frame_ths, cv2.MORPH_CLOSE, self.rectKernel)
                    temp = cv2.Canny(img_closed, 100, 200)
                    _, contours, hierarchy = cv2.findContours(temp, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
                    recognized_numbers = []
                    min_number = None
                    min_x = None
                    min_y = None
                    for index, c in enumerate(contours):
                        area = cv2.contourArea(c)
                        x, y, w, h = cv2.boundingRect(c)
                        if area > 1000 and w/h> 0.6 and w/h < 0.8:
                            img = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                            center_x = x + w // 2
                            center_y = y + h // 2
                            roi = img_closed[y:y+h, x:x+w]
                            small = self.match_num(roi)
                            cv2.putText(frame, str(small), (x + w - 26, y + 26), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)
                            recognized_numbers.append((small, center_x, center_y))
                    if recognized_numbers:
                        min_number = min(recognized_numbers, key=lambda x: x[0])
                        min_x, min_y = min_number[1], min_number[2]
                    if min_x is not None and min_y is not None:
                        cv2.putText(frame, "min", (min_x - 2, min_y - 2), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)
                    ret, jpeg = cv2.imencode('.jpg', frame)
                    self.framedata =  jpeg.tobytes()   
                elif self._mode == 2:
                    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
                    color_ranges = {
                            'red': ([0, 90, 45], [20, 180, 130]),
                            'yellow': ([0, 150, 50], [30, 200, 120]),
                            'blue': ([50, 100, 40], [130, 220, 180]),
                            'purple': ([110, 130, 0], [150, 200, 70])
                        }
                    colors = self.target
                    color_range = color_ranges[colors]
                    low = np.array(color_range[0])
                    high = np.array(color_range[1])
                    img = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                    img = cv2.GaussianBlur(img, (3, 3), 0)
                    mask = cv2.inRange(img, low, high)
                    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
                    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
                    _, contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                    max_area = 0
                    max_contour = None
                    for contour in contours:
                        area = cv2.contourArea(contour)
                        if area > 50:
                            if area > max_area:
                                max_area = area
                                max_contour = contour
                    if max_contour is not None:
                        x, y, w, h = cv2.boundingRect(max_contour)
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        cv2.putText(frame, colors, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                        center_x = x + w // 2
                        center_y = y + h // 2
                    ret, jpeg = cv2.imencode('.jpg', frame)
                    self.framedata =  jpeg.tobytes()   
        thread_func = threading.Thread(target=thread_cam)
        thread_func.start()



    def get_frame(self):
        return self.framedata

    def close(self) -> None:
        """关闭视觉识别"""
        self.isable = False
