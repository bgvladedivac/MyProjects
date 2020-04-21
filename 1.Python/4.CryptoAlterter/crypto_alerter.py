import requests
import json
import smtplib
import getpass
import os
import base64
from email.message import EmailMessage

email_from = ""
email_to = ""

rest_endpoints = {
	"get_all_coins" : "https://api.coinmarketcap.com/v2/listings/",
	"get_coin_by_id" : "https://api.coinmarketcap.com/v2/ticker/{0}/"
}

def create_email_message(from_address, to_address, subject, body):
    msg = EmailMessage()
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = subject
    msg.set_content(body)
    return msg

def evaluate_password():
	auth_file = "credentials"
	
	if not os.path.exists(auth_file):
		encode_password()

	return decode_password()

def encode_password():
	 ps = getpass.getpass(prompt="Password: ")
	 encoded_ps = base64.b64encode(ps.encode())
	 
	 with open("credentials", "wb") as f:
	 	f.write(encoded_ps)

	 return decode_password()

def decode_password():
	with open("credentials", "r") as f:
		content = f.readline()
		return str(base64.b64decode(content).decode("utf-8"))

data = requests.get(rest_endpoints["get_all_coins"]).json()['data']

coins = {}
header_columns = False

with open("coins", "r") as f:
	for line in f.readlines():
		line_parts = line.split()
		
		if header_columns:
			coin_name, amount, desired_value = line_parts[0], line_parts[1], line_parts[2] 
			coins[coin_name] = [amount, desired_value]
		
		header_columns = True

for coin in data:	
	if coin['symbol'].lower() in coins.keys():
		coins[coin['symbol'].lower()].append(coin["id"])
		
for coin in coins:
	price = requests.get(rest_endpoints["get_coin_by_id"].format(coins[coin][2])) \
	.json()['data'] \
	['quotes'] \
	['USD'] \
	['price']

	current_amount = price * float(coins[coin][0])
	
	if current_amount > coins[coin][2]:
		msg = """
		Hello,  
		Your crypto asset has just reached the target level.
		{0} ownings now worth {1}
		""".format(coin, str(current_amount))

		msg = create_email_message(email_from, email_to, "Crypto assets!", msg)

		with smtplib.SMTP('smtp.gmail.com', port=587) as smtp_server:
			smtp_server.ehlo()
			smtp_server.starttls()
			smtp_server.login(email_from, evaluate_password())
			smtp_server.send_message(msg)

		print("Email sent OK!")
	 
