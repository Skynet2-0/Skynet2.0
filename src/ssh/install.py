from src.ssh.SSH import SSH
import time


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
        print('Start installing.')
        (_, out0, err0) = self.ssh.run('apt-get update')
        self._checkStreams(out0, err0, 'apt update failed', 'apt updated.')
        (_, out0, err0) = self.ssh.run('apt-get install -y git')
        self._checkStreams(out0, err0, 'git install failed', 'git installed.')
        command = 'git clone https://github.com/Skynet2-0/Skynet2.0.git'
        (_, out0, err0) = self.ssh.run(command)
        self._checkStreams(out0, err0, 'git clone failed', 'project cloned.')
        command = """chmod a+rx -R Skynet2.0 && cd Skynet2.0 && export PATH=$PATH:. && sh build.sh"""
        (_, out0, err0) = self.ssh.run(command)
        self._checkStreams(out0, err0, 'build failed', 'project build.')
        print('Installation finished.')

    def _checkStreams(self, out, err, errmessage = '', succesmessage = None):
        '''
        Checks the streams for error message and exit code.
        out is the output stream.
        err is the error stream.
        errmessage is the message at the start after error.
        succesmessage is the message on succes.
        '''
        timeout = time.time() + 300
        done = False
        while time.time() <= timeout and not done:
            if out.channel.exit_status_ready():
                exitcode = out.channel.recv_exit_status()
                if exitcode != 0:
                    print("Error %s: %s\nexit status: %i" % (errmessage, err.read().decode(),
                                                exitcode))
                elif succesmessage is not None:
                    print(succesmessage)
                done = True
            else:
                time.sleep(1)

    def finish(self):
        '''
        Does some clean up.
        '''
        self.ssh.close_connection()
