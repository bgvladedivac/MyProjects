import socket
import threading
import pickle
import time
import sys
import os
from contextlib import contextmanager
from db import DataController 
from utils import get_current_time, parse_time# this needs to be transfered to a utility
from sender import send_alert


def handle_client_connection(connection):
	client_socket, client_address = connection
	client_data = client_socket.recv(1024)
	
	if len(client_data) > 0:
		client_data = pickle.loads(client_data)
		
		dc = DataController()	
		for entry in client_data:
			dc.navigate_data(entry)

	client_socket.close()
		

def evaluate_alerts():
	time.sleep(10)

	dc = DataController()
	tables = [ "filesystem" ]
	
	# Evaluate alerts runs in a separate dedicated thread, so it must be always running.
	while True:
		for table in tables:
			records = dc.retrieve_records(table, "timeinsertion")	
			
			# This needs to be updated/done
			# Currently just left the variable as a remainder
			track_already_sent_alerts = {
				"filesystem" : [] 
			}			

			if table == "filesystem":
				print("Retrieving the records from file system table.")

				for record in records:
					print("Record for evaluation")	
					print(record)
					current_time_tokens = parse_time(get_current_time())	
				
					# This try might not be needed, since the table wont accept records with missing index 7th	
					try:
						record_time_tokens = parse_time(record[7])
						if current_time_tokens["YearMonthDay"] == record_time_tokens["YearMonthDay"] and\
							current_time_tokens["Hour"] == record_time_tokens["Hour"]:
							
							if int(current_time_tokens["Minutes"]) - int(record_time_tokens["Minutes"]) == 1:
								print("OK I would send an alert now")# alert
								send_alert("FileSystem Alert", record)
							
					except IndexError:
						pass



@contextmanager
def handle_server_socket_resources():
	server_socket = socket.socket()
	try:
		yield server_socket
	finally:
		server_socket.close()


with handle_server_socket_resources() as server_socket:
	server_socket.bind(("localhost", 8080))	
	server_socket.listen()

	handle_alerts_started = False

	while True:
		conn = server_socket.accept()
		t = threading.Thread(target=handle_client_connection, args=(conn,))	
		t.start()
		# Handle evaluation of alerts, idea is to have a dedicated thread that keeps running all the time.
		if not handle_alerts_started:
			handle_alerts_started = True
			handle_alerts_thread = threading.Thread(target=evaluate_alerts, args=())	
			handle_alerts_thread.start()

