import os
from utils import get_client_settings, get_hostname

mail_template = "To: {0}\nSubject: {1}\nFrom: {2}\n\n{3}"

def send_alert(subject, details):
	receiper = get_client_settings()["email"]
	content = mail_template.format(receiper, subject, get_hostname(), details)
	tmp_content_file = "/tmp/tmpcontentfile"	

	with open(tmp_content_file, "w") as f:
		f.write(content)
	
	os.system("sendmail -vt < " + tmp_content_file)
	os.system("rm -rf " + tmp_content_file)

