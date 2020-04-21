#!/usr/bin/python

'''
    Simple introduction: adding user friendly aliases of the new presented luns.
'''
import sys, os, time, datetime
from shutil import copyfile

class Lun():
    def __init__(self, wwid, alias):
        self.wwid = wwid
        self.alias = alias

multipath_f = '/etc/multipath.conf'
multipath_copy = '/tmp/copy_multipath.conf'
file_msg = 'Enter a complete path to a file with lines being in a format "wwid alias", example being shown:'
file_eg = """
360002ac0000000000000029900014adf aSM_DISK_COREMST_DATA4
360002ac0000000000000029d00014adf asm_disk_COREMST_fra1
360002ac0000000000000029c00014adf Asm_disk_COREMST_fra1
"""
script_msg = "The argument number in the script is the line number from where the script will start writing in " + multipath_f

def print_info(sleep_time, *msgs):
    for msg in msgs:
        print(msg)
    time.sleep(sleep_time)

def retrieve_luns(file_name):
    luns = []
    with open(file_name, 'r') as f:
        for line in f:
            if not line.isspace():
                line_parts = line.split()
                current_lun = Lun(line_parts[0].lower(), line_parts[1])
                luns.append(current_lun)
    return luns

def generate_content(luns):
    mp_pattern = """
                multipath {
                        wwid %s
                        alias %s
                }
        """
    content = []
    for lun in luns:
            content.append(mp_pattern % (lun.wwid, lun.alias))
    return      "\n".join(content)

def write_content(file_name, line_number, content):
    with open(file_name, 'r') as f:
        lines = f.readlines()

    with open(file_name, 'w') as f:
        for i,line in enumerate(lines):
            if i + 1 == line_number:
                f.write("#Aliases Script started writing at " + str(datetime.datetime.now()))
                f.write(content)
                f.write("\n")
                f.write("#Aliases Script stopped writing at " + str(datetime.datetime.now()))
                f.write("\n")
                print("The following content has been added to " + multipath_f)
                time.sleep(1)
                print(content)
            f.write(line)
    time.sleep(2)
    print("The aliases have been written into " + multipath_f)

def get_input_based_on_py_version():
    if sys.version.startswith("3"):
        return input()
    else:
        return raw_input()

def encapsulate_logic():
    if os.path.isfile(multipath_f):
        print_info(1, script_msg)
        print_info(1, file_msg, file_eg)
        path = get_input_based_on_py_version()
        if os.path.isfile(path):
            time.sleep(1)
            print("Making a copy of the current" + multipath_f + " in " + multipath_copy)
            time.sleep(1)
            copyfile(multipath_f, multipath_copy)
            print("The copy has been made.")
            time.sleep(1)
            content = generate_content(retrieve_luns(path))
            write_content(multipath_f, int(sys.argv[1]), content)
        else:
            print("Sorry, the path is not a valid one.")
    else:
        print(multipath_f + " does not exist, bringing you back to the shell.")

def main():
    if len(sys.argv) > 1:
        encapsulate_logic()
    else:
        print("Sorry, the script needs a line number argument, example 'python script.py 29'")

if __name__ == '__main__':
    main()
