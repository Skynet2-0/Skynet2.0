'''
Created on Apr 20, 2016

@author: Niels
'''
from random import randrange
import string
import random

class bogusFormBuilder(object):
    '''
    this class can be used to generate common values for registry forms on websites
    '''
    def __init__(self):
        pass
        
    '''
    returns a 10 sized phone number
    '''
    def genPhoneNum(self):
        result = ""
        for _ in range(0,10):
            result+=randrange(0,9)
        return result
    
    '''
    returns a random email adress. this email adress is bogus and cannot be accessed
    '''
    def getEmail(self):
        tlds = [".com", ".co.uk", ".eu", ".ch", ".org"]
        return self.getRAString(randrange(3,10))+"@"+self.getRAString(randrange(3,10))+tlds[randrange(0,len(tlds))]
    
    '''
    returns a bogus firstname
    '''
    def getFirstName(self):
        return self.getRAString(randrange(3,10))
    
    'returns a bogus surname'
    def getSurname(self):
        return self.getRAString(randrange(3,10))
    
    'returns a bogus city'
    def getCity(self):
        return self.getRAString(randrange(3,10))
    
    '''
    returns a american zipcode
    '''    
    def getZipcode(self):
        return self.getRNString(5)
    
    'generates a password, do store it yourself'
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
    
    '''
    returns a random numerical string with size length.
    '''
    def getRNString(self, length):
        result = ""
        for _ in range(0,length):
            result+=random.choice(string.digits)
        return result
    
    '''
    returns a random string with size length (numerical, alphabetical and some random other signs)
    '''
    def getRString(self, length):
        result = ""
        for _ in range(0,length):
            result+=random.choice(string.printable)
        return result