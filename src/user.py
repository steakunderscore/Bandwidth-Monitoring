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

    def getData(self, type, date=None, peak='other'):
        '''
        Method to retrieve data for either a set date, or the total data used by user
        
        Return int, data used by this user
        '''
        data = 0
        if date == None:
            data = user.__getTotalData(self, type, peak)
        else:
            data = self.getDownData(type = type, date = date, peak = peak)
            date += self.getUpData(type = type, date = date, peak = peak)

        return data

    def __getTotalData(self, type, peak='other'):
        totalData = self.__getTotalUpData(type, peak)
        totalData = totalData + self.__getTotalDownData(peak = peak, type = type)
        return totalData

    def getUpData(self, type, date=None, peak='other'):
        data = 0
        if date == None:
            data = self.__getTotalUpData(type = type, peak = peak)
        elif date in self.dataUp:
            if type == 'on' or type == 'off':
                    data = self.dataUp[date][peak][type]
            else:
                    data = self.dataUp[date]['on'][type] + self.dataUp[date]['off'][type]

        return data

    def __getTotalUpData(self, type, peak='other'):
        dataTotal = 0

        for date, data in self.dataUp.items():
            if peak == 'on' or peak == 'off':
                dataTotal += data[peak][type]
            else:
                dataTotal += data['on'][type]
                dataTotal += data['off'][type]

        return dataTotal

    def getDownData(self, type, date=None, peak='other'):
        data = 0

        if date == None:
            data = self.__getTotalDownData(type = type, peak = peak)
        elif date in self.dataDown:
            if type == 'on' or type == 'off':
                data = self.dataDown[date][peak][type]
            else:
                data = self.dataDown[date]['on'][type] + self.dataDown[date]['off'][type]

        return data

    def __getTotalDownData(self, type, peak='other'):
        dataTotal = 0

        for date, data in self.dataDown.items():
            if peak == 'on' or peak == 'off':
                dataTotal += data[peak][type]
            else:
                dataTotal += data['on'][type]
                dataTotal += data['off'][type]

        return dataTotal

    def addData(self, date=None, data=0, pkts=0, peak='on', direction='up'):
        if direction == 'up':
            self.addUpData(date, data, pkts, peak)
        elif direction == 'down':
            self.addDownData(date, data, pkts, peak)

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

    '''
    Helper method
    '''
    def __checkDate(self, localDate=None):
        if localDate == None:
            localDate = datetime.date.today()
        return localDate
        
    def setMac(self, mac=None):
        self.macAddress = mac
    
    def setName(self, name=None):
        self.name = name    
