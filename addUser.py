#!/usr/bin/python
# -*- coding: utf-8 -*-
# Americo Dias - Jun 2014

import sys, os, getopt
import MySQLdb as mdb
from ConfigParser import SafeConfigParser

# Configuration file
configFile='config.ini'

def usage(scriptName):
    print scriptName, '-e email -p password'

def addUser(userEmail, userPassword):
    # Define variables
    emailName=userEmail.split('@')[0]
    domainName=userEmail.split('@')[1]
    
    parser = SafeConfigParser()
    parser.read(configFile)
    dbHost = parser.get('database', 'host')
    dbUser = parser.get('database', 'user')
    dbPass = parser.get('database', 'password')
    dbName = parser.get('database', 'name')

    mailBoxDirectory = parser.get('disk', 'vhostdir') + '/' + domainName + '/' + emailName
    mailUID = int(parser.get('disk', 'uid'))
    mailGID = int(parser.get('disk', 'gid'))

    # Connect with database
    con = mdb.connect(dbHost, dbUser, dbPass, dbName);

    with con:
        # Check if domain exists
        cur = con.cursor()
        cur.execute("SELECT * FROM  `virtual_domains` WHERE  `name` =  '" + domainName + "'")
	
        if cur.rowcount == 0:
            print("Domain " + domainName + " does not exist. user not created! Bye!")
            return -1

        row = cur.fetchone()
        domainID = str(row[0])

        # Check if alias user exists
        cur.execute("SELECT * FROM  `virtual_users` WHERE  `email` =  '" + userEmail + "'")
        if cur.rowcount > 0:
            print("User " + userEmail + " already exists! Bye!")
            return -1

        # Add alias on database
        cur.execute("INSERT INTO `" + dbName + "`.`virtual_users` (`id`, `domain_id`, `password` , `email`) VALUES ( NULL , '"
                    + domainID + "', ENCRYPT('" + userPassword + "', CONCAT('$6$', SUBSTRING(SHA(RAND()), -16))), '" + userEmail + "')")
        print("Email address " + userEmail + " added to database")

    # Create mail directory if not exists
    if not os.path.exists(mailBoxDirectory):
        # Create directory
        os.makedirs(mailBoxDirectory)
        # Set the user Id to mailUID and group ID to mailGID.
        os.chown( mailBoxDirectory, mailUID, mailGID)
        print("Mail box directory " + mailBoxDirectory + " created.")

    return 0
    
if __name__ == "__main__":
    # Check for root privileges
    if os.getuid() != 0:
        print("Sorry! You need to be root to run this script.")
        sys.exit(-1)

    # Parse command line arguments
    userEmail = ''
    userPassword = ''

    try:
        opts, args = getopt.getopt(sys.argv[1:],"he:p:",["email=","password="])
    except getopt.GetoptError:
        usage(sys.argv[0])
        sys.exit(-1)
    for opt, arg in opts:
        if opt == '-h':
            usage(sys.argv[0])
            sys.exit(0)
        elif opt in ("-e", "--email"):
            userEmail = arg.strip()
        elif opt in ("-p", "--password"):
            userPassword = arg.strip()

    if len(userEmail) == 0 or len(userPassword) == 0:
	usage(sys.argv[0])
        sys.exit(-1)

    result = addUser(userEmail, userPassword)
    
    sys.exit(result)
