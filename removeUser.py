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
    print scriptName, '-e email'

def deleteDirectory(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)
        return 1
    
    return 0
        
def removeUser(userEmail):
    # Define variables
    parser = SafeConfigParser()
    parser.read(configFile)
    dbHost = parser.get('database', 'host')
    dbUser = parser.get('database', 'user')
    dbPass = parser.get('database', 'password')
    dbName = parser.get('database', 'name')

    domainName=userEmail.split('@')[1]
    emailName=userEmail.split('@')[0]
    mailBoxDirectory = parser.get('disk', 'vhostdir') + '/' + domainName + '/' + emailName

    # Connect with database
    con = mdb.connect(dbHost, dbUser, dbPass, dbName)

    with con:
        cur = con.cursor()
        # Check if alias already exists
        cur.execute("SELECT * FROM  `virtual_users` WHERE  `email` =  '" + userEmail + "'")
        if cur.rowcount == 0:
            print("Email address " + userEmail + " was not found on database!")
            if deleteDirectory(mailBoxDirectory):
                print("Mail box directory " + mailBoxDirectory + " deleted.")
            return -1
        else:
            # Remove alias on database
            cur.execute("DELETE FROM `" + dbName + "`.`virtual_users` WHERE `virtual_users`.`email` = '" + userEmail + "'")
            print("Email address " + userEmail + " removed from database!")

    # Delete directory
    if deleteDirectory(mailBoxDirectory):
        print("Mail box directory " + mailBoxDirectory + " deleted.")
        
    return 0

if __name__ == "__main__":
    # Check for root privileges
    if os.getuid() != 0:
        print("Sorry! You need to be root to run this script.")
        sys.exit(-1)

    # Parse command line arguments
    userEmail = ''

    try:
        opts, args = getopt.getopt(sys.argv[1:],"he:",["email="])
    except getopt.GetoptError:
        usage(sys.argv[0])
        sys.exit(-1)
    for opt, arg in opts:
        if opt == '-h':
            usage(sys.argv[0])
            sys.exit(0)
        elif opt in ("-e", "--email"):
            userEmail = arg.strip()

    if len(userEmail) == 0:
	usage(sys.argv[0])
        sys.exit(-1)

    result = removeUser(userEmail)
    
    sys.exit(result)
