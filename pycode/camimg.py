import urllib.request
import cv2
import numpy as np

url='http://192.168.43.220/cam-hi.jpg'
a = 0
while True:
    imgResp=urllib.request.urlopen(url)
    imgNp=np.array(bytearray(imgResp.read()),dtype=np.uint8)
    img=cv2.imdecode(imgNp,-1)
    img = cv2.flip(img,0)
    # all the opencv processing is done here
    cv2.imshow('test',img)
    # a = a + 1
    # print(a)
    if ord('q')==cv2.waitKey(50):
        exit(0)
