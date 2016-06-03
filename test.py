from agent.Birthchamber import Birthchamber
from agent.DNA import DNA
from ssh.SSH import SSH

SSH.global_use_logfile()
print("global logging is : "+SSH.default_use_log)
s = Settings()

#this part works for this version, and since this script is just for doing integration it should be fine
#i still need to write a dummy vpsbuyer that simply takes these values
v = VPSBuyer()
v.SSHUsername = s.get_test_server_username()
v.SSHPassword = s.get_test_server_password()
v.IP = s.get_test_server_ip()

bc = Birthchamber()
bc.vps = v

bc.installChild()
bc.giveChildGeneticCode(DNA())
bc.startChild()