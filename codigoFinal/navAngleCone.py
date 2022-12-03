from gps import *
import time
import RPi.GPIO as GPIO
import cv2
import numpy as np
from i2clibraries import i2c_hmc5883l
from math import atan2, pi
import cv2
import numpy as np


gpsd = gps(mode=WATCH_ENABLE)

def iniciaMotor():

    global escEsq
    global escDir

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
  
    #Define as portas onde o motor está conectado
    GPIO.setup(29, GPIO.OUT)
    GPIO.setup(33, GPIO.OUT)
    
    #Passa para as portas um valor PWM para iniciar os ESC's
    escEsq = GPIO.PWM(29, 50)
    escDir = GPIO.PWM(33, 50)
    escEsq.start(0)
    escDir.start(0)

    time.sleep(2)

def getPosicao(gps):

    global latAtual
    global lonAtual

    #O gpsd mostra as informações sendo recebidas pelo GPS em formato de lista, para que seja possível retirar informações dele é criada a varíavel px, 
    #que serve para passar para a próxima linha.
    px = gpsd.next()

    #Faz-se uma checagem se o gpsd retornou a classe 'TPV', significando que o GPS conseguiu um fix, ou seja, conseguiu fixar sua localização com três 
    #satélites e portanto está pronto para repassar as informações recebidas.
    if px['class'] == 'TPV':
        #procura-se na lista strings de latitude e longitude, e retira a informações que elas estão repassando.
        latAtual = getattr(px, 'lat', "unknown")
        lonAtual = getattr(px, 'lon', "unknown")
        print("latitude: " + str(latAtual) + "longitude: " + str(lonAtual))


def getWaypoints():

    global latDestino
    global lonDestino
    global i

    latDestino = [1,2,3]
    lonDestino = [1,2,3]
    
    #Recebe as coordenadas dos marcos para qual o robô deve ir, sendo elas inseridas pelo usuário por meio do terminal.
    for i in range(3):
        latDestino[i] = float(input("latitude: "))
        lonDestino[i] = float(input("longitude: "))

    i = 0

def chamaBussola():

    global bussola
    
    #Aqui se cria a instância do magnetômetro, definindo para ele sempre ficar ativo. Define-se também, no setDeclination a inclinação em graus e 
    #minutos da onde será executado o código, para que a bússola seja precisa. Será ocultado por motivos de segurança, mas você pode checar a inclinação 
    #do seu local  neste site: https://www.magnetic-declination.com/

    bussola = i2c_hmc5883l.i2c_hmc5883l(1)
    bussola.setContinuousMode()
    bussola.setDeclination(x,x)

def calculaAngulo():

    global direcaoGraus

    deltaLat = latDestino[i] - latAtual
    deltaLon = lonDestino[i] - lonAtual
   
    direcaoGraus = atan2(deltaLon, deltaLat)/pi*180
    
    if direcaoGraus < 0:
        direcaoGraus = 360 + direcaoGraus

def segueCone(capture):
    
    global mask
    global width
    global height
    global centerImageX
    global centerImageY
    global minimum_area
    global maximum_area

    cap = cv2.VideoCapture(0)
    ret, capture = cap.read()

    width = int(cap.get(3))
    height =(cap.get(4))

    minimum_area = 250
    maximum_area = 100000

    #Foram tiradas duas cores do laranja: uma onde a luz do ambiente estava acesa e a outra com ela apagada, representada pelo LA e LD respectivamente. 
    #No momento está sendo usado somente a LA, mas é possível juntar os 4 ranges em uma máscara só e usá-la.
    lowerOrangeLA = np.array([0, 68, 255])
    upperOrangeLA = np.array([180, 255, 255])

   #lowerLaranjaLD = np.array([0, 109, 36])
   #upperLaranjaLD = np.array([180, 255, 255])

    centerImageX = width / 2
    centerImageY = height / 2

    hsv = cv2.cvtColor(capture, cv2.COLORBGR2HSV)
    laranja = cv2.inRange(hsv, lowerLaranjaLA, upperLaranjaLA)
    blur = cv2.GaussianBlur(laranja, (7,7), 0)
    mask = cv2.Canny(blur, 50, 150)


x = 0

while(x != 20):
    getPosicao(gps)
    x += 1
    print("ta indo")


coneLonge = True
    x += 1
    print("ta indo")
    #Esse while é necessário para a ativação do GPS, onde serve como uma forma de aguardar o fix ao mesmo tempo que retira as informações dele para que 
    #possam ser checadas na tela.

coneLonge = True
procurandoAngulo = True
achouAngulo = False

iniciaMotor()
getWaypoints()
chamaBussola()
calculaAngulo()

# É definida uma aceitação de erro para que o robô encontre a coordenada da qual ele tem que ir, pensando tanto em uma possível demora para o robô parar, 
#assim como um possível delay no magnetometro.

minAngle = direcaoGraus - 3
maxAngle = direcaoGraus + 3


while i != 3:

    ret, capture = cap.read()
    areaObject = 0
    objectX = 0
    objectY = 0

    iniciaCamera(capture)

    for contours in contorno:
        #Necessário para desenhar um contorno em torno do cone, para que seja possível checar seu tamanho.
        areaContorno = cv2.contourArea(contours)

        if areaContorno > 1500:
            #Caso a area contornada seja maior que 1500px, pega os dados da onde está sendo feito o contorno, para que se possa descobrir a onde o 
            #cone está em relação ao robô, esquerda, direita ou meio.   
            x, y, width, height = cv2.boundingRect(contours)
            cv2.rectangle(capture, (x,y), (x + width, y + height), (0, 0, 255), 3)
            coneLonge = False

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

                if coneLocation[0] > minimum_area and coneLocation[0] < maximum_area:
                    if coneLocation[1] > (centerImageX + (width / 3)):
                        escDir.ChangeDutyCycle(6.6)
                        escEsq.ChangeDutyCycle(6.2)
                        print("Indo para a direita")

                    elif coneLocation[1] < (centerImageX + (width / 3)):
                        escDir.ChangeDutyCycle(6.4)
                        escEsq.ChangeDutyCycle(7.4)
                        print("Indo para a esquerda")
                    
                    else: 
                        escDir.ChangeDutyCycle(6.4)
                        escEsq.ChangeDutyCycle(7)
                        print("Seguindo em frente")
            
            #Quando o cone está colado na câmera, a área do contorno fica em torno de 4800 a 5200. Como se faz necessário que o robô pare antes, 
            #é definido um range menor.
            if areaContorno > 3800:
                print("Cone muito perto")
                escEsq.ChangeDutyCycle(0)
                escDir.ChangeDutyCycle(0)
                print("Retornando controle para o GPS")
                coneLonge = True
                i+= 1
                    
    while coneLonge:
        while procurandoAngulo:

            #Recebemos da bussola para onde o robô está indo, pegando o primeiro termo pois o magnetometro sempre retorna graus e minutos, 
            #mas aqui só importa os graus.
            direcao = bussola.getHeading()
            anguloAtual = direcao[0]
    
            if anguloAtual > direcaoGraus:
                print("virando para a direita")
                escEsq.ChangeDutyCycle(6.4)
                escDir.ChangeDutyCycle(0)
                #Não precisa que o angulo que o robô está agora seja exatamente o angulo que está a coordenada, portanto, colocamos-o dentro do range 
                #definido anteriormente.
                if (minAngle <= anguloAtual <= maxAngle):
                    procurandoAngulo = False
                    achouAngulo = True
                    escEsq.ChangeDutyCycle(0)
                    escDir.ChangeDutyCycle(0)
    
            if anguloAtual < direcaoGraus:
                print("virando para esquerda")
                escEsq.ChangeDutyCycle(0)
                escDir.ChangeDutyCycle(6.6)
                if (minAngle <= anguloAtual <= maxAngle):
                    procurandoAngulo = False
                    achouAngulo = True
                    escEsq.ChangeDutyCycle(0)
                    escDir.ChangeDutyCycle(0)
    
        while achouAngulo:
            #Quando ele entrar no range de acerto do ângulo, irá mandar o robô andar para frente. 
            print("indo em direção ao angulo")
            escEsq.ChangeDutyCycle(6.4)
            escDir.ChangeDutyCycle(7)
            #Percebe-se a diferença de velocidade entre os motores.
        


