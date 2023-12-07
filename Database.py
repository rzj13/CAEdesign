#__author__ = "Christian L'Orange"
#__copyright__ = "Copyright 2023"
#__credits__ = ["Chrisitan L'Orange"]
#__license__ = "GPL"
#__version__ = "1.0.1"
#__email__ = "christian.lorange@colostate.edu"
#__status__ = "Beta"
#__description__ = "Example for senior design team on reading and writing to realtime database"
#__updated__ = "30 August 2023"


## libraries and pacakges
import firebase_admin # we will be using Google Firebase as the database (This is not a good scalable option, but free and easy for your project)
from firebase_admin import db # need to access database functionality
from firebase_admin import credentials # need to access credentials functionality
import time # we will look at time
import json # firebase databases are based on JSON formats

## establish connection with credentials
cred_object = firebase_admin.credentials.Certificate('C:\\Users\\ryanz\Desktop\\SD Proj\\AccountKey.json') # this is where you would add the credentials to access database
default_app = firebase_admin.initialize_app(cred_object, {
	'databaseURL':'https://senior-design-test-78c5a-default-rtdb.firebaseio.com/' 
	})

## establish the functions we are going to use

# write to database
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



## operating code
#write_to_database("controls","drain_valve","high") # this is going to write a new set of key pair objects to the database -- what if you wanted to write multiple things at once...you can do this
#write_to_database("controls","drain_valve","low")
#write_to_database("controls","mixing_manifold","10")
write_to_database("controls","floatsensor", "high")

drain_status = read_from_database("controls/drain_valve") # this will read the lastest value for a specific database endpoint and return an json object
print("drain status is currently " + drain_status["setting"])