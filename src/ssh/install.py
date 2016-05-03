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
        (_, out0, err0) = self.ssh.run('apt install git')
        self._checkStreams(out0, err0, 'git install failed', 'git installed.')
        (_, out0, err0) = self.ssh.run('git clone https://github.com/Skynet2-0/Skynet2.0.git')
        self._checkStreams(out0, err0, 'Clone failed', 'project cloned.')
        (_, out0, err0) = self.ssh.run('cd Skynet2.0')
        self._checkStreams(out0, err0, 'cd Skynet2.0 failed', 'Inside the Skynet2.0 directory')
        (_, out0, err0) = self.ssh.run('sh build.sh')
        self._checkStreams(out0, err0, 'build failed', 'build succeeded.')
        #(_, out0, err0) = self.ssh.run('sh run.sh')
        #self._checkStreams(out0, err0, 'run failed')
        print('Installation finished.')

    def _checkStreams(self, out, err, errmessage = '', succesmessage = None):
        '''
        Checks the streams for error message and exit code.
        out is the output stream.
        err is the error stream.
        errmessage is the message at the start after error.
        succesmessage is the message on succes.
        '''
        print("_checkStream called.")
        timeout = time.time() + 120
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
        print("_checkStream finished.")

    def finish(self):
        '''
        Does some clean up.
        '''
        self.ssh.close_connection()
