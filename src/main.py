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
    startTime = None; endTime = None

    #parse the arguments
    try:
        opts, args = getopt.getopt(argv[1:],
                                  "c:de:hs:o:V",
                                  ["config=", "debug","end=", "help", "start=",
                                   "output", "version"])
    except getopt.GetoptError:
        usage(argv)
        sys.exit(2)
    #Deal with the arguments
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage(argv)
            sys.exit()
        elif opt == ('-d', "--debug"):
            global _debug
            _debug = 1
        elif opt in ("-s", "--start"):
            startTime = arg
        elif opt in ("-e", "--end"):
            endTime = arg
        elif opt in ("-o", "--output"):
            outPut = arg
        elif opt in ("-c", "--config"):
            if arg == None:
                usage(argv)
                sys.exit(2)
            configFile = arg
            print("Sorry, config files are not supported yet!")
        elif opt in ("-V", "--version"):
            version()
            sys.exit()

    if len(args) != 1:
        usage(argv)
        sys.exit(2)
    else:
        host = args[0]

    if startTime == None: # Define the off-peak start time
        startTime = 0
    if endTime == None: # Define the off-peak start time
        endTime = 0 # Define the off-peak end time
    
    myTable = table.table()
    users = {}

    # Final program loop!
    while True:
        print("Currently updating data from router " + host)
        myTable.updateTable(host)

        # Check if we are currently on or off peak
        peak = 'on'
        curTime = datetime.time(time.localtime().tm_hour,time.localtime().tm_min)
        if curTime > datetime.time(startTime,0):
            if curTime < datetime.time(endTime,0):
                peak = 'off'

        while myTable.hasLines():
            line = myTable.getLine()
            
            if line["address"] not in users:
                users[line["address"]] = user.user()
            myUser = users[line["address"]]
            if line["upOrDown"] == "up":
                myUser.addUpData(data = line["bytes"], peak = peak)
            elif line["upOrDown"] == "down":
                myUser.addDownData(data = line["bytes"], peak = peak)
            else:
                print(line["bytes"] + " bytes lost from records")
    
        interface = webInterface.webInterface()
        interface.outputIndex('index.html', users)
        
        time.sleep(time.localtime(time.time())[3])

def version():
    print("v0.02")

def usage(argv):
    print(argv[0] + " [options] <host>")
    print("Monitor iptables data on the given host")
    print
    print("A <host> must either be an ip address or host name")
    print
    print("Mandatory arguments to long options are mandatory for short options too.")
    print("  -h    --help                     display this help and exit")
    print("  -d    --debug                    print debug information")
    print("  -c:   --config=File              where File is a config file")
    print("  -s:   --start=Time               off peak start time in format HHMM")
    print("  -e:   --end=Time                 off peak end time in format HHMM")
    print("Report touch bugs to henry@henryjenkins.name")

if __name__ == "__main__":
    main(sys.argv)
