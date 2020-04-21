#!/usr/bin/python

'''
    Simple introduction: checks RedHat installation for proper customer requested settings.
'''

import os

target_user="de_vscan"
target_group="wheel"
redhat_url_sudo_policy="https://access.redhat.com/documentation/en-US/Red_Hat_Enterprise_Linux_OpenStack_Platform/2/html/Getting_Started_Guide/ch02s03.html"

def get_file_content(file_name):
  with open(file_name, 'r') as f:
    return f.readlines()

def get_redhat_release():
  release_line = get_file_content("/etc/system-release")[0]
  release_numbers = [int(x) for x in release_line if x.isdigit()]
  if release_numbers[0] == 6:
    return "RedHat 6"
  elif release_numbers[0] == 7:
    return "RedHat 7"
     
def check_existing_user(user):
  file_content = get_file_content("/etc/passwd")
  for line in file_content:
    line_parts = line.split(";")
    if line_parts[0].lower() == user:
      return True
  return False

def check_user_being_part_of_group(user, group):
  os.system("getent group %s > result" % group)
  content = get_file_content("result")
  if user in content:
    print(user + " is added as sudo user.")
  else:
    print(user + " user is not added to the wheel group.")
    print("Please follow the RedHat7 sudo policy: ")
    print(redhat_url_sudo_policy)
  os.system("rm f result")
  
def adjust_release_user_existence():
  if get_redhat_release() == "RedHat 6":
    if file_contains_pattern("/etc/sudoers", target_user):
      print(target_user  + " is added as sudo.")
    else:
      print(target_user + " does not exist as sudo.")
  elif get_redhat_release() == "RedHat 7":
      check_user_being_part_of_group(target_user, target_group)
  else:
      print("Sorry, the script does not support your current RedHat release")
           
def file_contains_pattern(file_name, *pattern):
  result = ([x for x in pattern if x in open(file_name).read()])
  return len(result) == len(pattern)
    
def check_for_snow_client_installation(destination="/etc/snowclient.conf"):
  if os.path.isfile(destination):
    with open(destination, 'r') as f:
      first_line = f.readline().split("//")
      web_server_ip = first_line[len(first_line)-1]
      print("Snow agent is installed.")
      print("The web server to which Snow Agent reports: " + web_server_ip)
  else:
      print("Sorry, " + destination + " does not exist as a file.")

def check_ssh_session_timeout(file_name="/etc/ssh/sshd_config", first_property="ClientAliveInterval 7200", \
second_property="ClientAliveCountMax 0"):
  if file_contains_pattern(file_name, first_property, second_property):
    print("The SSH session time out is configured properly.")
  else:
    print("SECURITY BRIDGE => ssh session time out is not configured according to security policy.")
    
def check_pam_policy_settings(file_name="/etc/pam.d/password-auth-hpes", first_property="deny=5", \
second_property="password    requisite     pam_cracklib.so try_first_pass reject_username retry=3  type= minlen=8 lcredit=-1 ucredit=-1 dcredit=-1 difok=3 ocredit=-1 maxrepeat=2 minclass=3", \
third_property="password    sufficient    pam_unix.so sha512 shadow  try_first_pass use_authtok remember=5"):
  if file_contains_pattern(file_name, first_property, second_property, third_property):
    print("The PAM settings are configured properly.")
  else:
    print("SECURITY BRIDGE => pam settings are not configured properly")

def check_se_linux_being_disabled(file_name=["/etc/sysconfig/selinux", "/etc/selinux/config"], first_property='SELINUX=disabled'):
  if file_contains_pattern(file_name[0], first_property) and file_contains_pattern(file_name[1], first_property):
    print("SELINUX is configured properly.")
  else:
    print("SELINUX is not disabled.")
    
def main():
  adjust_release_user_existence()
  check_ssh_session_timeout()
  check_pam_policy_settings()
  check_for_snow_client_installation()
  check_se_linux_being_disabled()

if __name__ == "__main__":
    main()
