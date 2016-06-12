#!/usr/bin/python

import argparse
import os
import re
import sys
import time

from agent.Birthchamber import Birthchamber
from agent.DNA import DNA
from agent.Settings import Settings
from agent.VPSBuyer import VPSBuyer
from agent.Wallet import Wallet

from ExitNode import Tunnel

from ssh.SSH import SSH

from Tribler.community.tunnel.tunnel_community import TunnelSettings

class Prototype2(object):
    
    def __init__(self, enableExitNode, useTestServer):
        #prototype2 starts in development mode unless specifically told otherwise
        s = Settings()
        wallet = Wallet()
        
        if enableExitNode:
            print("starting Tribler Exitnode")
            settings = TunnelSettings()
            
            # For disabling anonymous downloading, limiting download to hidden services only
            settings.min_circuits = 0
            settings.max_circuits = 0
            settings.become_exitnode = True
            crawl_keypair_filename = None
            dispersy_port = -1 
            
            tunnel = Tunnel(settings, crawl_keypair_filename, dispersy_port)
            #StandardIO(LineHandler(tunnel, profile))
            tunnel.start(None)
        
        bc = Birthchamber()        
        
        if useTestServer:
            #this part works for this version, and since this script is just for doing integration it should be fine
            #i still need to write a dummy vpsbuyer that simply takes these values
            bc.get_child_using_test_server('prototype2')
            v = bc.vps
            
            print("preparing to run protoype2_agentcore on the following server:")
            print("SSHUsername: "+v.SSHUsername)
            print("SSHPassword: "+v.SSHPassword)
            print("SSHIP: "+v.IP)
            
            
            
        else:
            v = bc.vps
            while(wallet.balance()<bc.getChildCost()):
                print("Not enough bitcoins, waiting for money to arrive")
                time.sleep(600)
            bc.getChild('prototype2')
        
        
    
        print("started up agentCore on child, transferring own funds to child")
        ssh = SSH(v.getIP(),v.getSSHUsername(),v.getSSHPassword(),22)
        self.transfer_funds_to_child_wallet(ssh, v)
    
    def prepChild(self, ssh):
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
    
#    def customIntall(self, ssh):
#        print("starting the actual installing of programs on the child, this can take up to 15 minutes.")
 #       command = """cd ~/Skynet2.0 && sh build.sh >> build.out"""
 #       (_, out0, err0) = ssh.run(command)
 #       ssh._checkStreams_until_done(out0, err0, 'Preqrequisite installation failed', 'Preqrequisite installation succesfull.')
    
#    def startup_child(self, bc, vps):
#        bc.giveChildGeneticCode(DNA(), vps)
#        bc.start_child_other_version("agent/prototype2_agentCore.py")
        
    
    def transfer_funds_to_child_wallet(self, ssh, v):
        print("agentcore running on the server")
        
        #check wallet
        
        childWallet = self.get_child_wallet_address(ssh)
        
        print("preparing to send all contents of wallet to child, but first writing the following to child.out")
        print("child ssh username: "+v.SSHUsername)
        print("child ssh password: "+v.SSHPassword)
        print("child ssh ip: "+v.IP)
        print("child wallet address: "+childWallet)
        
        f = open("child.out", "a+")
        f.write('created a child:')
        f.write("child ssh username: "+v.SSHUsername)
        f.write("child ssh password: "+v.SSHPassword)
        f.write("child ssh ip: "+v.IP)
        f.write("child wallet address: "+childWallet)
        
        w = Wallet()
        w.send_everything_to(childWallet)
        
    def get_child_wallet_address(self, ssh):
        """
        returns the child's wallet address if one exists. Else it will create one and return this.
        """
        command = """electrum listaddresses"""
        (_, out0, err0) = ssh.run(command)
        ssh._checkStreams(out0, err0, 'error was thrown for "'+command+'"', 'no error was thrown for "'+command+'"')
        
        walletFinder = re.compile(r'\[\W*"([A-z0-9]+)"\W*\]')
        #f = out0#open("Skynet.log", "r")
        
        fr = out0.read()
        print('wallet output:'+ fr)    
        
        result = walletFinder.search(fr)
            
        #This horrible feedback loop is here due to a quirk of electrum.
        #Needs refactoring, but do not refactor without extensive testing (i.e. multiple vps all from clean install)
        #Because electrum behaviour right after startup tends to differ from server to server (i suspect something to do wtih specs)
        try:
            return result.group(1)
        except:
            ssh.run('''(cd ~/Skynet2.0 && PYTHONPATH=${PYTHONPATH}:. python agent/prototype2_agentCore.py -t True -x True &> agentCore.out &)''')
            return self.get_child_wallet_address(ssh)
    
    
#    def run(self, ssh,bc,v):    
 #       self.prepChild(ssh)
#        self.customIntall(ssh)
#        self.startup_child(bc)
#        self.transfer_funds_to_child_wallet(ssh, v)
        
def main(argv):
    parser = argparse.ArgumentParser(description='Prototype 2 of the Autonomous self-replicating code.')
    try:
        parser.add_argument('-t', '--usetestserver', help='circumvent dna and use testserver defined in settings.json')
        parser.add_argument('-x', '--exitnode', help='Enable the agents\' Tribler Exit Node functionality')
        
        parser.add_help = True
        args = parser.parse_args(argv)

    except argparse.ArgumentError:
        parser.print_help()
        sys.exit(2)
    
    #return whether -as boolean- the set value, return default if not set
    #defaults are development mode equivalent
    usetestserver = False if args.usetestserver in ['False', 'false'] else True
    exitnode = True if args.exitnode in ['True', 'true'] else False
        
    Prototype2(exitnode, usetestserver)
    
        
if __name__=="__main__":
    main(sys.argv[1:])
    
