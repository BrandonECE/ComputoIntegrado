import RPi.GPIO as GPIO
import serial
import threading
import time 

GPIO.setmode(GPIO.BCM)

puertoSerial = serial.Serial('/dev/ttyUSB0', 9600)
leds = [26, 13, 6, 12, 19]
buzzer = 4


GPIO.setup(buzzer, GPIO.OUT)
GPIO.output(buzzer, GPIO.LOW)

for led in leds:
	GPIO.setup(led, GPIO.OUT)
	GPIO.output(led, GPIO.LOW)
 
def apagarLeds():
	for led in leds:
		GPIO.output(led, GPIO.LOW)
	
def hilo1():#SECUENCIA1
	global parpadeo
	global hiloActual
	while True:
		hiloActual = threading.currentThread()
		
		while hiloActual == thread1:#Ejecucion de secuencia1
			if(parpadeo == False):
				break
			apagarLeds()
			time.sleep(0.1)
			for led in leds:
				GPIO.output(led, GPIO.HIGH)
				time.sleep(0.1)
				
		apagarLeds()
		time.sleep(1.5)
		
		while hiloActual == thread2:#Tiempo de espera
			time.sleep(1)
			print("HILO1 ESPERA")
	print("Terminando1")	
		
def hilo2():#SECUENCIA2
	global parpadeo
	global hiloActual
	while True:
		print("2HILO")
		hiloActual = threading.currentThread()
		
		while hiloActual == thread2:#Ejecucion de secuencia2
			if(parpadeo == False):
				break
			apagarLeds()
			time.sleep(0.1)
			for led in leds:
				GPIO.output(led, GPIO.HIGH)
			time.sleep(0.1)
			
		apagarLeds()
		time.sleep(1.5)
		while hiloActual == thread1:#Tiempo de espera
			time.sleep(1)
			print("HILO2 ESPERA")	
	print("Terminando2")		


def hilo3():#BUZZER
	global parpadeo
	global switchbuzzer
	while True:
		if (switchbuzzer == True):
			GPIO.output(buzzer, GPIO.HIGH)
			print("SONADO BUZZER")
		elif (switchbuzzer == False):
			print("BUZZER APAGADO")
			parpadeo = False
			GPIO.output(buzzer, GPIO.LOW)

thread1 = threading.Thread(target=hilo1, daemon=True)
thread2 = threading.Thread(target=hilo2, daemon=True)
thread3 = threading.Thread(target=hilo3, daemon=True)
hiloActual = None
secuencia = True #True es secuencia 1 | False es secuencia 2
turno = True
once1 = False
once2 = False
once3 = False
switchbuzzer = False
parpadeo = False

#time.sleep(10)

while True:
	
	valueserial = str(puertoSerial.readline().decode('utf-8').strip())
	
	if(valueserial == "MOVIMIENTO"):#BUZZER
		print("Movimiento")
		switchbuzzer = True
		parpadeo = True
		if once3 == False:
			thread3.start()
			once3 = not once3
		
	if(valueserial == "PRESIONADO"):#BOTON PARA LEDS
		print("Presionando")
		secuencia = not secuencia
		
	if(valueserial == "DOSPRESIONADO"):#BOTON PARA APAGAR EL BUZZER
		print("DOSPresionando")
		switchbuzzer = False
	
	if(parpadeo == True):
		if secuencia == True and turno == True:#SECUENCIA1
			if(hiloActual != thread1):
				hiloActual = None
				if(once1 == False):
					thread1.start()
					once1 = not once1
			turno = False
			
		if secuencia == False and turno == False:#SECUENCIA2
			if(hiloActual != thread2):
				hiloActual = None
				if(once2 == False):
					thread2.start()
					once2 = not once2
			turno = True
	elif(parpadeo == False):
		apagarLeds()
	

time.sleep(1);

for led in leds:
	GPIO.output(led, GPIO.LOW)


GPIO.cleanup()