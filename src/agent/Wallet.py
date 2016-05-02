'''
Created on Apr 26, 2016

@author: niels
'''
from subprocess import PIPE, STDOUT
import subprocess
import re
import os
import time
import sys
import pexpect

class Wallet(object):
    '''
    classdocs
    
    This class will manage the bitcoins going in and out off the agent.
    '''

    def __init__(self):
        '''
        Constructor
        '''
        
        output = pexpect.run('electrum listaddresses').decode('ascii')
        print(output)
        pattern = re.compile(r"[A-z0-9]+") #the specific output for electrum if 1 adress exists
        
        print(pattern.search(output))#r"\[\n    \"([A-z0-9]+)\"\n\]\n", output))
        
        if(pattern.search(output)):
            #if a wallet exists, initialize that one
            pass
        else:
            #build a new wallet if no wallet yet exists
        
            walletpair=str(subprocess.check_output('sh ~/Skynet2.0/getaddr.sh',shell=True))
            walletpair = re.split('\W+', walletpair)
        
            self.address = walletpair[1]
            self.privkey = walletpair[2]
        
            print('created a wallet with address \''+self.address+'\' and privatekey \''+self.privkey+'\'')
        
            child = pexpect.spawn('electrum', ['restore', self.privkey])
        
            #wait for the password prompt, then ignore it 
            child.waitnoecho()
            child.sendline('')
            child.expect(pexpect.EOF)
        subprocess.call(['electrum', 'daemon', 'start'])
    
   # def __del__(self):
   #     '''
   #     clear up the electrum service
   #     '''
   #     subprocess.call(['electrum', 'daemon', 'stop'])
    
    def balance(self):
        '''
        Return the balance of the Btc wallet
        '''
        return float('inf')
    
    def payTo(self, address, fee, amount):
        '''
        If funds allow, transfer amount in Btc to Address. With a fee for processor
        '''
        if float(amount)+float(fee)<=self.balance():
            #child = pexpect.spawn('electrum payto -f ' + fee + ' ' + address + ' '+ amount)
            #child.expect(pexpect.EOF)
            print(str(subprocess.call(['electrum', 'payto', '-f', fee, address, amount])))