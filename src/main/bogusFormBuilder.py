'''
Created on Apr 20, 2016

@author: Niels
'''
from random import randrange
import string
import random

class bogusFormBuilder(object):
    '''
    classdocs
    '''
    def __init__(self):
        pass
        
    def genPhoneNum(self):
        result = ""
        for _ in range(0,10):
            result+=randrange(0,9)
        return result
    
    def getEmail(self):
        tlds = [".com", ".co.uk", ".eu", ".ch", ".org"]
        
        return self.getRAString(randrange(3,10))+"@"+self.getRAString(randrange(3,10))+tlds[randrange(0,len(tlds))]
    
    def getFirstName(self):
        return self.getRAString(randrange(3,10))
    
    def getSurname(self):
        return self.getRAString(randrange(3,10))
        
    def getCity(self):
        return self.getRAString(randrange(3,10))
        
    def getZipcode(self):
        return self.getRNString(5)
    
    def getPassword(self):
        return self.getRString(randrange(15,30))
        
    '''
    returns a random string with size length. contains just alphabetical characters
    '''    
    def getRAString(self, length):
        result = ""
        for _ in range(0,length):
            result+=random.choice(string.ascii_letters)
        return result
    
    def getRNString(self, length):
        result = ""
        for _ in range(0,length):
            result+=random.choice(string.digits)
        return result
    
    def getRString(self, length):
        result = ""
        for _ in range(0,length):
            result+=random.choice(string.printable)
        return result