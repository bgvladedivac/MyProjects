'''
    Simple introduction: creates an AWS AMI, copies it to another region. Provision out of it. 
    You can easily change the AWS regions inside the 'regions' dictionary in the beginning of the file.

    Proper run: python migrate_instance.py instance_id image_name instance_type subnet new_instance_name
'''

import boto3
import sys
import time

AWS_ACCESS_KEY_ID = ""
AWS_SECRET_ACCESS_KEY = ""

service = "ec2"

regions = {
	"source" : "eu-central-1",
	"target" : "eu-west-1",
} 

def get_aws_client(region):
	return boto3.client(
		service,
		region,
		aws_access_key_id = AWS_ACCESS_KEY_ID,
		aws_secret_access_key = AWS_SECRET_ACCESS_KEY
	)

def get_instance_tags(instance_id):
	ec2_resource = get_aws_resource(regions["source"])
	ec2_instance = ec2_resource.Instance(instance_id)
	return ec2_instance.tags

def get_aws_resource(region):
	return boto3.resource(
		service,
		region,
		aws_access_key_id = AWS_ACCESS_KEY_ID,
		aws_secret_access_key = AWS_SECRET_ACCESS_KEY
	)


def is_img_available(client, img_id, operation="Creation"):
	while True:
		if operation == "Creation":
			print("Image not created. Wait for 10 seconds.")
		else:
			print("Image not been transfered. Wait for 10 seconds.")

		time.sleep(10)
		image = client.describe_images(ImageIds=[img_id])
		if image['Images'][0]['State'] == 'available':
 			print(operation + " finished.")
 			return 

try:

	# Create image w/f
	client_source = get_aws_client(regions["source"])
	img_id = client_source.create_image(InstanceId=sys.argv[1], Name=sys.argv[2])['ImageId']
	img_tags = get_instance_tags(sys.argv[1])

	# Set up new hostname 
	for tag_pair in img_tags:
		if tag_pair["Key"] == "Name":
			tag_pair["Value"] = sys.argv[5]

	# Check for img creation.
	is_img_available(client_source, img_id)

	# Copy img w/f
	client_destination = get_aws_client(regions["target"])
	new_img_id = client_destination.copy_image(
		Name = sys.argv[2],
		SourceImageId=  img_id,
		SourceRegion = regions['source'],
	)['ImageId']
	
	# Check for img copy.
	is_img_available(client_destination, new_img_id, operation="Copy")
		
	destination_resource = get_aws_resource(regions["target"])

	# Provision new instance
	destination_resource.create_instances(
		 ImageId=new_img_id,
		 MinCount=1,
		 MaxCount=1,
		 InstanceType=sys.argv[3], 
		 SubnetId=sys.argv[4],
		 KeyName="Bastion",
		 TagSpecifications=[
		{
			'ResourceType': 'instance',
			'Tags': img_tags
		},
		]
	)

except Exception as e:
	print(e)
