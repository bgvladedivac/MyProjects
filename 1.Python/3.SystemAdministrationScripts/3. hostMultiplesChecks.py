#!/usr/bin/python

'''
    Python Version: 2.6.6
    Simple introduction: automation of customer vlan, divided in Ecom Bau Numbers.
'''

from __future__ import print_function
from collections import namedtuple
import os, platform, glob, re

hosts_in_vlan200 = ['gbwynlvweb001', 'gbwynlvweb002', 'gbwynlvweb003']

vlan_inventory_file = '/tmp/inventory'
patch_content = '/tmp/edsoutput'
patch_result = '/tmp/edspatch'
services_result = '/tmp/services'
hardware_result = '/tmp/hardware'
file_system_result = '/tmp/filesystems'

dev_pattern = ['sd.*']
disk_ntuple = namedtuple('partition',  'device mountpoint fstype')
usage_ntuple = namedtuple('usage',  'total used free percent')

def generate_patches_for_installation(quoter='2Q2016'):
	"""
	Ecom Bau 2 checks for the patches that need to be installed on each of the hostnames.
	By default, the quoter argument is changed on every 4 months.
	"""

	os.system('eds-linux-patch -a -m ' + quoter + ' > ' + patch_content)
	searchqueries = ['Advisory', 'RHEA', 'RHBA']

	with open(patch_content, 'r') as f:
		with open(patch_result, 'w') as f2:
			lines = f.readlines()
			f2.write("Patches for " + os.uname()[1] + " that needs to be installed ")
			for i, line in enumerate(lines):
				for query in searchqueries:
					if line.startswith(query):
						f2.write(line)

def get_listening_services(udp=False, tcp=False, both=True):
	"""
	Ecom Bau 6 checks for listening services, by default tcp/udp.
	"""

	services = []

	if both:
		os.system('netstat -ltu > /tmp/netstatinfo')
	elif udp:
		os.system('netstat -lu > /tmp/netstatinfo')
	elif tcp:
		os.system('netstat -lt > /tmp/netstatinfo')

	with open('/tmp/netstatinfo', 'r') as f:
		content = f.readlines()
		for line in content:
			line_parts = line.split()
			if not line_parts[0] == 'Active' and not line_parts[0] == 'Proto':
				services.append(line_parts[3])

	generate_listening_services_output(services, "all")

def generate_listening_services_output(services, port):
	"""
	Ecom Bau 6 checks for listening services, generates the content in file.
	"""

	counter = 1
	with open(services_result, 'w') as f:
		w.write("Currently listening services on " + port + " port/ports\n")
		for service in services:
			f.write(str(counter) + ". " + service +"\n")
			counter += 1

def get_size(device):
	nr_sectors = open(device+'/size').read().rstrip('\n')
	sect_size = open(device+'/queue/hw_sector_size').read().rstrip('\n')

	return (float(nr_sectors)*float(sect_size))/(1024.0*1024.0*1024.0)

def get_hardware_info():
	"""
	Ecom Bau 8 hardware review
	"""

	interfaces = os.listdir('/sys/class/net/')[-2:]
	with open('/proc/cpuinfo') as f:
		with open(hardware_result, 'w') as f2:
			f2.write("OS: " + platform.platform() + "\n")
			f2.write("Release: " + platform.release() + "\n")
			f2.write("Architecture: " + platform.architecture()[0] + "\n")
			f2.write("Interfaces: " + interfaces[0] + " " + interfaces[1] + "\n" )
			f2.write("Processing units: \n")

			counter = 1
			for line in f:
				if line.strip():
					if line.rstrip('\n').startswith('model name'):
						model_name = line.rstrip('\n').split(':')[1]
						f2.write(str(counter) + ". " + model_name + "\n")
						counter += 1

			for device in glob.glob('/sys/block/*'):
				for pattern in dev_pattern:
					if re.compile(pattern).match(os.path.basename(device)):
						f2.write('Device:: {0}, Size:: {1} GiB\n'.format(device, size(device)))

def get_disk_partitions(all=False):
	"""
	Return all mountd partitions as a nameduple.
	If all == False return phyisical partitions only.
	"""

	phydevs = []
	with open('/proc/filesystems', 'r') as f:
		for line in f:
			if not line.startswith('nodev'):
				phydevs.append(line.strip())
	

	retlist = []
	f = open('/etc/mtab', "r")
	for line in f:
		if not all and line.startswith('none'):
			continue
		fields = line.split()
		device = fields[0]
		mountpoint = fields[1]
		fstype = fields[2]
		if not all and fstype not in phydevs:
			continue
		if device == 'none':
			device = ''
		ntuple = disk_ntuple(device, mountpoint, fstype)
		retlist.append(ntuple)
	return retlist

def get_disk_usage(path):
	"""
	Return disk usage associated with path.
	"""
	st = os.statvfs(path)
	free = (st.f_bavail * st.f_frsize)
	total = (st.f_blocks * st.f_frsize)
	used = (st.f_blocks - st.f_bfree) * st.f_frsize
	try:
		percent = ret = (float(used) / total) * 100
	except ZeroDivisionError:
		percent = 0

	return usage_ntuple(total, used, free, round(percent, 1))

def get_file_systems():
	"""
	Ecom Bau 9 consists of file systems, drivers and scripts on the OS.
	Although the function name is get_file_systems(), it also returns the 
	drivers and scripts currently located in the OS.
	"""
	with open(file_system_result, 'w') as f:
		for part in disk_partitions():
			f.write("Device: " + part.device + "  Mountpoint: " +  part.mountpoint +  "  FSType: " +  part.fstype  + "\n")
			f.write("    %s\n" % str(disk_usage(part.mountpoint)) + '\n')

def main():
	#Ecom Bau 1 checks for all hostsnames in vlan200

	with open(vlan_inventory_file, 'w') as f:
		f.write("The hosts in vlan200: ")
		f.write(", ".join(hosts_in_vlan200))
		generate_patches_for_installation()	 
		get_listening_services()
		get_hardware_info()
		get_file_systems()
 
if __name__ == '__main__':
	main()

 
