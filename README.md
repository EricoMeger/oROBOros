# oROBOros
<p align="justify"> 

Projeto de conclusão de curso para Técnico em Informática no IFPR.

O trabalho consistiu no desenvolvimento de um robô-tanque para participar em competições de robótica na modalidade Trekking.
Não foi possível concluí-lo em sua totalidade, tendo sido desenvolvido apenas os códigos de visão computacional para reconhecimento dos cones 
e o código de geolocalização.

Como "cérebro" do robô foi utilizado um Raspberry Pi 4, de 4 gb. Para alimentar ele foi utilizado um powerbank genérico de 2000mAh, e uma webcam também 
genérica para a visão. Além disso, para movimentar os robôs foram utilizados ESC's SimonSeries 20A, motores de drone SunnySky X2212 e uma
bateria de lítio de 11.1v para alimentá-los. Foi utilizado também um magnetômetro hmc5883l. No quesito do GPS, houveram alguns problemas ao utilizar um módulo
específico para tal, portanto, foi utilizado o próprio GPS do celular por meio do app [GPSd Forwarder](https://f-droid.org/pt_BR/packages/io.github.tiagoshibata.gpsdclient/index.html)
O código para leitura de GPS, em teoria, apesar de ter sido feito com o próposito de ser utilizado por meio deste app, deve funcionar com módulos de GPS também,
bastando ter o [GPSd](https://gpsd.gitlab.io/gpsd/) instalado em seu sistema. 

**É possível ver os diagramas de montagem na pasta "Imagens".**

O tanque foi construído com base no modelo de [Andre Klaus](https://www.thingiverse.com/thing:2414983);

Para controle do magnetômetro foi utilizada a biblioteca [i2clibraries](https://github.com/ameer1234567890/i2clibraries), de criação de Barteled e Ameer, nossos agradecimentos à eles.

Além do uso do código de visão computacional tentamos o uso de uma rede neural para detecção de cones. Por conta das limitações do Raspberry, no entanto,
não foi possível usar ela. Caso seja de seu interesse, é possível utilizá-la junto do [yolov5](https://github.com/ultralytics/yolov5), com o arquivo treino3.pt

*python detect.py --source 0 --weights treino3.pt*

O dataset utilizado também foi feito por nós, e está disponível no [roboflow](https://app.roboflow.com/robotica-xftin/traffic-cones-4laxg/overview).
</p>
