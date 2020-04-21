'''
    Python Version:  3x
    Simple introduction: decrypt encypretd credentials stored in a byte file using the AWS KMS master key.
    Sets 2 different env variables that could be referenced by other programs. The idea is to be used as 
    part of the automation process, as pure txt credentials are not stored somewhere. Do not forget to 
    remove the environment variables after the authentication step is performed.
'''



import getpass
import boto3
from subprocess import check_output

def get_hidden_input(input_proprety):
	return getpass.getpass(input_proprety)

ACCESS_KEY =  get_hidden_input('Access Key: ')
SECRET_KEY =  get_hidden_input('Secret Key: ')

client = boto3.client(
	'kms',
	 aws_access_key_id=ACCESS_KEY,
	 aws_secret_access_key=SECRET_KEY,
	 region_name='eu-central-1'
)


with open(".credens", "rb") as f:
	file_content = f.read()

decrypted_msg = client.decrypt(
	CiphertextBlob = file_content,
	EncryptionContext = {
		'string':'string'
	}
)

decrypted_msg = decrypted_msg['Plaintext']
 
content = decrypted_msg.decode().split(",")
 
env1 = content[0].split(":")[1]
env2 = content[1].split(":")[1]

check_output("setx UN " + env1)
check_output("setx PASS " + env2)
