#!/usr/bin/python
# -*- coding: utf-8 -*-
# Americo Dias - Jun 2014

import sys, os, getopt
import MySQLdb as mdb
from ConfigParser import SafeConfigParser

# Configuration file
configFile='config.ini'

def usage(scriptName):
    print scriptName, '-d domain'

def addDomain(domainName):
    # Define variables
    parser = SafeConfigParser()
    parser.read(configFile)
    dbHost = parser.get('database', 'host')
    dbUser = parser.get('database', 'user')
    dbPass = parser.get('database', 'password')
    dbName = parser.get('database', 'name')

    mailDirectory = parser.get('disk', 'vhostdir') + '/' + domainName
    mailUID = int(parser.get('disk', 'uid'))
    mailGID = int(parser.get('disk', 'gid'))
        
    # Connect with database
    con = mdb.connect(dbHost, dbUser, dbPass, dbName);

    with con:
        # Check if domain already exists
        cur = con.cursor()
        cur.execute("SELECT * FROM  `virtual_domains` WHERE  `name` =  '" + domainName + "'")
	
        if cur.rowcount > 0:
            print("Domain " + domainName + " already exists. Bye bye!")
            return -1

        # Add domain on database
        cur.execute("INSERT INTO `" + dbName + "`.`virtual_domains` (`id`, `name`) VALUES (NULL, '" + domainName + "')")
        print("Domain " + domainName + " added to database.")

        # Create mail directory if not exists
        if not os.path.exists(mailDirectory):
            # Create directory
            os.makedirs(mailDirectory)
            # Set the user Id to mailUID and group ID to mailGID.
            os.chown( mailDirectory, mailUID, mailGID)

            print("Mail directory " + mailDirectory + " created.")

    return 0
    
if __name__ == "__main__":
    # Check for root privileges
    if os.getuid() != 0:
        print("Sorry! You need to be root to run this script.")
        sys.exit(-1)

    # Parse command line arguments
    domainName = ''

    try:
        opts, args = getopt.getopt(sys.argv[1:],"hd:",["domain="])
    except getopt.GetoptError:
        usage(sys.argv[0])
        sys.exit(-1)
    for opt, arg in opts:
        if opt == '-h':
            usage(sys.argv[0])
            sys.exit(0)
        elif opt in ("-d", "--domain"):
            domainName = arg.strip()

    if len(domainName) == 0:
	usage(sys.argv[0])
        sys.exit(-1)

    result = addDomain(domainName)

    sys.exit(result)
