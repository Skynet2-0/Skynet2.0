'''
Created on Apr 20, 2016

@author: Niels
'''
from random import randrange
import string
import random

class BogusFormBuilder(object):
    '''
    this class can be used to generate common values for registry forms on websites
    '''
    
    
    def __init__(self):
        pass
    
    def getPhoneNum(self):    
        '''
        returns a 10 sized phone number
        '''
        if hasattr(self, 'phoneNum'):
            return self.phoneNum
        
        self.phoneNum = self.getRNString(10)

        return self.phoneNum
    
    '''
    returns a random email adress. this email adress is bogus and cannot be accessed
    '''
    def getEmail(self):
        if hasattr(self, 'email'):
            return self.email
        
        tlds = [".com", ".co.uk", ".eu", ".ch", ".org"]
        
        self.email = self.getRAString(randrange(3,10))+"@"+self.getRAString(randrange(3,10))+tlds[randrange(0,len(tlds))]        
        return self.email
    
    def getFirstName(self):
        '''
        returns a bogus firstname
        '''
        if hasattr(self, 'firstName'):
            return self.firstName
        
        self.firstName = self.getRAString(randrange(3,10)) 
        return self.firstName
    
    def getSurname(self):
        'returns a bogus surname'
        if hasattr(self, 'surname'):
            return self.surname
        
        self.surname = self.getRAString(randrange(3,10)) 
        return self.surname
    
    def getCity(self):
        'returns a bogus city'
        if hasattr(self, 'city'):
            return self.city
        
        self.city = self.getRAString(randrange(3,10)) 
        return self.city
      
    def getZipcode(self):
        '''
        returns a american zipcode
        '''  
        if hasattr(self, 'zipcode'):
            return self.zipcode
        self.zipcode = self.getRNString(5)
        return self.zipcode
    
    def getPassword(self):
        'generates a password, do store it yourself'
        if hasattr(self, 'password'):
            return self.password
        self.password =  self.getRString(randrange(15,30))
        return self.password
           
    def getRAString(self, length):
        '''
        returns a random string with size length. contains just alphabetical characters
        ''' 
        result = ""
        for _ in range(0,length):
            result+=random.choice(string.ascii_letters)
        return result
    
    def getRNString(self, length):
        '''
        returns a random numerical string with size length.
        '''
        result = ""
        for _ in range(0,length):
            result+=random.choice(string.digits)
        return result
    
    def getRString(self, length):
        '''
        returns a random string with size length (numerical, alphabetical and some random other signs)
        '''
        result = ""
        for _ in range(0,length):
            result+=random.choice(string.printable)
        return result