import yaml
import socket
from datetime import datetime

def get_current_time():
	return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def parse_time(time):
	tokens = time.split()
	hour, minutes, seconds = tokens[1].split(":")

	return {
		"YearMonthDay" : tokens[0],
		"Hour" : hour,
		"Minutes" : minutes,
		"Seconds" : seconds
	}


def get_client_settings(default_configuration_file="client-config.yaml"): 
	try:
		with open(default_configuration_file) as f:
			configuration = yaml.load(f, Loader=yaml.FullLoader)
			return configuration	
	except FileNotFoundError:
		print("Sorry, the {0} file is missing.".format(default_configuration_file))
		sys.exit(1)		
	
def get_hostname():
	return socket.getfqdn()
