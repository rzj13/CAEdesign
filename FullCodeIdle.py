import RPi.GPIO as GPIO
import time, sys
from time import sleep
import firebase_admin 
from firebase_admin import db 
from firebase_admin import credentials 
import time 
import json 
import requests

cred_object = firebase_admin.credentials.Certificate('C:\\Users\\ryanz\Desktop\\SD Proj\\AccountKey.json') # this is where you would add the credentials to access database
default_app = firebase_admin.initialize_app(cred_object, {
	'databaseURL':'https://senior-design-test-78c5a-default-rtdb.firebaseio.com/' })

def write_to_database(table, k, value):
	ref = db.reference(table) # establish what table you are looking for
	ref.child(k).push({'setting':value,'time':get_time()}) # start building a json object that you want to write

def read_from_database(path):
	ref = db.reference(path) # set the pathway for the object you are looking to query
	keys = ref.order_by_key().get().keys() #get the keys (timestamps) in descending order
	most_recent_timestamp = max(keys) # Get the most recent timestamp
	most_recent_value = ref.child(most_recent_timestamp).get() # get the value associated with the most recent timestamp
	return(most_recent_value)


def get_time():
	current_unix_time = int(time.time()) # get time in unix format
	return(current_unix_time)



def get_temperature():
    try:
        url = "http://10.0.0.183/api/values"  # Replace with your actual local API URL
        response = requests.get(url)
        response.raise_for_status()

        # Parse the JSON response
        data = json.loads(response.text)
        temperature = data['modules'][0]['Celsius']

        return temperature
        time.sleep(10)
    except Exception as e:
        print(f"Error: {e}")
        return None
    


def get_ph():
    try:
        url = "http://10.0.0.183/api/values"  # Replace with your actual local API URL
        response = requests.get(url)
        response.raise_for_status()

        # Parse the JSON response
        data = json.loads(response.text)
        ph = data['modules'][0]['Celsius']

        return ph
        time.sleep(10)
    except Exception as e:
        print(f"Error: {e}")
        return None
    

def get_ec():
    try:
        url = "http://10.0.0.183/api/values"  # Replace with your actual local API URL
        response = requests.get(url)
        response.raise_for_status()

        # Parse the JSON response
        data = json.loads(response.text)
        ec = data['modules'][0]['Celsius']

        return ec
        time.sleep(10)
    except Exception as e:
        print(f"Error: {e}")
        return None


#write_to_database("controls","floatsensor", "high")

#drain_status = read_from_database("controls/drain_valve")
#print("drain status is currently " + drain_status["setting"])



GPIO.setwarnings(False)
cyclecount1 = 0
cyclecount2 = 0
cyclecount3 = 0
global count
count1 = 0
count2 = 0
count3 = 0

stepper1 = False
stepper2 = False
stepper3 = False
stepper4 = False
stepper5 = False
    
valve1 = 12
valve2 = 1
valve3 = 7
valve4 = 8
valve5 = 25
valve6 = 24
valve7 = 23
valve8 = 18

ballvalve= 8
transferpump= 21
sensorlinepump =20
sprinklerpump = 13
flushpump = 12
floatRO = 2 #tbd, must be pullup
floatNR = 3 #tbd, must be pullup
flowsensor1 = 14 # tbd

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
GPIO.setup(floatRO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(floatNR, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(flowsensor1, GPIO.IN, pull_up_down = GPIO.PUD_UP)


GPIO.output(valve1, False)
GPIO.output(valve2, False)
GPIO.output(valve3, False)
GPIO.output(valve4, False)
GPIO.output(valve5, False)
GPIO.output(valve6, False)
GPIO.output(valve7, False)
GPIO.output(valve8, False)

# Could have used only one DURATION constant but chose two. This gives play options.
durationFwd = 5000 # This is the duration of the motor spinning. used for forward direction
durationBwd = 600 # This is the duration of the motor spinning. used for reverse direction
#set durationBWD to 900 for 1mL using small pump
#set durationBWD to 7750 for 10mL using small pump
#set durationBWD to 275 for 1mL using large pump
#set durationBWD to  2200 for 10mL using small pump
delay = 0.001 # This is actualy a delay between PUL pulses - effectively sets the mtor rotation speed.
cycles = 1 # This is the number of cycles to be run once program is started.


def countPulse(channel):
   global count
   start_counter = 1
   if start_counter == 1:
      count = count+1

GPIO.add_event_detect(flowsensor1, GPIO.FALLING, callback=countPulse)



def reverse(ENA,DIR,PUL):
    GPIO.output(ENA, GPIO.HIGH)
    GPIO.output(DIR, GPIO.HIGH)

    for y in range(durationBwd):
        GPIO.output(PUL, GPIO.HIGH)
        sleep(delay)
        GPIO.output(PUL, GPIO.LOW)
        sleep(delay)
        
    GPIO.output(ENA, GPIO.LOW)
    return


def countflow():
     while True:
        try:
            start_counter = 1
            time.sleep(1)
            start_counter = 0
            flow = (count / 7.5) # Pulse frequency (Hz) = 7.5Q, Q is flow rate in L/min.
            print("The flow is: %.3f Liter/min" % (flow))
            return flow
            count = 0
            time.sleep(1)
        except KeyboardInterrupt:
            print('\nkeyboard interrupt!')
            GPIO.cleanup()
            sys.exit()



def relay_off(pin):
    GPIO.output(pin, False)
    
def relay_on(pin):
    GPIO.output(pin, True)
       
def ROfloatcheck(floatRO):
    ROfloatstate = GPIO.input(floatRO)
    if (ROfloatstate == "high"):
        write_to_database("controls","ROfloatsensor", "high")
    else:
         write_to_database("controls","ROfloatsensor", "low")

    return ROfloatstate

def NRfloatcheck(floatNR):
    NRfloatstate = GPIO.input(floatNR)
    if (NRfloatstate == "high"):
        write_to_database("controls","NRfloatsensor", "high")
    else:
         write_to_database("controls","NRfloatsensor", "low")

    return NRfloatstate

def write_temperature_to_database(temperature):
    try:
        table = "temperature_data"  # Replace with the desired Firebase database table
        timestamp = int(time.time())  # Get the current UNIX timestamp
        ref = db.reference(table)

        # Create a JSON object to write to the database
        data = {
            'temperature': temperature,
            'time': timestamp
        }

        ref.push(data)  # Push the data to the database

        print(f"Temperature {temperature} °C written to the database at timestamp {timestamp}")
    except Exception as e:
        print(f"Error: {e}")


def write_ph_to_database(ph):
    try:
        table = "ph_data"  # Replace with the desired Firebase database table
        timestamp = int(time.time())  # Get the current UNIX timestamp
        ref = db.reference(table)

        # Create a JSON object to write to the database
        data = {
            'ph': ph,
            'time': timestamp
        }

        ref.push(data)  # Push the data to the database

        print(f"PH {ph} written to the database at timestamp {timestamp}")
    except Exception as e:
        print(f"Error: {e}")




def write_ec_to_database(ec):
    try:
        table = "ec_data"  # Replace with the desired Firebase database table
        timestamp = int(time.time())  # Get the current UNIX timestamp
        ref = db.reference(table)

        # Create a JSON object to write to the database
        data = {
            'ec': ec,
            'time': timestamp
        }

        ref.push(data)  # Push the data to the database

        print(f"EC {ec} written to the database at timestamp {timestamp}")
    except Exception as e:
        print(f"Error: {e}")

def write_flow_to_database(flow):
    try:
        table = "flow_data"  # Replace with the desired Firebase database table
        timestamp = int(time.time())  # Get the current UNIX timestamp
        ref = db.reference(table)

        # Create a JSON object to write to the database
        data = {
            'flow': flow,
            'time': timestamp
        }

        ref.push(data)  # Push the data to the database

        print(f"EC {flow} written to the database at timestamp {timestamp}")
    except Exception as e:
        print(f"Error: {e}")

    
def main():        
    relay_on(valve2)
    time.sleep(.1)
    relay_on(valve4)
    time.sleep(.1)           
    relay_on(valve6)
    time.sleep(.1)
    relay_on(valve7)
    time.sleep(.1)
    relay_on(sprinklerpump)
    time.sleep(.1)
    relay_on(sensorlinepump)
    time.sleep(.1)  

    while True:   #replace with the drain status or dosing
         ROfloatcheck(floatRO)
         time.sleep(.1)      
         NRfloatcheck(floatNR)
         time.sleep(.1)
         temperature = get_temperature()
         write_temperature_to_database(temperature)
         ph = get_ph(ph)
         write_ph_to_database(ph)
         ec = get_ec(ec)
         write_ec_to_database(ec)
         flow = flowsensor1(flow)
         write_flow_to_database(flow)

         #all the other constant readings, flow sensors and data sensors

         while (ROfloatcheck(floatRO) == 'high'):
              relay_on(ballvalve) # whichever opens the RO valve
         while (NRfloatcheck(floatNR) != 'high'):  
              relay_on(transferpump)  


         if(stepper1 == True):
                while cyclecount1 < cycles:
                    reverse(ENA1,DIR1,PUL1)
                    cyclecount1 = (cyclecount1 + 1)
         cyclecount1 = 0
         if(stepper2 == True):
                while cyclecount2 < cycles:
                    reverse(ENA2,DIR2,PUL2)
                    cyclecount2 = (cyclecount2 + 1)
         cyclecount2 = 0
         if(stepper3 == True):
                while cyclecount3 < cycles:
                    reverse(ENA3,DIR3,PUL3)
                    cyclecount3 = (cyclecount3 + 1)
         cyclecount3 = 0
"""          if(stepper4 == True):
                while cyclecount < cycles:
                    reverse(ENA4,DIR4,PUL4)
                    cyclecount = (cyclecount + 1)
         cyclecount = 0
         if(stepper5 == True):
                while cyclecount < cycles:
                    reverse(ENA5,DIR5,PUL5)
                    cyclecount = (cyclecount + 1)
         cyclecount = 0 """




if __name__ == '__main__':
    main()   
        
   

        
            

    
        
    

