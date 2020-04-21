#!/usr/bin/python

'''
    File name: infoGainer.py
    Author: If Beli
    Date created: 11/22/2016
    Date last modified: 31/07/2016
    Python Version: 3x
    Simple introduction: collects Linux node information and generates HTML result file.
'''

import os, platform, inspect
from rpmUtils.miscutils import splitFilename

LOCAL_FS_TYPES = ['ext4', 'xfs']
REMOTE_FS_TYPES = ['nfs', 'cifs']
SEARCHED_SERVICES = [':ssh', ':httpd']

class User:
    """
        User class to represent Linux user obj.
        :un: username.
        :un_id: username id.
        :home_dir: home directory of the user.
        :shell: shell of the user.
        :groups: groups to whom the user belongs.
    """
    
    def __init__(self, un, un_id, home_dir, shell, groups):
        self.un = un
        self.un_id = un_id
        self.home_dir = home_dir
        self.shell = shell

        self.groups = groups

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "Username {0}".format(self.un)

    def __eq__(self, other):
        return self.un == other.un and self.un_id == other.un_id

    @staticmethod
    def get_properties():
        """
        Returns all the properties of the user object 
        :return: list
        """
        return ["Username", "Username ID", "Home Directory", "Shell", "Groups"]


class Package:
    """
        Package class to represent rpm Linux pkg.
        :name: name of the package.
        :version: version of the package.
        :release: release of the package.
    """
    
    def __init__(self, name, version, release):
        self.name = name
        self.version = version
        self.release = release

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "Package Name: {0} Package Version: {1} Package Release{2}"\
            .format(self.name, self.version, self.release)
    
    def __eq__(self, other):
        return self.name == other.name and self.version == other.version and \
            self.release == other.release
    
    @staticmethod
    def get_properties():
        """
        Returns all the properties of the package object 
        :return: list
        """
        return ["Name of package", "Version", "Release"]


class Service:
    """
        Services class to represent Linux service.
        :name: the name of the service.
        :port: port to which the sevice is binded.
        :state: the state of the service.
    """
    def __init__(self, name, port, state):
        self.name = name
        self.port = port
        self.state = state

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "Service name: {0} Service port: {1} Service state: {2}"\
            .format(self.name, self.port, self.state)
    
    """
        Returns all the properties of the service object 
        :return: list
    """
    @staticmethod
    def get_properties():
        return ["Name of service", "Port", "State"]


class FileSystem:
    """
        Filesystem class to represent the Linux fs. Properties taken by 'df -hT'.
        :block_device: the block device to which the fs is presented.
        :block_device_size: the size of the block device.
        :free_size: the free size of the fs.
        :fs_type: the type of the filesystem.
        :mount_point: the mount point where the fs is mounted.
    """
    
    def __init__(self, block_device, block_device_size, free_size, fs_type, mount_point):
        self.block_device = block_device
        self.block_device_size = block_device_size
        self.free_size = free_size
        self.fs_type = fs_type
        self.mount_point = mount_point

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "Block Device: {0} Block Device Size: {1} Free Size: {2} Fs Type: {3} Mount Point: {4}"\
            .format(self.block_device, self.block_device_size, self.free_size, self.fs_type, self.mount_point)

    @staticmethod
    def get_properties():
        return ["Block Device", "Block Device Size", "Free Size", "FS Type", "Mount Point"]


class Utils:
    """
        Standart utility class to handle static functions. 
    """
        
    @staticmethod
    def get_all_users(user_file="/etc/passwd"):
    """
       Extract users.
       :param user_file: the filename from which the usernames will be extracted.
       :return: list
    """
        users = []
        content = Utils.get_content(user_file)
        user_id = 500
        temp_groups_file = "/tmp/groupsinfo"

        for line in content:
            line_parts = line.split(":")

            if (int(line_parts[2])) > user_id:
                os.system("groups " + line_parts[0] + " > " + temp_groups_file)

                with open(temp_groups_file, 'r') as f:
                    groups = " ".join([str(x) for x in f.readline().split(":")[1:]])


                    current_user = User(line_parts[6], groups, line_parts[2], line_parts[5], line_parts[0])
                    print("Adding " + str(current_user))
                    users.append(current_user)

                os.system("rm -f " + temp_groups_file)

        return users

    @staticmethod
    def get_content(file_name, state='r'):
    """
       Extract users.
       :param user_file: the filename from which the usernames will be extracted.
       :return: list
    """        
        with open(file_name, state) as f:
            f_content = f.readlines()
            return f_content

    @staticmethod
    def get_packages():
    """
       Extract packages.
       :return: list
    """
        packages = []
        package_location_file = "/tmp/packagesinfp"
        os.system("rpm -qa > " + package_location_file)

        content = Utils.get_content(package_location_file)
        for line in content:
            package_info = splitFilename(line)
            current_package = Package(package_info[0], package_info[1], package_info[2])

            print("Adding package " + str(current_package))
            packages.append(current_package)

        os.system("rm -f " + package_location_file)

        return packages

    @staticmethod
    def get_file_systems(local=True, remote=False, both=False):
    """
       Extract file systems.
       :param local: only local file systems like xfs.
       :remote: remote file system like NFS and smb.
       :both: both type of file systems
       :return: list
    """
        result = []
        file_name = '/tmp/fsinfo'
        command = 'df -HT | grep -e '

        if local:
            os.system(
                command + LOCAL_FS_TYPES[0] + ' -e ' + LOCAL_FS_TYPES[1] + " > " + file_name)
        elif remote:
            os.system(
                command + REMOTE_FS_TYPES[0] + ' -e ' + REMOTE_FS_TYPES[1] + " > " + file_name)
        elif both:
            os.system(command + LOCAL_FS_TYPES[0] + ' -e ' + LOCAL_FS_TYPES[1] + " -e " +
                      REMOTE_FS_TYPES[0] + ' -e ' + REMOTE_FS_TYPES[1] + " > " + file_name)

        f_content = Utils.get_content(file_name)

        for l in f_content:
            l_parts = l.split()
            current_fs = FileSystem(l_parts[0], l_parts[2], l_parts[
                                    5], l_parts[1], l_parts[6])
            print("Adding File System " + str(current_fs))
            result.append(current_fs)

        os.system('rm -rf ' + file_name)

        return result

    @staticmethod
    def get_services(tcp=True, udp=False, both=False):
    """
       Extract services
       :param tcp: tcp services
       :udp: udp services
       :both: both tcp and udp services.
       :return: list
    """
        result = []
        file_name = '/tmp/servicesinfo'
        command = 'ss -l'

        if tcp:
            os.system(command + 't >' + file_name)
        elif udp:
            os.system(command + 'u >' + file_name)
        elif both:
            os.system(command + 'tu > ' + file_name)

        f_content = Utils.get_content(file_name)

        for line in f_content:
            for service in SEARCHED_SERVICES:

                if line.find(service) != -1:
                    parts = line.split()[0]
                    current_service = Service(service, Utils.get_service_port(service[1:]), parts[0])

                    print("Adding " + str(current_service))
                    result.append(current_service)

        return result

    @staticmethod
    def get_service_port(name):
        content = Utils.get_content('/etc/services')

        for line in content:
            line_parts = line.split()

            try:
                if line_parts[0] == name:
                    port = line_parts[1].split("/")[0]
                    return port

            except Exception:
                pass


class HtmlGenerator:
    
    """
      HtmlGenerator class to generate html table headers and close the HTML document.
    """
    
    def __init__(self):
        self.file_name = "/tmp/result.html"
        self.table = ['<htm><body><table border="1">']

    def generate_table_headers(self, objects):
        """
          Generates the headers for specific set of objects ( Filesystems, Packages ... )
          :param objects: the objects for which the table headers will be generated.
        """
        
        with open(self.file_name, 'w') as f:

            obj = objects[0]
            headers = None

            if isinstance(obj, FileSystem):
                headers = FileSystem.get_properties()
                self.generate_header_row(headers)

            elif isinstance(obj, User):
                headers = User.get_properties()
                self.generate_header_row(headers)

            elif isinstance(obj, Package):
                headers = Package.get_properties()
                self.generate_header_row(headers)

            elif isinstance(obj, Service):
                headers = Service.get_properties()
                self.generate_header_row(headers)

            for obj in objects:
                public_props = (name for name in dir(obj) if not name.startswith('_'))
                row_created = False

                for prop in public_props:
                    try:
                        table_data = (obj.__dict__[prop])
                        if row_created:
                            self.table.append(r"<td>{}</td>".format(table_data))
                        else:
                            self.table.append(r'<tr><td>{}</td>'.format(table_data))
                            row_created = True
                    except KeyError:
                        pass

                self.table.append(r'</tr>')

    def generate_header_row(self, headers):
        """
          Generates the number of headers.
          :param headers: number of headers to be generated.
        """
        
        row = False

        for h in headers:
            if row:
                self.table.append(r'<th>{}</th>'.format(h))
            else:
                self.table.append(r'<tr><th>{}</th>'.format(h))
                row = True

        self.table.append(r'</tr>')
    
    def close_content(self):
       """
         Closes the html content.
       """
    
        self.table.append('</table></body></html>')
        with open(self.file_name, 'w') as f:
            f.write("".join(self.table))

def main():
    #Extract file systems, services, users and packages
    filesystems = Utils.get_file_systems()
    services = Utils.get_services()
    users = Utils.get_all_users()
    packages = Utils.get_packages()
    
    #Initialize the html generator object
    htmlGen = HtmlGenerator()
    
    #Create the headers
    htmlGen.generate_table_headers(filesystems)
    htmlGen.generate_table_headers(services)
    htmlGen.generate_table_headers(users)
    htmlGen.generate_table_headers(packages)
    
    #Close the html document.
    htmlGen.close_content()

if __name__ == '__main__':
    main()
