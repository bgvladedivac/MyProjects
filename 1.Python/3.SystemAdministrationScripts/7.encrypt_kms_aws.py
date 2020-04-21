#!/usr/bin/python

'''
    Python Version:  3x
    Simple introduction: encypt credentials by using the master key in AWS KMS. 
    Stores the byte output in a hidden read only file.
'''


import getpass
import boto3
import os
from stat import S_IREAD

creden = """
	un:{},
	pass:{}
""" 

def get_hidden_input(input_proprety):
	return getpass.getpass(input_proprety)

un = get_hidden_input('Username: ')
pswd = get_hidden_input('Password: ')

creden = creden.format(un, pswd)

ACCESS_KEY = get_hidden_input('Access Key: ')
SECRET_KEY = get_hidden_input('Secret Key: ')

client = boto3.client(
	'kms',
	 aws_access_key_id=ACCESS_KEY,
	 aws_secret_access_key=SECRET_KEY,
	 region_name='eu-central-1'
)

#Better to look up the key id by the API, not hard code it.
response = client.encrypt(
	KeyId='',
	Plaintext=creden,
	EncryptionContext={
		'string':'string'
	}
)


encrypted_msg = response['CiphertextBlob']

with open(".credens", "wb") as f:
	f.write(encrypted_msg)

os.chmod(".credens", S_IREAD)
