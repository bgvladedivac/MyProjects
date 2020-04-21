import sys
import yaml
import os
import socket
import time
import pickle
from utils import get_current_time, get_client_settings, get_hostname

def evaluate_file_systems(settings):
	result = []
	tmp_file = "/tmp/fsinfo"

	os.system("df -hT | grep -v tmpfs | grep -iv filesystem > {0}".format(tmp_file))

	with open(tmp_file, "r") as f:
		lines = f.readlines()

		for line in lines: 
			line_tokens = line.split() 
			fs_usage_procent = int(line_tokens[5].split("%")[0])
			
			# 14.02.2020
			# WE NEED TO IMPLEMENT REAL HANDLING OF THIS
			# CURRENTLY THIS IS NOT TRIGGERED AS OF 
			# CURRENT TIME THE IDEA IS TO TEST END/END SOCKET
			# AND THEN INSERT INTO THE DB 
			if fs_usage_procent >= settings["threshold"]:
				result.append({
					"Hostname" : get_hostname(),
					"Filesystem" : line_tokens[0],
					"Type" : line_tokens[1],
					"Size" : line_tokens[2],
					"Use%" : fs_usage_procent, 
					"Mount Point" : line_tokens[6], 
					"TimeInsertion" :  get_current_time()
				})

	fs_data = pickle.dumps(result)

	os.system("rm -rf {0}".format(tmp_file))

	socket_client = socket.socket()
	socket_client.connect(("127.0.0.1", 8080))
	
	socket_client.send(fs_data)
	server_answer = socket_client.recv(1024)

	print(server_answer)

def evaluate_processes(settings):
	pass

def evaluate_packages(settings):
	pass


settings = get_client_settings()


while True:
	if "filesystem" in settings.keys():
		evaluate_file_systems(settings["filesystem"])
		time.sleep(1)
	elif "processes" in settings.keys():
		evaluate_client_settings(settings["processes"])
	elif "packages" in settings.keys():
		evaluate_packages(settings["packages"])
