import cv2
import numpy as np

cap = cv2.VideoCapture(0)
ret, capture = cap.read()

lowerOrangeLA = np.array([0, 68, 255])
upperOrangeLA = np.array([180, 255, 255])

lowerLaranjaLD = np.array([0, 109, 36])
upperLaranjaLD = np.array([180, 255, 255])

while True:
    print("foi")
    ret, capture = cap.read()
    hsv = cv2.cvtColor(capture, cv2.COLOR_BGR2HSV)
    laranja  = cv2.inRange(hsv, lowerOrangeLA, upperOrangeLA)
    blur = cv2.GaussianBlur(laranja,(7, 7), 0)
    mask = cv2.Canny(blur, 50, 150)
    contorno, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
             
    for contours in contorno:
        areaContorno = cv2.contourArea(contours)
        
        if areaContorno > 1200:
            x, y, width, height = cv2.boundingRect(contours)
            cv2.rectangle(capture, (x,y), (x + width, y + height), (0, 0, 255), 3)
          
    key = cv2.waitKey(1)
    if key == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
