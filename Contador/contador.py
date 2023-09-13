
import RPi.GPIO as GPIO
import time 

suma = 0
dectobin = 128
arrayPines = [22,18,16,15,13,12,11,7]
arrayPines.reverse()
GPIO.setmode(GPIO.BOARD)

for i in arrayPines:
	GPIO.setup(i, GPIO.OUT)
	GPIO.output(i, GPIO.LOW)
	
for i in range(0,256):
	
	suma = 0
	dectobin = 128
	print(i)
	
	for y in arrayPines:
		GPIO.output(y, GPIO.LOW)

	if(i!=0):
		for y in arrayPines:
			
			if dectobin > i or suma == i or (suma+dectobin) > i:
				GPIO.output(y, GPIO.LOW)
			else:
				suma += dectobin
				GPIO.output(y, GPIO.HIGH)
			dectobin /= 2
			
	time.sleep(0.8)
	
	
time.sleep(2)
GPIO.cleanup()

