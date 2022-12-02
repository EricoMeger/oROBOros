import cv2
import numpy as np
import time
import RPi.GPIO as GPIO
import threading

def segueCone():
    cap = cv2.VideoCapture(0)
    ret, capture = cap.read()

    width = int(cap.get(3))
    height =(cap.get(4))

    minimum_area = 250
    maximum_area = 100000

    lowerOrangeLA = np.array([0, 68, 255])
    upperOrangeLA = np.array([180, 255, 255])

    #lower_orange = np.array([0, 150, 194])
    #upper_orange = np.array([180, 255, 255])
    
    lowerLaranjaLD = np.array([0, 109, 36])
    upperLaranjaLD = np.array([180, 255, 255])

    centerImageX = width / 2
    centerImageY = height / 2

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)

    GPIO.setup(29, GPIO.OUT)
    GPIO.setup(33, GPIO.OUT)

    escEsq = GPIO.PWM(29, 50)
    escDir = GPIO.PWM(33, 50)

    escEsq.start(0)
    escDir.start(0)


    while True:
        ret, capture = cap.read()
            
        hsv = cv2.cvtColor(capture, cv2.COLOR_BGR2HSV)
         
        laranja  = cv2.inRange(hsv, lowerLaranjaLD, upperLaranjaLD)

        blur = cv2.GaussianBlur(laranja,(7, 7), 0)

        mask = cv2.Canny(blur, 50, 150)
        
        contorno, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        areaObject = 0
        objectX = 0
        objectY = 0
                
        for contours in contorno:
            areaContorno = cv2.contourArea(contours)
            
            if areaContorno > 1200:
                x, y, width, height = cv2.boundingRect(contours)
                cv2.rectangle(capture, (x,y), (x + width, y + height), (0, 0, 255), 3)
                areaFound = width * height
                centerX = x + (width / 2)
                centerY = y + (height / 2)
           
                if areaObject < areaFound:
                    areaObject = areaFound
                    objectX = centerX
                    objectY = centerY
            
                if areaObject > 0:
                    coneLocation = [areaObject, objectX, objectY]
                
                else:
                    coneLocation = None
                    
                if coneLocation:
                    
                    if (coneLocation[0] > minimum_area) and (coneLocation[0] < maximum_area):
                        
                        if coneLocation[1] > (centerImageX + (width/3)):
                            escDir.ChangeDutyCycle(6.6)
                            escEsq.ChangeDutyCycle(6.2)
                            print("Indo para direita")
                        
                        elif coneLocation[1] < (centerImageX - (width/3)):
                            escDir.ChangeDutyCycle(6.4)
                            escEsq.ChangeDutyCycle(7.2)
                            print("Indo para esquerda")
                        
                        else:
                            escDir.ChangeDutyCycle(6.4)
                            escEsq.ChangeDutyCycle(7)
                            print("Indo para frente")
                    
                    elif (coneLocation[0] < minimum_area):
                        escEsq.ChangeDutyCycle(7)
                        escDir.ChangeDutyCycle(0)
                        print("procurando cone")
                    
                    else:
                        escEsq.ChangeDutyCycle(0)
                        escDir.ChangeDutyCycle(0)
                    
                    
                    
        
        
        
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
        

    cap.release()
    cv2.destroyAllWindows()

segueCone()
