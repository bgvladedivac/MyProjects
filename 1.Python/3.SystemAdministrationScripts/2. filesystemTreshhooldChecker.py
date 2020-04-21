#!/usr/bin/python

'''
    Simple introduction: search file systems with usage over 90 % and sends an email.
'''

import os, re
import smtplib
import subprocess

class Treshhold():
	def __init__(self, mount_point, space, treshhold_number):
		self.mount_point = mount_point
		self.space = space
		self.treshhold_number = treshhold_number

	def __str__(self):
		return "Filesystem on " + self.mount_point + " has reached " + str(space) + " on required " + treshhold_number 

def check_for_running_services(searched_services = ['sshd', 'httpd']):
	output = subprocess.check_output(['ps', '-ef'])
	for s in searched_services:
		if s in output:
			print(s + " is running.")
		else:
			send_email(s + " is not running", 'email_address@gmail.com', 'Password', 'email_address@gmail.com')


def get_fs_info():
	os.system('df -HT > /tmp/filesysteminfo')
	result = []

	with open('/tmp/filesysteminfo', 'r') as f:
		fs_output = f.readlines()
		for line in fs_output:
			parts = line.split()
			used_space = re.findall(r'\d+', parts[5])
			mount_point = parts[6]
			if hasattr(used_space, 'len'):
				result.append((mount_point, used_space))
	return result

def check_for_treshhoold(fs_tuples, treshhold_number=90):
	for fs_tuple in fs_tuples:
		if fs_tuple[1] > treshhold_number:
			return Treshhold(fs_tuple[0], fs_tuple[1], treshhold_number)
	return False

def send_email(msg, sender_email, passw, receiver_email):
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(email, passw)
        server.send_email(email, receiver_email, msg)
        server.quit()
	
def main():
	fs_info = get_fs_info()
	if isinstance(check_for_treshhoold(fs_info), Treshhold):
		treshhold = check_for_treshhoold(fs_info)
		send_email(str(treshhold), 'email_address@gmail.com', 'Password', 'email_address@gmail.com')
	else:
		print("Everything is ok with the file systems.")

	os.system('rm -f /tmp/filesysteminfo')	
	check_for_running_services()
 
if __name__ == '__main__':
	main()











