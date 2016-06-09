#!/usr/bin/python

from agent.Birthchamber import Birthchamber
from agent.DNA import DNA
from agent.Settings import Settings
from agent.VPSBuyer import VPSBuyer
from ssh.SSH import SSH
import os
import re
import time

s = Settings()

#this part works for this version, and since this script is just for doing integration it should be fine
#i still need to write a dummy vpsbuyer that simply takes these values
v = VPSBuyer()
v.SSHUsername = s.get_test_server_ssh_username()
v.SSHPassword = s.get_test_server_ssh_password()
v.IP = s.get_test_server_ip()

print("preparing to run agentcore on the following server:")
print(v.SSHUsername)
print(v.SSHPassword)
print(v.IP)


bc = Birthchamber()
bc.vps = v

print("starting the installation procedure")
ssh = SSH(v.getIP(),v.getSSHUsername(),v.getSSHPassword(),22)

#bc.installChild()



def prepChild(ssh):
    print('Start prepping child.')
    (_, out0, err0) = ssh.run('apt-get update')
    ssh._checkStreams(out0, err0, 'apt update failed', 'apt updated.')
    (_, out0, err0) = ssh.run('apt-get install -y --force-yes git')
    ssh._checkStreams(out0, err0, 'git install failed', 'git installed.')
    
    command = """git clone --recursive https://github.com/Skynet2-0/Skynet2.0.git"""
    (_, out0, err0) = ssh.run(command)
    ssh._checkStreams(out0, err0, 'git clone failed', 'project cloned.')
    
    command = """cd ~/Skynet2.0 && git checkout prototype2"""
    (_, out0, err0) = ssh.run(command)
    ssh._checkStreams(out0, err0, 'Changing Branch Failed', 'Changed Branch.')

def customIntall(ssh):
    print("starting the actual installing of programs on the child, this can take up to 15 minutes.")
    command = """cd ~/Skynet2.0 && sh build.sh >> build.out"""
    (_, out0, err0) = ssh.run(command)
    ssh._checkStreams_until_done(out0, err0, 'Preqrequisite installation failed', 'Preqrequisite installation succesfull.')

def startup_child(bc):
    bc.giveChildGeneticCode(DNA())
    bc.startChild()

def startup_and_transfer_funds(ssh, v):
    print("agentcore running on the server")
    
    #check wallet
    
    command = """electrum listaddresses"""
    (_, out0, err0) = ssh.run(command)
    ssh._checkStreams(out0, err0, 'error was thrown for "'+command+'"', 'no error was thrown for "'+command+'"')
    
    walletFinder = re.compile(r'\[\W*"([A-z0-9]+)"\W*\]')
    #f = out0#open("Skynet.log", "r")
    
    fr = out0.read()
    print('wallet output:'+ fr)    
    
    result = walletFinder.search(fr)
    
    childWallet = result.group(1)
    
    print("preparing to send all contents of wallet to child, but first writing the following to child.out")
    print("child ssh username: "+v.SSHUsername)
    print("child ssh password: "+v.SSHPassword)
    print("child ssh ip: "+v.IP)
    print("child wallet address: "+childWallet)
    
    f = open("child.out", "A+")
    f.write('created a child:')
    f.write("child ssh username: "+v.SSHUsername)
    f.write("child ssh password: "+v.SSHPassword)
    f.write("child ssh ip: "+v.IP)
    f.write("child wallet address: "+childWallet)
    
    #Wallet.send_everything_to(childWallet)

prepChild(ssh)
customIntall(ssh)
startup_child(bc)
#sleep for a while to let all programs startup
time.sleep(300)
startup_and_transfer_funds(ssh, v)