'''
Created on 11/02/2010

@author: henry@henryjenkins.name
'''

class webInterface(object):
    '''
    classdocs
    '''
    writeFile = None

    def __init__(self):
        pass
        
    def __openFile(self, fileName):
        self.writeFile = open(fileName, 'w')
        
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
        self.writeFile.write('<td>On-peak Upload data</td>')
        self.writeFile.write('<td>Off-peak Upload data</td>')
        self.writeFile.write('<td>On-peak Downlaod data</td>')
        self.writeFile.write('<td>Off-peak Downlaod data</td>')
        self.writeFile.write('<td>Total data</td>')
        self.writeFile.write('</tr>')
        
        usersList = users.keys()
        usersList.sort()
        for user in usersList:
            self.writeFile.write('<tr>')
            self.writeFile.write('<td>' + user + '</td>')
            self.writeFile.write('<td>' + self.humanizeNumber(users[user].getUpData(date=None, peak='on')) + '</td>')
            self.writeFile.write('<td>' + self.humanizeNumber(users[user].getUpData(date=None, peak='off')) + '</td>')
            self.writeFile.write('<td>' + self.humanizeNumber(users[user].getDownData(date=None, peak='on')) + '</td>')
            self.writeFile.write('<td>' + self.humanizeNumber(users[user].getDownData(date=None, peak='off')) + '</td>')
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
        
    def outputIndex(self,file,users = None):
        self.__openFile(file)
        self.writeHeader()
        self.writeBody(users)
        self.writeFooter()
        self.closeFile()