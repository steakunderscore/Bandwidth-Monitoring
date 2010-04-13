'''
Created on 5/02/2010

@author: henry@henryjenkins.name
'''

import datetime

class user(object):
    '''
    classdocs
    '''
    dataUp = None
    dataDown = None
    macAddress = ""
    name = ""

    def __init__(self, mac="", name=""):
        '''
        Constructor
        '''
        self.name = name
        self.dataUp = {}
        self.dataDown = {}
        self.macAddress = mac

    def getData(self, date=None, peak='on'):
        '''
        Method to retreve data for either a set date, or the total data used by user
        
        Return int, data used by this user
        '''
        if date == None:
            return user.__getTotalData(self, peak)
        elif date in self.dataUp:
            return self.dataUp[date]['data']
        else:
            return 0
           
    def __getTotalData(self, peak='on'):
        totalData = self.__getTotalUpData(peak)
        totalData = totalData + self.__getTotalDownData(peak)
        return totalData
    
    def getUpData(self, date=None, peak='on'):
        if date == None:
            return self.__getTotalUpData(peak)
        elif date in self.dataUp:
            return self.dataUp[date][peak]['data']
        else:
            return 0
        
    def __getTotalUpData(self, peak='on'):
        dataTotal = 0
        for date, data in self.dataUp.items():
            dataTotal += data[peak]['data']
        return dataTotal
    
    def getDownData(self, date=None, peak='on'):
        if date == None:
            return self.__getTotalDownData(peak)
        elif date in self.dataDown:
            return self.dataDown[date][peak]['data']
        else:
            return 0
        
    def __getTotalDownData(self, peak='on'):
        dataTotal = 0
        for date, data in self.dataDown.items():
            dataTotal += data[peak]['data']
        return dataTotal
     
    def addUpData(self, date=None, data=0, pkts=0, peak='on'): #TODO store packets
        date = self.__checkDate(date)
        if date not in self.dataUp:# Check if data for date already
            self.dataUp[date] = {
                                 'on': {'data': 0, 'pkts': 0}, 
                                 'off': {'data': 0, 'pkts': 0}
                                 }
        
        self.dataUp[date][peak]['data'] += int(data)
        self.dataUp[date][peak]['pkts'] += int(pkts)
    
    def addDownData(self, date=None, data=0, pkts=0, peak='on'): #TODO store packets
        date = self.__checkDate(date)
        if date not in self.dataDown:# Check if data for date already
            self.dataDown[date] = {
                                   'on': {'data': 0, 'pkts': 0}, 
                                   'off': {'data': 0, 'pkts': 0}
                                   }
        
        self.dataDown[date][peak]['data'] += int(data)
        self.dataDown[date][peak]['pkts'] += int(pkts)

    def __checkDate(self, localDate=None):
        if localDate == None:
            localDate = datetime.date.today()
        return localDate
        
    def setMac(self, mac=None):
        self.macAddress = mac
    
    def setName(self, name=None):
        self.name = name    
