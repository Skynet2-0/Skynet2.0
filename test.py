from agent.Birthchamber import Birthchamber
from agent.DNA import DNA
from agent.Settings import Settings
from agent.VPSBuyer import VPSBuyer
from ssh.SSH import SSH
import os

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
print('Start installing.')
(_, out0, err0) = ssh.run('apt-get update')
ssh._checkStreams(out0, err0, 'apt update failed', 'apt updated.')
(_, out0, err0) = ssh.run('apt-get install -y git')
ssh._checkStreams(out0, err0, 'git install failed', 'git installed.')
command = """git clone --recursive https://github.com/Skynet2-0/Skynet2.0.git"""
(_, out0, err0) = ssh.run(command)
ssh._checkStreams(out0, err0, 'git clone failed', 'project cloned.')
command = """cd Skynet2.0 && git checkout prototype2"""
(_, out0, err0) = ssh.run(command)
ssh._checkStreams(out0, err0, 'Changing Branch Failed', 'Changed Branch.')

print("starting the actual installing of programs on the child, this can take up to 15 minutes.")
command = """sh Skynet2.0/build.sh"""
(_, out0, err0) = ssh.run(command)
ssh._checkStreams(out0, err0, 'Preqrequisite installation failed', 'Preqrequisite installation succesfull.')






print('Installation finished.')

bc.giveChildGeneticCode(DNA())
bc.startChild()
print("agentcore running on the server")

#check wallet

command = """electrum listaddresses"""
(_, out0, err0) = ssh.run(command)
ssh._checkStreams(out0, err0, 'Wallet finding failed', 'Found wallet.')