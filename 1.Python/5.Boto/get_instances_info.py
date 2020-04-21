import boto3
import csv

data_centers = {
	"N.Virginia" : "us-east-1",
	"Singapore" : "ap-southeast-1",
	"Sydney" : "ap-southeast-2",
	"Tokyo" : "ap-northeast-1",
	"Frankfurt" : "eu-central-1",
	"Ireland" : "eu-west-1"
}

def get_tag_value(tags, tag_value = "OS"):
	for tag in tags:
		if tag['Key'] == tag_value:
			return tag['Value'] 

def write_data_for_region(instance_objects, region):

	with open("{0}.csv".format(region), mode="w") as region_result:
		field_names = ["InstanceId", "PrivateDnsName", "SubnetId", "State", "OS", "Volumes"]
		writer = csv.DictWriter(region_result, fieldnames = field_names)

		writer.writeheader()

		for instance_object in instance_objects:
			writer.writerow(instance_object)

def get_volumes_info(volume):
	volume_info = []

	for volume in volumes:
		volume_info.append(volume['Attachments'][0]['Device'])
		volume_info.append(volume['Attachments'][0]['VolumeId'])
		volume_info.append(volume['Encrypted'])

	return volume_info

instance_objects = [ ]

for data_center in data_centers:
	client = boto3.client('ec2', region_name = data_centers[data_center])
	instances = client.describe_instances()['Reservations'] 
	
	for instance in instances:
		instance_details = instance['Instances'][0]
 
		os = "N/A"
		if 'Tags' in instance_details:
			os = get_tag_value(instance_details['Tags'])
		
				
		volumes = client.describe_volumes(
			Filters = [
				{
					'Name': "attachment.instance-id",
					'Values': [
						instance_details['InstanceId']
					]
				}
			]
		)['Volumes']

		instance_object = {
			"InstanceId" : instance_details["InstanceId"],
			"PrivateDnsName" : instance_details["PrivateDnsName"],
			"SubnetId" : instance_details["SubnetId"],
			"State" : instance_details["State"]["Name"],
			"OS" : os,
			"Volumes" : get_volumes_info(volumes)
		}			
			
		instance_objects.append(instance_object)

	write_data_for_region(instance_objects, data_center)
	instance_objects = []

 
