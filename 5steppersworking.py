
from time import sleep
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
#
PUL1 = 16   
DIR1 = 20  
ENA1 = 21
PUL2 = 13   
DIR2 = 19  
ENA2 = 26
PUL3 = 00   
DIR3 = 5  
ENA3 = 6
PUL4 = 10   
DIR4 = 9  
ENA4 = 11
PUL5 = 17   
DIR5 = 27  
ENA5 = 22

GPIO.setmode(GPIO.BCM)

GPIO.setup(PUL1, GPIO.OUT)
GPIO.setup(DIR1, GPIO.OUT)
GPIO.setup(ENA1, GPIO.OUT)
GPIO.setup(PUL2, GPIO.OUT)
GPIO.setup(DIR2, GPIO.OUT)
GPIO.setup(ENA2, GPIO.OUT)
GPIO.setup(PUL3, GPIO.OUT)
GPIO.setup(DIR3, GPIO.OUT)
GPIO.setup(ENA3, GPIO.OUT)
GPIO.setup(PUL4, GPIO.OUT)
GPIO.setup(DIR4, GPIO.OUT)
GPIO.setup(ENA4, GPIO.OUT)
GPIO.setup(PUL5, GPIO.OUT)
GPIO.setup(DIR5, GPIO.OUT)
GPIO.setup(ENA5, GPIO.OUT)


print('Initialization Completed')

# Could have usesd only one DURATION constant but chose two. This gives play options.
durationFwd = 5000 # This is the duration of the motor spinning. used for forward direction
durationBwd = 600 # This is the duration of the motor spinning. used for reverse direction
#set durationBWD to 900 for 1mL using small pump
#set durationBWD to 7750 for 10mL using small pump
#set durationBWD to 275 for 1mL using large pump
#set durationBWD to  2200 for 10mL using small pump

delay = 0.001 # This is actualy a delay between PUL pulses - effectively sets the mtor rotation speed.


cycles = 1 # This is the number of cycles to be run once program is started.
cyclecount = 0 # This is the iteration of cycles to be run once program is started.


def reverse():
    GPIO.output(ENA1, GPIO.HIGH)
    GPIO.output(DIR1, GPIO.HIGH)
    GPIO.output(ENA2, GPIO.HIGH)
    GPIO.output(DIR2, GPIO.HIGH)
    GPIO.output(ENA3, GPIO.HIGH)
    GPIO.output(DIR3, GPIO.HIGH)
    GPIO.output(ENA4, GPIO.HIGH)
    GPIO.output(DIR4, GPIO.HIGH)
    GPIO.output(ENA5, GPIO.HIGH)
    GPIO.output(DIR5, GPIO.HIGH)
    for y in range(durationBwd):
        GPIO.output(PUL1, GPIO.HIGH)
        sleep(delay)
        GPIO.output(PUL1, GPIO.LOW)
        sleep(delay)
        GPIO.output(PUL2, GPIO.HIGH)
        sleep(delay)
        GPIO.output(PUL2, GPIO.LOW)
        sleep(delay)
        GPIO.output(PUL3, GPIO.HIGH)
        sleep(delay)
        GPIO.output(PUL3, GPIO.LOW)
        sleep(delay)
        GPIO.output(PUL4, GPIO.HIGH)
        sleep(delay)
        GPIO.output(PUL4, GPIO.LOW)
        sleep(delay)
        GPIO.output(PUL5, GPIO.HIGH)
        sleep(delay)
        GPIO.output(PUL5, GPIO.LOW)
        sleep(delay)
    GPIO.output(ENA1, GPIO.LOW)
    GPIO.output(ENA2, GPIO.LOW)
    GPIO.output(ENA3, GPIO.LOW)
    GPIO.output(ENA4, GPIO.LOW)
    GPIO.output(ENA5, GPIO.LOW)
    return



while cyclecount < cycles:
    
    reverse()
    
    cyclecount = (cyclecount + 1)
    
GPIO.cleanup()

