#!/usr/bin/python
# -*- coding: utf-8 -*-
# Americo Dias - Jun 2014

import sys, os, getopt
import MySQLdb as mdb
from ConfigParser import SafeConfigParser

# Configuration file
configFile='config.ini'

def usage(scriptName):
    print scriptName, '-e email -p newpassword'

def changePassword(userEmail, password):
    # Define variables
    emailName=userEmail.split('@')[0]
    domainName=userEmail.split('@')[1]
    
    parser = SafeConfigParser()
    parser.read(configFile)
    dbHost = parser.get('database', 'host')
    dbUser = parser.get('database', 'user')
    dbPass = parser.get('database', 'password')
    dbName = parser.get('database', 'name')

    # Connect with database
    con = mdb.connect(dbHost, dbUser, dbPass, dbName)

    with con:
        cur = con.cursor()

        # Check if user exists
        cur.execute("SELECT * FROM  `virtual_users` WHERE  `email` =  '" + userEmail + "'")
        if cur.rowcount == 0:
            print("User " + userEmail + " not found! Bye!")
            return -1

        # Change password
        cur.execute("UPDATE `" + dbName + "`.`virtual_users` SET `password` = ENCRYPT('" + userPassword
                    + "', CONCAT('$6$', SUBSTRING(SHA(RAND()), -16))) WHERE `email` = '" + userEmail + "'")
        print("Email password for " + userEmail + " changed.")

    return 0
    
if __name__ == "__main__":
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

    result = changePassword(userEmail, userPassword)
    
    sys.exit(result)
