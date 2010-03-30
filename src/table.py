'''
Created on 4/02/2010

@author: henry
'''

import os
import subprocess
import tempfile

class table(object):
    '''
    classdocs
    '''
    tableRawLines = None
    tableLines = None

    def __init__(self, textFile=None):
        self.tableRawLines = []
        self.tableLines = []
        
    def updateTable(self, textFile=None):
        if textFile == None:
            textFile = table.__updatefile(self)
        table.__parsTable(self, textFile)
        table.__cleanTableLines(self)
        table.__cleanTableRows(self)
            
    def __updatefile(self,host="bawls.grr", table="filter",chain="act"):
        command = "ssh root@" + host + " iptables -v -x -Z -n -L " + chain + " -t " + table                                                       
        process = subprocess.Popen(command,stdout=subprocess.PIPE,shell=True)
        os.waitpid(process.pid, 0)
        myFile = tempfile.mktemp()
        myWriteFile = open(myFile, 'w')
        myWriteFile.write(process.stdout.read())
        myWriteFile.close()
        return myFile

    def __parsTable(self, testFile):
        openFile = open(testFile, 'r')
        for line in openFile: 
            table.__parsLine(self, line)
            
    def __parsLine(self, aLine=""):
        myLineAry = aLine.split()
        if len(myLineAry) == 9:
            self.tableRawLines.append(myLineAry)

    def __cleanTableLines(self):
        tableLen = len(self.tableRawLines)
        curLine = 0
        while curLine < tableLen:
            if self.tableRawLines[curLine][0] == '0':
                self.tableRawLines.remove(self.tableRawLines[curLine])
                tableLen = tableLen - 1
            elif self.tableRawLines[curLine][0] == "pkts":
                self.tableRawLines.remove(self.tableRawLines[curLine])
                tableLen = tableLen - 1
            else:
                curLine = curLine + 1
                
    def __cleanTableRow(self, tableRow):
        if len(tableRow) != 9:
            return None
        pkts = tableRow[0]
        bytes = tableRow[1]
        
        if table.__internalAddress(self, tableRow[7]):
            upOrDown = 'up'
            address = tableRow[7]
        elif table.__internalAddress(self, tableRow[8]):
            upOrDown = 'down'
            address = tableRow[8]
        else:
            upOrDown = 'other'
            address = tableRow[8]
                
        return { "pkts":pkts, "bytes":bytes, "address":address, "upOrDown":upOrDown }
   
    def __cleanTableRows(self):
        while len(self.tableRawLines) > 0:
            cleanRow = table.__cleanTableRow(self, self.tableRawLines.pop())
            self.tableLines.append(cleanRow)

    def __internalAddress(self, address=None):
        splitAddress = address.split(".")
        if len(splitAddress) != 4:
            return False
        elif splitAddress[0] == "192" and splitAddress[1] == "168":
            return True
        else:
            return False

    def hasLines(self):
        if len(self.tableLines) > 0:
            return True
        else:
            return False

    def getLine(self):
        if table.hasLines(self):
            return self.tableLines.pop()
        else:
            return None
    
