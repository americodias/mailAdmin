#!/usr/bin/python
# -*- coding: utf-8 -*-
# Americo Dias - Jun 2014

import sys, os, getopt
import MySQLdb as mdb
from ConfigParser import SafeConfigParser

# Configuration file
configFile='config.ini'

def usage(scriptName):
    print scriptName, '-s source -d destination'

def addAlias(sourceEmail, destinationEmail):
    # Define variables
    domainName = sourceEmail.split('@')[1]
    parser = SafeConfigParser()
    parser.read(configFile)
    dbHost = parser.get('database', 'host')
    dbUser = parser.get('database', 'user')
    dbPass = parser.get('database', 'password')
    dbName = parser.get('database', 'name')

    # Connect with database
    con = mdb.connect(dbHost, dbUser, dbPass, dbName);

    with con:
        # Check if domain exists
        cur = con.cursor()
        cur.execute("SELECT * FROM  `virtual_domains` WHERE  `name` =  '" + domainName + "'")
	
        if cur.rowcount == 0:
            print("Domain " + domainName + " does not exist. Alias not created! Bye!")
            return -1

        row = cur.fetchone()
        domainID = str(row[0])

        # Check if alias already exists
        cur.execute("SELECT * FROM  `virtual_aliases` WHERE  `source` =  '" + sourceEmail + "'")
        if cur.rowcount > 0:
            print("Alias for " + sourceEmail + " already exists! Bye!")
            return -1

        # Add alias on database
        cur.execute("INSERT INTO  `" + dbName + "`.`virtual_aliases` (`id` , `domain_id` , `source` , `destination`) VALUES ( NULL ,  '"
                    + domainID + "',  '" + sourceEmail + "',  '" + destinationEmail + "')")
        print("Email address " + sourceEmail + " is now an alias of " + destinationEmail)
        
    return 0

if __name__ == "__main__":
    # Parse command line arguments
    sourceEmail = ''
    destinationEmail = ''

    try:
        opts, args = getopt.getopt(sys.argv[1:],"hs:d:",["source=","destination="])
    except getopt.GetoptError:
        usage(sys.argv[0])
        sys.exit(-1)
    for opt, arg in opts:
        if opt == '-h':
            usage(sys.argv[0])
            sys.exit(0)
        elif opt in ("-s", "--source"):
            sourceEmail = arg.strip()
        elif opt in ("-d", "--destination"):
            destinationEmail = arg.strip()

    if len(sourceEmail) == 0 or len(destinationEmail) == 0:
	usage(sys.argv[0])
        sys.exit(-1)
        
    result = addAlias(sourceEmail, destinationEmail)

    sys.exit(result)
