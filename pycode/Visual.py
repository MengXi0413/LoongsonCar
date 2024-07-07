import cv2
import numpy as np
import urllib
import urllib.request
import threading
import cv2
import requests
import numpy as np
from io import BytesIO
from PIL import Image

# 网球的hsv空间阈值
tennisLowDist = np.array([23, 60, 58])
tennisHighDist = np.array([60, 255, 219])

# 闭运算算子
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
radius = 0

class VISUAL():
    def __init__(self, driver) -> None:
        self.driver = driver
        self.isStart = False
        self.max_r_gap = -1
        self.max_size = -1
        self.max_gap = -1
        self.isable = True
        imgResp=urllib.request.urlopen("http://192.168.43.220/cam-hi.jpg")
        imgNp=np.array(bytearray(imgResp.read()),dtype=np.uint8)
        frame=cv2.imdecode(imgNp,-1)
        height, width = frame.shape[:2]
        self.max_size = max(height, width)
        self.max_gap = int(width * 0.1)
        pass
    
    def start(self) -> None:
        self.isable = True
        def thread_cam():
            while self.isable:
                imgResp=urllib.request.urlopen("http://192.168.43.220/cam-hi.jpg")
                imgNp=np.array(bytearray(imgResp.read()),dtype=np.uint8)
                frame=cv2.imdecode(imgNp,-1)
                frame = cv2.flip(frame,-1)
                # 得到中线位置
                height, width = frame.shape[:2]
                x_center = width // 2
                y_center = height // 2
                r_list = []
                

                # 得到全黑图
                huatu = frame.copy()
                huatu[:, :, 1] = 0
                huatu[:, :, 2] = 0
                huatu[:, :, 0] = 0

                # 转换为hsv
                img = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

                # 高斯模糊
                img = cv2.GaussianBlur(img, (3, 3), 0)

                # 通过hsv阈值得到物体掩码
                mask = cv2.inRange(img, tennisLowDist, tennisHighDist)

                # 形态学操作，闭运算消除孔洞
                mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
                # mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
                # mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
                mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

                # cv2.imshow("hsv", mask)

                # 寻找轮廓
                try:
                    _, contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                except:
                    contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                if len(contours) != 0:
                    for i in range(len(contours)):
                        cv2.drawContours(huatu, contours, i, (255, 255, 255), 1)  # 画出边缘
                    gray1 = cv2.cvtColor(huatu, cv2.COLOR_BGR2GRAY)
                    circles = cv2.HoughCircles(gray1, cv2.HOUGH_GRADIENT, 1, 100, param1=50, param2=20, minRadius=1,maxRadius=200)
                else:
                    circles = None

                if circles is not None:
                    # 将检测到的圆的坐标和半径转换为整数
                    circles = np.round(circles[0, :]).astype("int")
                    
                    min_r = 10
                    # max_r = 100
                    drawn_circles = []
                    # 遍历每个检测到的圆
                    for (x, y, r) in circles:
                        if min_r <= r:
                            overlap = False
                            for (dx, dy, dr) in drawn_circles:
                                distance = np.sqrt((x - dx) ** 2 + (y - dy) ** 2)
                                if distance < r + dr:  # 检查是否有重叠
                                    overlap = True
                                    break
                            if not overlap:
                                r_list.append(x)
                                r_list.append(self.max_size + r)
                            # 绘制圆心
                                cv2.circle(frame, (x, y), 1, (0, 0, 255), 2)
                            # 绘制圆的边界
                                cv2.circle(frame, (x, y), r, (0, 255, 0), 2)
                                drawn_circles.append((x, y, r))
                    if not r_list == []: 
                        max_r_x = r_list[r_list.index(max(r_list))-1]
                        self.max_r_gap = max_r_x - x_center
                        # print(abs(self.max_r_gap),"------",self.max_gap)
                    else:
                        self.max_r_gap = None
                else:
                    self.max_r_gap = None
                    self.driver.stop()
                if self.max_r_gap is None:
                    continue
                if abs(self.max_r_gap) > self.max_gap:
                    # driver1.stop()
                    print(f"相差{self.max_r_gap}")
                    if self.max_r_gap < 0:
                        print("负数")
                        self.driver.turn_counterclockwise()
                    elif self.max_r_gap == 0:
                        self.driver.move_forward()
                    else:
                        print("正数")
                        self.driver.turn_clockwise()
                else:
                    self.driver.move_forward()
                    # print(self.max_r_gap,"=======",x_center,"=======",abs(self.max_r_gap) < self.max_gap)
                    # print(True if abs(self.max_r_gap) < self.max_gap else False)
                # 绘制中线
                # cv2.line(frame, (x_center, 0), (x_center, height), (0, 0, 255), 1)
                # cv2.line(frame, (0, y_center), (width, y_center), (0, 0, 255), 1)

                # 显示图像
                # cv2.imshow("Tennis Ball Detection norm", frame)
                # cv2.imwrite("./consolesite/static/image.jpg",frame)
                # if cv2.waitKey(50) & 0xFF == ord('q'):
                #     break

                # if cv2.waitKey(50) & 0xFF == ord('s'):
                #     cv2.imwrite("./image.jpg",frame)
                # # 按下 'q' 键退出循环
                # elif cv2.waitKey(50) & 0xFF == ord('q'):
                #     break
            # cv2.destroyAllWindows()
        thread_func = threading.Thread(target=thread_cam)
        thread_func.start()
        pass

    def close(self) -> None:
        self.isable = False
        pass