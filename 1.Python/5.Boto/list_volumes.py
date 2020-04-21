import boto3
import csv
import datetime

regions = [
	"eu-west-1", 
	"eu-central-1"
]

def write_results(volumes, region, encrypted=True):
	current_time = datetime.datetime.now()
	current_time = "_".join([str(current_time.year), str(current_time.month), str(current_time.day)]) 

	if encrypted:
		file_name = "".join([region, "_result_", current_time, "_encrypted", ".csv"])
	else:
		file_name = "".join([region, "_result_", current_time, "_unencyprted", ".csv"])

	with open(file_name, "w") as f:
		writer = csv.writer(f)
		writer.writerow(["InstanceId", "VolumeId", "Device", "Encrypted"])


		for volume in volumes:
			volume_attachments = volume.attachments

			for attachment in volume_attachments:
				writer.writerow([attachment['InstanceId'], attachment['VolumeId'], attachment['Device'], encrypted==True])

		print(file_name + " has been created.")

for region in regions:
	ec2 = boto3.resource('ec2', region_name=region)
	
	volumes = ec2.volumes.all()

	encrypted_volumes = [x for x in volumes if x.encrypted]
	unencrypted_volumes = [x for x in volumes if not x.encrypted]

	current_time = datetime.datetime.now()
	current_time = "_".join([str(current_time.year), str(current_time.month), str(current_time.day)]) 

	file_name = "".join([region, "_result_", current_time, ".csv"])

	write_results(encrypted_volumes, region)
	write_results(unencrypted_volumes, region, encrypted=False)

