
import RPi.GPIO as GPIO
import time 
GPIO.setmode(GPIO.BCM)

			 #a, b, c, d, e, f, g
#arrayPines = [7,11,12,16,15,40,38]
arrayPines = [4,17,18,23,22,21,20]
arrayLed = [26, 19, 6, 27, 10, 9, 5, 12, 16]

value = 0
pinPoten = 13
GPIO.setup(pinPoten, GPIO.IN)

configN = {
	0: [1,1,1,1,1,1,0],
	1: [0,1,1,0,0,0,0],
	2: [1,1,0,1,1,0,1],
	3: [1,1,1,1,0,0,1],
	4: [0,1,1,0,0,1,1],
	5: [1,0,1,1,0,1,1],
	6: [1,0,1,1,1,1,1],
	7: [1,1,1,0,0,0,0],
	8: [1,1,1,1,1,1,1],
	9: [1,1,1,1,0,1,1],
}

for i in arrayPines:	
	GPIO.setup(i, GPIO.OUT)
	GPIO.output(i, GPIO.HIGH)
	
for i in arrayLed:
	GPIO.setup(i, GPIO.OUT)
	GPIO.output(i, GPIO.LOW)


	
time.sleep(2)	

	
#FUNCION
def display(valor, configN, arrayPines):
	
	for clave, digit in configN.items():
			
		if(valor == clave):
			print("Display " + str(clave))
			for i, pin in zip(digit, arrayPines):
				if i == 0:
					GPIO.output(pin, GPIO.HIGH)
				else:
					GPIO.output(pin, GPIO.LOW)
	
	
					
display(value, configN, arrayPines)
time.sleep(3)		
while True:
	lectura = GPIO.input(13)
	if lectura == 1 and value < 9:
		value += 1
		GPIO.output(arrayLed[value-1], GPIO.HIGH)
		display(value, configN, arrayPines)
	if lectura == 0 and value > 0:
		value -= 1
		GPIO.output(arrayLed[value], GPIO.LOW)
		display(value, configN, arrayPines)		
		
	print("Potenciometro: " + str(lectura))
	time.sleep(1)

GPIO.cleanup()
