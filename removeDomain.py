#!/usr/bin/python
# -*- coding: utf-8 -*-
# Americo Dias - Jun 2014

import sys, os, getopt
import MySQLdb as mdb
import shutil
from ConfigParser import SafeConfigParser

# Configuration file
configFile='config.ini'

def usage(scriptName):
    print scriptName, '-d domain'

def removeDomain(domainName):
    # Define variables
    parser = SafeConfigParser()
    parser.read(configFile)
    dbHost = parser.get('database', 'host')
    dbUser = parser.get('database', 'user')
    dbPass = parser.get('database', 'password')
    dbName = parser.get('database', 'name')

    mailDirectory = parser.get('disk', 'vhostdir') + '/' + domainName

    # Connect with database
    con = mdb.connect(dbHost, dbUser, dbPass, dbName);

    with con:
        # Check if domain already exists
        cur = con.cursor()
        cur.execute("SELECT * FROM  `virtual_domains` WHERE  `name` =  '" + domainName + "'")
	
        if cur.rowcount == 0:
            print("Domain " + domainName + " does not exist.")
        else:
            row = cur.fetchone()
            domainID = str(row[0])

            # Get the number of users for this domain
            cur.execute("SELECT * FROM  `virtual_users` WHERE  `domain_id` =  '" + domainID + "'")
            usersCount = cur.rowcount

            # Get the number of alias for this domain
            cur.execute("SELECT * FROM  `virtual_aliases` WHERE  `domain_id` =  '" + domainID + "'")
            aliasesCount = cur.rowcount

            # Exit if there are users or aliases for this domain
            if usersCount > 0 and aliasesCount > 0:
                print("There are " + str(usersCount) + " users and " + str(aliasesCount) + " aliases for this domain.")
                print("Please delete them first! Bye!")
                return -1
            elif usersCount > 0:
                print("There are " + str(usersCount) + " users for this domain.")
                print("Please delete them first! Bye!")
                return -1
            elif aliasesCount > 0:
                print("There are " + str(aliasesCount) + " aliases for this domain.")
                print("Please delete them first! Bye!")
                return -1

            # Remove domain on database        
            cur.execute("DELETE FROM `" + dbName + "`.`virtual_domains` WHERE `virtual_domains`.`name` = '" + domainName + "'")
            print("Domain " + domainName + " removed from database.")

        # Delete directory
	if os.path.exists(mailDirectory):
            shutil.rmtree(mailDirectory)
            print("Mail directory " + mailDirectory + " removed.")

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

    result = removeDomain(domainName)
    
    sys.exit(result)

