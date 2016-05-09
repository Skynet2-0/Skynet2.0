'''
Created on Apr 29, 2016

@author: Stefan
'''
import unittest
from src.ssh.SSH import *
#from MockSSH import Server
import time

@unittest.skip("Not working test.")
class SSHTest(unittest.TestCase):

    port = 1050
    hostname = 'localhost'

    @classmethod
    def setUpClass(cls):
        users = {'testadmin': 'x'}
        MockSSH.startThreadedServer(
            commands,
            prompt="[root@hostname:Active] testadmin # ",
            interface=SSHTest.hostname,
            port=SSHTest.port,
            **users)
        time.sleep(0.5)

    @classmethod
    def tearDownClass(cls):
        print("tearDownClass")
        MockSSH.stopThreadedServer()

    def setUp(self):
        self.that = SSH(SSHTest.hostname, None, None, SSHTest.port)
        self.that.set_missing_host_key_policy(WarningPolicy())

    def tearDown(self):
        self.that.close_connection()

    def testNoError(self):
        '''
        Tests if out exists after running a command.
        '''
        (_, out, _) = self.that.run('ls')
        self.assertIsNotNone(out)

    def testLsReturnValue(self):
        '''
        Checks the return value of ls
        '''
        (_, out, _) = self.that.run('ls')
        self.assertEqual(0, out.channel.recv_exit_status())

    def testLsStringReturned(self):
        '''
        Checks the existance of a string returned by ls.
        '''
        (_, out, _) = self.that.run('ls')
        output = out.read().decode()
        self.assertIsNotNone(output)
        print("\nls returned %s" % output)

    def testEchoStringReturned(self):
        '''
        Tests the reply of the echo command.
        '''
        string = 'The reply'
        (_, out, _) = self.that.run('echo -n ' + string)
        output = out.read().decode()
        print("\necho returned %s" % output)
        self.assertEqual(output, string)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
