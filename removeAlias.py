#!/usr/bin/python
# -*- coding: utf-8 -*-
# Americo Dias - Jun 2014

import sys, os, getopt
import MySQLdb as mdb
from ConfigParser import SafeConfigParser

# Configuration file
configFile='config.ini'

def usage(scriptName):
    print scriptName, '-s source'

def removeAlias(sourceEmail):
    # Define variables
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
        # Check if alias already exists
        cur.execute("SELECT * FROM  `virtual_aliases` WHERE  `source` =  '" + sourceEmail + "'")
        if cur.rowcount == 0:
            print("Alias for " + sourceEmail + " was not found on database! Bye!")
            return -1
        else:
            # Remove alias from database
            cur.execute("DELETE FROM `"+dbName+"`.`virtual_aliases` WHERE `virtual_aliases`.`source` = '"+sourceEmail+"'")
            print("Alias for " + sourceEmail + " deleted!")

    return 0
    
if __name__ == "__main__":
    # Parse command line arguments
    sourceEmail = ''

    try:
        opts, args = getopt.getopt(sys.argv[1:],"hs:",["source="])
    except getopt.GetoptError:
        usage(sys.argv[0])
        sys.exit(-1)
    for opt, arg in opts:
        if opt == '-h':
            usage(sys.argv[0])
            sys.exit(0)
        elif opt in ("-s", "--source"):
            sourceEmail = arg.strip()

    if len(sourceEmail) == 0:
	usage(sys.argv[0])
        sys.exit(-1)
        
    result = removeAlias(sourceEmail)
    
    sys.exit(result)
    

