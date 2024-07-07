import cv2
import numpy as np

def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        selected_region = hsv[y-10:y+10, x-10:x+10]  # 以点击位置为中心，选择一个10x10的区域
        min_hue = np.min(selected_region[:, :, 0])
        max_hue = np.max(selected_region[:, :, 0])
        min_saturation = np.min(selected_region[:, :, 1])
        max_saturation = np.max(selected_region[:, :, 1])
        min_value = np.min(selected_region[:, :, 2])
        max_value = np.max(selected_region[:, :, 2])
        print("HSV range in selected region:")
        print("Hue: {} - {}".format(min_hue, max_hue))
        print("Saturation: {} - {}".format(min_saturation, max_saturation))
        print("Value: {} - {}".format(min_value, max_value))

img = cv2.imread('image.jpg')

cv2.imshow('Image', img)
cv2.setMouseCallback('Image', click_event)

cv2.waitKey(0)
cv2.destroyAllWindows()