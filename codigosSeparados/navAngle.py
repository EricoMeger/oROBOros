from gps import *
import time
import RPi.GPIO as GPIO
from i2clibraries import i2c_hmc5883l
from math import atan2, pi
from geopy.distance import geodesic
gpsd = gps(mode=WATCH_ENABLE)

def iniciaMotor():

    global escEsq
    global escDir

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(29, GPIO.OUT)
    GPIO.setup(33, GPIO.OUT)

    escEsq = GPIO.PWM(29, 50)
    escDir = GPIO.PWM(33, 50)
    escEsq.start(0)
    escDir.start(0)

    time.sleep(2)

    escEsq.ChangeDutyCycle(3)
    escDir.ChangeDutyCycle(3)

    time.sleep(1)

def getPosicao(gps):

    global latAtual
    global lonAtual

    px = gpsd.next()

    if px['class'] == 'TPV':
        latAtual = getattr(px, 'lat', "unknown")
        lonAtual = getattr(px, 'lon', "unknown")
        print("latitude: " + str(latAtual) + "longitude: " + str(lonAtual))


def getWaypoints():

    global latDestino
    global lonDestino
    global i

    latDestino = [1,2,3]
    lonDestino = [1,2,3]

    for i in range(3):
        latDestino[i] = float(input("latitude: "))
        lonDestino[i] = float(input("longitude: "))

    i = 0


def calculaDistancia():

    #Para definir que o robô chegou na coordenada, é necessário comparar a lat e lon atual com a lat e lon destino,
    #sendo necessário também uma taxa de aceitação, considerando o erro do GPS.

    global distancia
    global distanciaMax
    global distanciaMin

    matrixCoord_Atual = [latAtual, lonAtual]
    matrixCoord_Dest = [latDestino[i], lonDestino[i]]

    distancia = geodesic(matrixCoord_Atual, matrixCoord_Dest).m
    print(distancia)
    distanciaMin = distancia - 0,5
    distanciaMax = distancia + 0,5


def chamaBussola():

    global bussola
    
    bussola = i2c_hmc5883l.i2c_hmc5883l(1)
    bussola.setContinuousMode()
    bussola.setDeclination(x, x)

def calculaAngulo():

    global direcaoGraus

    deltaLat = latDestino[i] - latAtual
    deltaLon = lonDestino[i] - lonAtual
   
    direcaoGraus = atan2(deltaLon, deltaLat)/pi*180
    
    if direcaoGraus < 0:
        direcaoGraus = 360 + direcaoGraus

x = 0

while(x != 20):
    getPosicao(gps)
    x += 1
    print("ta indo")


naoChegou = True
procurandoAngulo = True
achouAngulo = False

iniciaMotor()
getWaypoints()
chamaBussola()
calculaAngulo()

minAngle = direcaoGraus - 3
maxAngle = direcaoGraus + 3

while naoChegou:

    calculaDistancia()

    if (0.5 <= distancia <= 1):
        naoChegou = False

    else:
        
        while procurandoAngulo:
            direcao = bussola.getHeading()
            anguloAtual = direcao[0]

            if anguloAtual > direcaoGraus:
                print("virando para a direita")
                escEsq.ChangeDutyCycle(6.4)
                escDir.ChangeDutyCycle(0)
                if (minAngle <= anguloAtual <= maxAngle):
                    procurandoAngulo = False
                    achouAngulo = True
                    escEsq.ChangeDutyCycle(0)
                    escDir.ChangeDutyCycle(0)

            if anguloAtual < direcaoGraus:
                print("virando para esquerda")
                escEsq.ChangeDutyCycle(0)
                escDir.ChangeDutyCycle(7.6)
                if (minAngle <= anguloAtual <= maxAngle):
                    procurandoAngulo = False
                    achouAngulo = True
                    escEsq.ChangeDutyCycle(0)
                    escDir.ChangeDutyCycle(0)

        while achouAngulo:
            print("indo em direção ao angulo")
            escEsq.ChangeDutyCycle(6.4)
            escDir.ChangeDutyCycle(7)

i+= 1

if (i == 2):
    print("trajeto concluído")

else:
    naoChegou = True
    procurandoAngulo = True
    achouAngulo = False

