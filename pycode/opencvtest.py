import cv2
import requests
import numpy as np
from io import BytesIO
from PIL import Image

res = requests.get('http://192.168.43.220/cam.mjpeg', stream=True)
imageBytes = bytes()
for data in res.iter_content(chunk_size=300):
    # 输出data 查看每一张图片的开始与结尾，查找图片的头与尾截取jpg。并把剩余部分imageBytes做保存
    imageBytes += data
    a = imageBytes.find(b'\xff\xd8')
    b = imageBytes.find(b'\xff\xd9')
    if a != -1 and b != -1:
        print(1111)
        jpg = imageBytes[a:b+2]
        imageBytes = imageBytes[b+2:]

        bytes_stream = BytesIO(jpg)
        frame = Image.open(bytes_stream)
        frame = cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2BGR)
        frame = cv2.flip(frame,0)


        cv2.imshow('img', frame)
        


        
        if cv2.waitKey(1) & 0XFF == ord('q'):
            break

cv2.destroyAllWindows()
















# # import urllib
# # import urllib.request
# import requests
# import cv2
# import numpy as np

# url="http://192.168.43.220/cam.mjpeg"
# #改成自己的ip地址+/cam-hi.jpg
# cap = cv2.VideoCapture(url)
# while True:
    
#     # imgResp=requests.get(url)
#     # imgNp=np.array(bytearray(imgResp.content),dtype=np.uint8)
#     # img=cv2.imdecode(imgNp,-1)
#     ret, frame = cap.read()

#         # 如果帧读取失败，则退出循环
#     if not ret:
#         break

#     # all the opencv processing is done here
#     cv2.imshow('test',frame)
#     if ord('q')==cv2.waitKey(50) & 0xFF:
#         exit(0)
