import time
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(29, GPIO.OUT)
GPIO.setup(33, GPIO.OUT)

escEsq = GPIO.PWM(29, 50)
escDir = GPIO.PWM(33, 50)

escEsq.start(0)
escDir.start(0)

print("esc's iniciados")
time.sleep(2)

escEsq.ChangeDutyCycle(3)
escDir.ChangeDutyCycle(3)
time.sleep(1)


while True:
        escEsq.ChangeDutyCycle(6.6)
        escDir.ChangeDutyCycle(7)
