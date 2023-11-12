import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)

    
valve1 = 12
valve2 = 1
valve3 = 7
valve4 = 8
valve5 = 25
valve6 = 24
valve7 = 23
valve8 = 18




# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(valve1, GPIO.OUT)
GPIO.setup(valve2, GPIO.OUT)
GPIO.setup(valve3, GPIO.OUT)
GPIO.setup(valve4, GPIO.OUT)
GPIO.setup(valve5, GPIO.OUT)
GPIO.setup(valve6, GPIO.OUT)
GPIO.setup(valve7, GPIO.OUT)
GPIO.setup(valve8, GPIO.OUT)

GPIO.output(valve1, False)
GPIO.output(valve2, False)
GPIO.output(valve3, False)
GPIO.output(valve4, False)
GPIO.output(valve5, False)
GPIO.output(valve6, False)
GPIO.output(valve7, False)
GPIO.output(valve8, False)

def relay_off(pin):
    GPIO.output(pin, False)
    
def relay_on(pin):
    GPIO.output(pin, True)
       

# relay_off(valve2)
# relay_off(valve4)
# relay_off(valve1)
# relay_off(valve6)
# relay_off(valve5)
# relay_off(valve3)
# relay_off(valve7)
# relay_off(valve8)

    
state = int(input('enter 1 '))


if (state==1):
    try:
            relay_on(valve1)
            time.sleep(.5)
            relay_on(valve2)
            time.sleep(.5)
            relay_on(valve3)
            time.sleep(.5)
            relay_on(valve4)
            time.sleep(.5)
            relay_on(valve5)
            time.sleep(.5)
            relay_on(valve6)
            time.sleep(.5)
            relay_on(valve7)
            time.sleep(.5)
            relay_on(valve8)
            time.sleep(10)
            relay_off(valve2)
            relay_off(valve4)
            relay_off(valve1)
            relay_off(valve6)
            relay_off(valve5)
            relay_off(valve3)
            relay_off(valve7)
            relay_off(valve8)
         
        
    except KeyboardInterrupt:
         relay_off(valve2)
         relay_off(valve4)
         relay_off(valve1)
         relay_off(valve6)
         relay_off(valve5)
         relay_off(valve3)
         relay_off(valve7)
         relay_off(valve8)

        
            

    
        
    

