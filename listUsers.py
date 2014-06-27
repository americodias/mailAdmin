#!/usr/bin/python
# -*- coding: utf-8 -*-
# Americo Dias - Jun 2014

import sys
import MySQLdb as mdb
import texttable as tt
from ConfigParser import SafeConfigParser

# Configuration file
configFile='config.ini'

def lisUsers():
    parser = SafeConfigParser()
    parser.read(configFile)
    dbHost = parser.get('database', 'host')
    dbUser = parser.get('database', 'user')
    dbPass = parser.get('database', 'password')
    dbName = parser.get('database', 'name')
    tab = tt.Texttable()
    header = ['ID', 'Domain ID', 'Email address']
    tab.header(header)

    # Connect with database
    con = mdb.connect(dbHost, dbUser, dbPass, dbName)
    
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM virtual_users")

        for i in range(cur.rowcount):
        
            row = cur.fetchone()
            tab.add_row([row[0], row[1], row[3]])

    print tab.draw()

if __name__ == "__main__":
    lisUsers()
    sys.exit(0)
    
