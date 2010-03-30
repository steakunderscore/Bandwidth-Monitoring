'''
Created on 4/02/2010

@author: henry
'''
import table
import user
import time
import webInterface



if __name__ == '__main__':
    myTable = table.table()
    users = {}

    # Final program loop!
    while True:
        print("Loop is running")
        myTable.updateTable()

        while myTable.hasLines():
            line = myTable.getLine()
    
            if line["address"] not in users:
                users[line["address"]] = user.user()
            myUser = users[line["address"]]
            if line["upOrDown"] == "up":
                myUser.addUpData(data = line["bytes"])
            elif line["upOrDown"] == "down":
                myUser.addDownData(data = line["bytes"])
            else:
                print(line["bytes"] + " bytes lost from records")
    
        print("Loop has run")
        interface = webInterface.webInterface()
        interface.outputIndex('index.html', users)
        
        time.sleep(time.localtime(time.time())[3])
