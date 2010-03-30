'''
Created on 11/02/2010

@author: henry
'''
import tempfile
import io

class webInterface(object):
    '''
    classdocs
    '''
    writeFile = None

    def __init__(self):
        pass
        
    def openFile(self, fileName = "index.html"):
        self.writeFile = open('../www/' + fileName, 'w')
        
    def closeFile(self):
        self.writeFile.close()

    def writeHeader(self, title = 'Henry\'s iptables data accounting'):
        self.writeFile.write('<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">\n')
        self.writeFile.write('<HTML>\n')
        self.writeFile.write('<HEAD>\n')
        self.writeFile.write('<TITLE>' + title + '</TITLE>\n')
        self.writeFile.write('</HEAD>\n')
        
    def writeBody(self, users):
        self.writeFile.write('<BODY>\n')
        self.writeFile.write('<table border="1">')

        self.writeFile.write('<tr>')
        self.writeFile.write('<td>IP address</td>')
        self.writeFile.write('<td>Total Upload data</td>')
        self.writeFile.write('<td>Total Downlaod data</td>')
        self.writeFile.write('<td>Total data</td>')
        self.writeFile.write('</tr>')
        
        usersList = users.keys()
        usersList.sort()
        for user in usersList:
            self.writeFile.write('<tr>')
            self.writeFile.write('<td>' + user + '</td>')
            self.writeFile.write('<td>' + self.humanizeNumber(users[user].getUpData()) + '</td>')
            self.writeFile.write('<td>' + self.humanizeNumber(users[user].getDownData()) + '</td>')
            self.writeFile.write('<td>' + self.humanizeNumber(users[user].getData()) + '</td>')
            self.writeFile.write('</tr>')
            
        self.writeFile.write('</table>') 
        self.writeFile.write('</BODY>\n')
    
    def writeFooter(self):
        self.writeFile.write('</HTML>\n')
        
    def humanizeNumber(self,number = 0):
        if number > 1024*1024*1024:
            number = number/(1024*1024*1024)
            number = str(number) + ' GBytes'
        elif number > 1024*1024:
            number = number/(1024*1024)
            number = str(number) + ' MBytes'
        elif number > 1024:
            number = number/1024
            number = str(number) + ' KBytes'
        else:
            number = str(number) + ' Bytes'
        return number
        
    def outputIndex(self,file = 'index.html',users = None):
        self.openFile(file)
        self.writeHeader()
        self.writeBody(users)
        self.writeFooter()
        self.closeFile()