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
    myTable = table.table()
    users = {}

    # Final program loop!
    while True:
        print("Loop is running")
        myTable.updateTable()

        while myTable.hasLines():
            line = myTable.getLine()
            
            peak = 'on'

            curTime = datetime.time(time.localtime().tm_hour,time.localtime().tm_min)
            
            if curTime > datetime.time(1,0):
                print( "It's after 1am")
                if curTime < datetime.time(7,0):
                    print("And it's before 7am")
            #        peak = 'off'
                else:
                    print("But it's after 7am too.")
            
            if line["address"] not in users:
                users[line["address"]] = user.user()
            myUser = users[line["address"]]
            if line["upOrDown"] == "up":
                myUser.addUpData(data = line["bytes"], peak = peak)
            elif line["upOrDown"] == "down":
                myUser.addDownData(data = line["bytes"], peak = peak)
            else:
                print(line["bytes"] + " bytes lost from records")
    
        print("Loop has run")
        interface = webInterface.webInterface()
        interface.outputIndex('index.html', users)
        
        time.sleep(time.localtime(time.time())[3])
