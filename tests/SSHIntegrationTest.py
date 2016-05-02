'''
Created on Apr 29, 2016

@author: Stefan
'''
import unittest
from src.agent.SSH import *
import time


class SSHTest(unittest.TestCase):
    '''
    Does an Integration test of the SSH class.
    To succesfully run this test fill in the parameters below with
    values corresponding to an SSH server. This can be any SSH server
    that you can log into. It should even work when the SSH server is local.
    '''

    port = None # the port
    hostname = None # the host
    user = None # the user
    pwd = None # the password'

    def setUp(self):
        self.that = SSH(SSHTest.hostname, SSHTest.user, SSHTest.pwd, SSHTest.port)

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
        #print("\nls returned %s" % output)

    def testEchoStringReturned(self):
        '''
        Tests the reply of the echo command.
        '''
        string = 'The reply'
        (_, out, _) = self.that.run('echo -n ' + string)
        output = out.read().decode()
        #print("\necho returned %s" % output)
        self.assertEqual(output, string)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
