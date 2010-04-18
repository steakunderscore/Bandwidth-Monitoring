#!/usr/bin/python
'''
Created on 4/02/2010

@author: henry@henryjenkins.name
'''
import table
import user
import time
import webInterface
import datetime
import sys
import getopt

def main(argv):
    startTime = None; endTime = None; outPut = None; configFile = None
    global _debug
    _debug = None;
    #parse the arguments
    try:
        opts, args = getopt.getopt(argv[1:],
                                  "c:de:hs:o:V",
                                  ["config=", "debug","end=", "help", "start=",
                                   "output", "version"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    #Deal with the arguments
    for opt, arg in opts:
        if   opt in ("-h",   "--help"):
            usage()
            sys.exit()
        elif opt in ('-d',  "--debug"):
            _debug = 1
        elif opt in ("-s",  "--start"):
            startTime = makeInt(arg)
        elif opt in ("-e",    "--end"):
            endTime = makeInt(arg)
        elif opt in ("-o", "--output"):
            outPut = arg
        elif opt in ("-c", "--config"):
            configFile = arg
            print("Sorry, config files are not supported yet!")
            sys.exit(2)
        elif opt in ("-V", "--version"):
            version()
            sys.exit()

    if configFile != None: # Deal with config file.
        pass
    elif len(args) != 1: # the host must be defined in the args
        usage()
        sys.exit(2)
    else:
        host = args[0]

    if startTime == None: # Define the off-peak start time
        startTime = 0 # TODO: Think about what these defaults should be
    if endTime   == None: # Define the off-peak end time
        endTime   = 0
    if outPut    == None:
        outPut    = "../www/index.html"
    
    myTable = table.table()
    users = {}
    interface = webInterface.webInterface()
    # Final program loop!
    while True:
        print("Currently updating data from router " + host)
        myTable.updateTable(host)
        if _debug == 1 : print("DEBUG: updated table")
        # Check if we are currently on or off peak

        curTime = datetime.time(time.localtime().tm_hour,time.localtime().tm_min)
        if  curTime > datetime.time(startTime,0) \
        and curTime < datetime.time(endTime  ,0):
                peak = 'off'
        else:
            peak = 'on'

        while myTable.hasLines():
            line = myTable.getLine()
            
            if line["address"] not in users:
                users[line["address"]] = user.user()
            myUser = users[line["address"]]
            myUser.addData(data = line["bytes"], pkts = line["pkts"],
                           peak = peak, direction = line["upOrDown"])

        interface.outputIndex(outPut, users)
        
        time.sleep(time.localtime(time.time())[3])

def makeInt(value):
    try:
        return int(value)
    except:
        print("An incorrect value was passed in. Aborting!")
        print
        usage()
        sys.exit(2)

def version():
    print("Bandwidth-Monitoring v0.02")
    print("Copyright (C) 2010 Henry Jenkins")
    print("License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>.")
    print("This is free software: you are free to change and redistribute it.")
    print("There is NO WARRANTY, to the extent permitted by law.")
    print
    print("Written by Henry Jenkins")


def usage():
    print("Usage: " + sys.argv[0] + " [options] <host>")
    print
    print("A <host> must either be an ip address or host name")
    print
    print("Mandatory arguments to long options are mandatory for short options too")
    print("  -h    --help                     display this help and exit")
    print("  -d    --debug                    print debug information")
    print("  -c:   --config=File              where File is a config file")
    print("  -s:   --start=Time               off peak start time in format HHMM")
    print("  -e:   --end=Time                 off peak end time in format HHMM")
    print("Report bugs to henry@henryjenkins.name")

if __name__ == "__main__":
    main(sys.argv)
