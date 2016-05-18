'''
Created on Apr 29, 2016

@author: Stefan
'''
import unittest
from src.agent.ssh.install import Installer
from src.agent.ssh.SSH import SSH
import time


port = None # the port
hostname = None # the host
user = None # the user
pwd = None # the password

@unittest.skipIf(hostname is None, 'Installation test requires a hostname to install on.')
class InstallTest(unittest.TestCase):
    '''
    Does an Integration test of the Installer class.
    To succesfully run this test fill in the parameters above with
    values corresponding to an SSH server. This can be any SSH server
    that you can log into. It should even work when the SSH server is local.
    After running please reset all the parameters to None.
    '''

    def setUp(self):
        ssh = SSH(hostname, user, pwd, port)
        ssh.run('rm -rf Skynet2.0')
        ssh.close_connection()
        self.installer = Installer(hostname, user, pwd, port)
        self.installer.install()
        self.ssh = self.installer.ssh

    def tearDown(self):
        self.installer.finish()

    def testInstall(self):
        (_, out, _) = self.ssh.run('ls')
        #(_, curdir, _) = self.ssh.run('pwd')
        output = out.read().decode()
        print("folders: %s" % (output))
        #print("Current directory %s" % (curdir.read().decode()))
        self.assertTrue("Skynet" in output)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
