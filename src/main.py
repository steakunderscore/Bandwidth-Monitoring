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



if __name__ == '__main__':
    STARTTIME = 01 # Define the off-peak start time
    ENDTIME = 07 # Define the off-peak end time
    
    myTable = table.table()
    users = {}

    # Final program loop!
    while True:
        print("Currently updating data from router")
        myTable.updateTable()

        # Check if we are currnetly on or off peak
        peak = 'on'
        curTime = datetime.time(time.localtime().tm_hour,time.localtime().tm_min)
        if curTime > datetime.time(STARTTIME,0):
            if curTime < datetime.time(ENDTIME,0):
                peak = 'off'

        while myTable.hasLines():
            line = myTable.getLine()
            
            if line["address"] not in users:
                users[line["address"]] = user.user()
            myUser = users[line["address"]]
            myUser.addData(data = line["bytes"], peak = peak, direction = line["upOrDown"])

        interface = webInterface.webInterface()
        interface.outputIndex('index.html', users)
        
        time.sleep(time.localtime(time.time())[3])
