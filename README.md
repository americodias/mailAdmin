emailAdmin
==============

About
--------------

This is a small collections of scripts to manage a simple email
server based on Postfix, Dovecot and MySQL. For more information
on how to setup this configuration, please read the tutorial
written for DigitalOcean by Nestor de Haro, available here:

http://goo.gl/y0kY0k

Prerequisites
--------------

These scripts are compabible with Python 2.7.3. I don't know if they
work on Python 3, but you can try. :)

You need to install a python module called
[texttable](https://pypi.python.org/pypi/texttable). To install it
just run:

```
sudo easy_install texttable
```

Usage
--------------

First you'll need to edit the configuration file *config.ini* according
with your configuration. My configuration is as follows:

```
[database]
host = localhost
user = usermail
password = PASSWORD_HERE
name = servermail

[disk]
vhostdir = /var/mail/vhosts
uid = 5000
gid = 5000

```

For more information, please read the tutorial referred above.

Now you will be able to run the scripts as follows:

```
sudo ./addUser.py -e email -p password
sudo ./removeUser.py -e email
./changePassword.py -e email -p newpassword
./listUsers.py

sudo ./addDomain.py -d domain
sudo ./removeDomain.py -d domain
./listDomains.py

./addAlias.py -s source -d destination
./removeAlias.py -s source
./listAliases.py
```

Some scripts need root permissions in order to create or delete the mailboxes
on disk.
