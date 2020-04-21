# File names in which the results from bash commands are stored.
FS_FILE = "/tmp/fsinfo"
PACKAGE_FILE = "/tmp/packinfo"
PASSWORD_FILE = "/tmp/passinfo"
SERVICES_FILE = "/tmp/servicesinfo"
RESULT_FILE = "/tmp/display.html"

# A class to represent a Linux file system. The properties are extracted
# from the standart 'df -hT' command. 
class FileSystem

  def initialize(lv, mp, size, free_cap, fs_type)
    @lv = lv
    @mp = mp
    @size = size
    @free_cap = free_cap
    @fs_type = fs_type
  end

  # A string representation of the file system, returning the file system
  # as a html row with each table data representing an attribute.
  def to_s
    """
    <tr>
      <td>#{@lv}</td>
      <td>#{@mp}</t>
      <td>#{@size}</td>
      <td>#{@free_cap}</td>
      <td>#{@fs_type}</td>
    </tr>
    """
  end

  # Static method declaration
  class << self

    # Extracts the file systems from the 'df -hT' output. By default
    # looks for 'xfs' and 'ext4' file system. You could add more by 
    # just extending the 'if line' (if line =~ /xfs/ || line =~ /ext/).
    def extract_fs
      system("df -hT > " + FS_FILE)
      file_systems = []
      content = get_file_content(FS_FILE)

      content.each_line do |line|
        if line =~ /xfs/ || line =~ /ext/
          line_parts = line.split
          file_systems << FileSystem.new(line_parts[0], line_parts[6], line_parts[4], \
            line_parts[5], line_parts[1])
        end

      end

      system("rm -f " + FS_FILE)
      file_systems
    end
  
    end
end

# A class to represent a rpm RHEL package. The properties are extracted
# from the 'rpm -qai'.
class Package
  
  attr_writer :name, :version, :release, :architecture, :description
 
  # All the package properties are assigned with optional arguments.
  def initialize(name = "", version = 0.0, release = 0, architecture = "noarch", description = "")
    @name = name
    @version = version
    @release = release
    @architecture = architecture
    @description = description
  end

  # A string representation of the package instance, returning the instance
  # as a html row with each table data representing an attribute.
  def to_s
    """
    <tr>
      <td>#{@name}</td>
      <td>#{@version}</t>
      <td>#{@release}</td>
      <td>#{@architecture}</td>
      <td>#{@description}</td>
    <tr>
    """
  end

  # Static methods.
  class << self

    # Extracts the packages, returning a list of them.
    def extract_packages
      system("rpm -qai > " + PACKAGE_FILE)
      packages =  []
      content = get_file_content(PACKAGE_FILE)
  
      current_pkg = nil
      line_counter = 1
    
      content.each_line do |line|
        if line =~ /Name/
           current_pkg = Package.new
           current_pkg.name = line.split(":")[1]
           line_counter += 1
        elsif  line =~ /Version/
           current_pkg.version = line.split(":")[1]
           line_counter += 1
        elsif line =~ /Release/
            current_pkg.release = line.split(":")[1]
            line_counter += 1
        elsif line =~ /Architecture/
            current_pkg.architecture = line.split(":")[1]
          line_counter +=1
        elsif line =~ /Description/
          description = IO.readlines(PACKAGE_FILE)[line_counter]  \
          + IO.readlines(PACKAGE_FILE)[line_counter + 1]
          current_pkg.description = description
          line_counter += 1
          packages << current_pkg
        else
            line_counter += 1
        end

      end

      system("rm -f " + PACKAGE_FILE)
      packages
    end
  end
  end

# A class to represent a user in the system. Properties:
# username = user name of the user.
# sudo = boolean expression whether the user is a sudo one.
# pass_exp_in_days = remaining days until the password is expired.
class User
  
  attr_accessor :sudo, :pass_exp_in_days

  def initialize(username="", sudo=false, pass_exp_in_days=90)
    @username = username
    @sudo = sudo
    @pass = pass_exp_in_days
  end

  # String representation of each user instance, returning the instance
  # as a html row with each table data representing an attribute.
  def to_s
    """
      <tr>
          <td>#{@username}</td>
          <td>#{@sudo}</td>
          <td>#{@pass_exp_in_days}</td>
      </tr>
    """
  end
  
  class << self

    # Extract and returns users with id over 1, 000.
    def extract_users
      users = []
      content = get_file_content("/etc/passwd")
      desired_user_id = 1000

      content.each_line do |line|
        line_parts = line.split(":")
        if line_parts[2].to_i > desired_user_id
	  username = line_parts[0]
          user =  User.new(username = username)
          user.sudo = User.is_sudo_user(username)
          user.pass_exp_in_days = User.get_pass_exp_in_days(username)
          users <<  user
        end
      end
      users
    end
  end

    # Check if a user is a sudo. Arguments:
    # un = user name that needs to be checked.
  private
   def self.is_sudo_user(un)

      content = get_file_content("/etc/group")
      sudo_group = "wheel"

      content.each_line do |line|
        line_parts = line.split(":")
        if line_parts[0] == sudo_group
          return true if line_parts[3].include?(un)
        end
      end

      false
    end

    # Get the days in which the password of the user will expire. Arguments:
    # un = user name which password must be checked.
    def self.get_pass_exp_in_days(un)
      system("chage -l " + un + " > " + PASSWORD_FILE)
      content = get_file_content(PASSWORD_FILE)

      content.each_line do |line|
	if line.start_with?("Password expires")
	  system("rm -f " + PASSWORD_FILE)
	  return line.split(":")[1]
	end
      end
     
     system("rm -f " + PASSWORD_FILE)
    end
  end

# Returns the content of the file. Arguments:
# dest = the destination of the file.
def get_file_content(dest)
  File.open(dest, "r").read
end

# Returns the running services in html table row/data format. Arguments:
# services = list of services that needs to be checked.
def are_services_running(services)
  system("ss -lt > " + SERVICES_FILE)
  result = [] 

  services.each do |service|
    if File.foreach(SERVICES_FILE).detect { |line| line.include?(service) } 
    	result << "<tr><td>Service #{service} is running</td></tr>"
    end
  end
  
  system("rm -f " + SERVICES_FILE)
  result
end

# Concatenates all different sets of objects to return 1 global. Arguments:
# obj = objects that needs to be concatenated.
def concatenate_html(obj)
  content = ""
  obj.each do |o|
    content += o.to_s
  end
  content
end



# Set the html for all the objects. Arguments:
# filesystems = file systems
# packages = packages
# users = users
def generate_html(filesystems, packages, users)
  service_status = are_services_running(["ssh", "nfs", "http"])

  html_content =
  """
  <html><head><title>Linux box info</title></head>
  <body><table>
    <tr>
      <th>Logical Volume</th>
      <th>Mount Point</th>
      <th>Size</th>
      <th>Free</th>
      <th>FS Type</th>
   </tr>#{concatenate_html(filesystems)}

    <tr>
      <th>Name</th>
      <th>Version</th>
      <th>Release</th>
      <th>Architecture</th>
      <th>Description</th>
    </tr>#{concatenate_html(packages)}

    <tr>
      <th>Username</th>
      <th>Sudo</th>
      <th>Password expiration</th>
    </tr>#{concatenate_html(users)}

    <tr>
      <th>Service status</th>
    </tr>#{service_status}
  </table></body>
  </html>
  """

  File.open(RESULT_FILE, 'w') { |file| file.write(html_content)}
end

generate_html(FileSystem.extract_fs, Package.extract_packages, User.extract_users)
system("firefox file://" + RESULT_FILE)

