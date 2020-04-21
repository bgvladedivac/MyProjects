#!/usr/bin/python

'''
    File name: udevOracleRules.py
    Author: If Beli
    Date created: 2/3/2016
    Date last modified: 21/08/2017
    Simple introduction: creating the proper udev rules for adding Oracle disks.
'''

import sys, os, time
from shutil import copyfile

class Lun():
    def __init__(self, wwid, alias):
        self.wwid = wwid
        self.alias = alias

udev_rules_path = '/etc/udev/rules.d/99-asmmultipath.rules'
file_msg_format = """
        Enter a path to a file in a format 'wwid alias', example being shown: 
        361231adf asm_disk_fra_1
        367127abf asm_fisk_fra_2
        """
def get_input_based_on_py_vers():
    if sys.version.startswith("3"):
        return input()
    else:
        return raw_input()

def retrive_luns(file_name):
    luns = [] 
    with open(file_name, 'r') as f:
        lines = f.readlines()
        for line in lines:
            if not line.isspace():
                line_parts = line.split()
                current_lun = Lun(line_parts[0], line_parts[1])
                luns.append(current_lun)
        return luns

def file_exists(file_name):
    return os.path.isfile(file_name)

def get_lun_properties(luns):
    result = ""
    for lun in luns:
        wwid = "mpath-" + lun.wwid
        symlink = "oracle_asm/" + lun.alias
        line_propertes = ['ADCTION=="add|change"', 'ENV{DM_UUID}=="%s"' %
        wwid, 'SYMLINK+="%s"' % lun.alias, 'GROUP="oinstall"', 'OWNER="oragrid"', 'MODE="0660"']
        current_result = ", ".join(line_propertes)
        current_result += '\n'
        result+=current_result
    return result

def generate_oracle_asm(file_name, luns, **kwargs):
    if "Append" in kwargs:
        with open(file_name, 'a') as f:
            f.write(luns)
    else:
        with open(file_name, 'w') as f:
            f.write(luns)
    print("The Oracle ASM configuration is stored in " + udev_rules_path)

def inform_user():
    print("This sciprt will add the appropriate luns into " + udev_rules_path)
    print("Pick 1 for generating brand new file or overriding existing one.")
    print("Pick 2 for appending on already existing file.")

def append_to_file(choice):
    return choice == "2"

def get_user_input():
    choice = get_input_based_on_py_vers()
    if choice == "1" or choice == "2":
        print(file_msg_format)
        time.sleep(1)
        path = get_input_based_on_py_vers()
        if file_exists(path):
            luns = retrive_luns(path)
            properties = get_lun_properties(luns)
            if append_to_file(choice):
                print("Making a copy of the current configuration in /tmp just in case")
                time.sleep(1)
                copyfile(udev_rules_path, '/tmp/99-asmmultipath.rules')
                generate_oracle_asm(udev_rules_path, properties, Append=True)
            else:
                generate_oracle_asm(udev_rules_path, properties)
        else:
            print("Sorry, the path is not a file. Bringing you back to bash")
    else:
        print("Sorry, no such option. Bringing you back to bash.")

def main():
    inform_user()
    get_user_input()

if __name__ == "__main__":
    main()
