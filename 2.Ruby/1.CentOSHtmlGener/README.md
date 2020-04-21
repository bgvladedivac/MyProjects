A Ruby script that would collection the following information from **RHEL 7 derivative**. The script assumes that you have 'firefox' as command line utility and enough user prilleges.

1. **File system information** ( logical volumes, mount points, size, free capacity and fs types, by default just xfs and ext4 ) 
2. **All installed packages** ( name, version, release, architecture, description ) 
3. **Users** ( users with id bigger than 1000, username, sudo or not, passwod expiration in days )
4. **Running services** ( ssh, nfs, http ... ) 

The result is a file called **display.html**
