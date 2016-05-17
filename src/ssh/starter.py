'''
This class can start a child once it has been installed unto
'''

class Starter:
	'''
    This class is responsable for sending the startup commands to
    the child server. It uses the SSH class to send them.
    '''

    def __init__(self, hostip, user, password, port = None):
        '''
        Constructs the Installer.
        hostip is the ip address of the host.
        user is the username of the user (Usually it will be host).
        password is the password.
        port is the port to connect to.
        '''

        self.ssh = SSH(hostip, user, password, port)
		
	def start(self):
		(_, out0, err0) = self.ssh.run('PYTHONPATH="Skynet2.0"python Skynet2.0/src/agent/agentCore.py')
        #self._checkStreams(out0, err0, 'apt update failed', 'apt updated.')