#!/usr/bin/python

'''
    Python Version: 2x, 3x
    Simple introduction: add a set of users, following best ITIL practices.
'''



import os, time, sys

def get_input_based_on_py_vers(msg):
        if sys.version.startswith("3"):
                return input(msg)
        else:
                return raw_input(msg)

def print_info():
        print("This script will add a set of users to the current Linux distribution.")
        print("The script will expect a file with the following properties, seperated by space: ")
        print("Change_id user_name geco_information")
        print("Example being shown: ")
        time.sleep(1)
        print()
        print("E2-C00488741 username firstname.familyname@company.co.uk")
        print("E2-C00488741 username firstname.familyname@company.co.uk")
        print()

def get_users():
        users = {}
        file_destination = get_input_based_on_py_vers("Please enter a path to the file: ")
        if os.path.isfile(file_destination):
                with open(file_destination, 'r') as f:
                        for line in f:
                                line_parts = line.split()
                                users[line_parts[1]] = "%s, %s" % (line_parts[0], line_parts[2])
                return users
        else:
                print("Sorry the provided path does not exist.")
                exit

def add_users(users, password):
        for key in users.keys():
                creation_user_execution_stat =  \""useradd -c \"%s\" -p $(echo%s\" | openssl passwd -1 -stdin) %s" \
                        % (users[key], password, key)
                os.system(creation_user_execution_stat)

                pass_change_first_login_exec_stat = "chage -d 0 %s" % (key, )
                os.system(pass_change_first_login_exec_stat)

                print("User " + key + " was just added.")

def main():
        print_info()
        users = get_users()
        add_users(users, "Password123")

if __name__ == "__main__":
        main()
