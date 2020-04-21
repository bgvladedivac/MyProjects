import boto3
import csv
import datetime
from botocore.config import Config

config = Config(
    retries = dict(
        max_attempts = 10
    )
)

aws_dcs = {
    "frankfurt": "eu-central-1",
    "ireland": "eu-west-1",
    "nvirginia": "us-east-1",
    "singapore": "ap-southeast-1",
    "sydney": "ap-southeast-2",
    "tokyo": "ap-northeast-1"
}


def get_pretty_tuples(tuple_list):
    output = []
    for tuple in tuple_list:
        output.append("{0} => {1}".format(tuple[0], tuple[1]))

    return ", ".join(output)


def take_care_for_output(instance_objects, region_name):
    now = datetime.datetime.now()

    with open("{0}-{1}-{2}-{3}.csv".format(region_name, str(now.year), str(now.month), str(now.day)), "w") as f:
        writer = csv.writer(f)
        writer.writerow(['InstanceID', 'NonEncryptedVolumes'])

        for instance_obj in instance_objects:
            row_data = []

            for key in instance_obj:
                row_data = [key, get_pretty_tuples(instance_obj[key])]

            writer.writerow(row_data)

def get_non_encypted_instances(ec2_object):
    non_encypted_instances = []

    for instance in ec2.instances.all():
        instance_non_encrypted_obj = {
            instance.instance_id: []
        }

        found_at_least_one_unencrypted_volume = False

        for volume in instance.volumes.all():
            if not volume.encrypted:

                found_at_least_one_unencrypted_volume = True

                for block_device_mapping in instance.block_device_mappings:
                    if block_device_mapping['Ebs']['VolumeId'] == volume.volume_id:
                        instance_non_encrypted_obj[instance.instance_id].append((block_device_mapping['DeviceName'], volume.volume_id))

        if found_at_least_one_unencrypted_volume:
            non_encypted_instances.append(instance_non_encrypted_obj)

    return non_encypted_instances

for dc_key in aws_dcs:   
    ec2 = boto3.resource('ec2', region_name = aws_dcs[dc_key], config=config)
    take_care_for_output(get_non_encypted_instances(ec2), dc_key)
