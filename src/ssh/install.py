from src.ssh import SSH


class Installer(object):
    '''
    This class is responsable for sending the install commands to
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
        #self.ip = hostip
        #self.user = user
        #self.password = password
        self.ssh = SSH(hostip, user, password, port)

    def install(self):
        '''
        Makes the class install itself through SSH.
        It also starts running the class.
        '''
        self.ssh.run('git clone https://github.com/Skynet2-0/Skynet2.0.git')
        self.ssh.run('cd Skynet2.0')
        self.ssh.run('sh build.sh')
        self.ssh.run('sh run.sh')

    def finalized(self):
        '''
        Does some clean up.
        '''
        self.ssh.close_connection()
