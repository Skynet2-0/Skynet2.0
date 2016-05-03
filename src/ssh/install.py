from src.ssh.SSH import SSH


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
        (_, out0, err0) = self.ssh.run('apt-get update')
        self._checkStreams(out0, err0, 'apt update failed')
        (_, out0, err0) = self.ssh.run('apt-get install git')
        self._checkStreams(out0, err0, 'git install failed')
        (_, out0, err0) = self.ssh.run('git clone https://github.com/Skynet2-0/Skynet2.0.git')
        self._checkStreams(out0, err0, 'Clone failed')
        (_, out0, err0) = self.ssh.run('cd Skynet2.0')
        self._checkStreams(out0, err0, 'cd Skynet2.0 failed')
        (_, out0, err0) = self.ssh.run('sh build.sh')
        self._checkStreams(out0, err0, 'build failed')
        (_, out0, err0) = self.ssh.run('sh run.sh')
        self._checkStreams(out0, err0, 'run failed')

    def _checkStreams(self, out, err, startmessage = ''):
        '''
        Checks the streams for error message and exit code.
        out is the output stream.
        err is the error stream.
        startmessage is the message at the start after error.
        '''
        errstr = err.read().decode()
        if errstr is not None:
            print("Error %s: %s\nexit status: %i" % (startmessage, errstr,
                                        out.channel.recv_exit_status()))

    def finish(self):
        '''
        Does some clean up.
        '''
        self.ssh.close_connection()
