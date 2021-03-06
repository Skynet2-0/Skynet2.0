"""
This class can start a child once it has been installed unto.
"""

from SSH import SSH
import os


class Starter(object):
    """
    This class is responsable for sending the startup commands to
    the child server. It uses the SSH class to send them.
    """

    def __init__(self, hostip, user, password, port=None, use_log=None):
        """
        Constructs the Starter which starts the program.

        hostip -- the ip address of the host.
        user -- the username of the user (Usually it will be host).
        password -- the password.
        port -- the port to connect to. (Default is None)
        use_log -- True for logging the starting. (Default is None)
        """
        if (use_log is None):
            self.ssh = SSH(hostip, user, password, port)
        else:
            self.ssh = SSH(hostip, user, password, port, use_log)

    def start(self, otherCore = None):
        """ Starts the program. """
        self.start_other_requirements()
        if otherCore:
            self.start_agent("agent/"+otherCore+" -x True -t False")
        else:            
            self.start_agent("agent/agentCore.py -x True -t False")

    def start_other_requirements(self):
        self.ssh.run('''(Xvfb :99 -ac &> /dev/null &)''')
        
        self.ssh.run('''(cd ~/Skynet2.0 && export DISPLAY=:99 && java -jar selenium-server-standalone-2.53.0.jar &>log.out &)''')

    def start_agent(self, relAgentPath):
        """
        given the path to the agent program starting from ~/Skynet2.0 runs this agent
        """
        self.ssh.run('(cd ~/Skynet2.0 && PYTHONPATH=${PYTHONPATH}:. python ' + relAgentPath + ' &>>agentCore.out &)')