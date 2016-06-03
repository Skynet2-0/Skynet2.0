"""
This class can create a file with contents
"""

from SSH import SSH


class FileCreator(object):
    """
    This class is responsable for creating files on the child server. It uses the SSH class to send them.
    """

    def __init__(self, hostip, user, password, port=None, use_log=None):
        """
        Constructs the FileCreator which starts the program.

        hostip -- the ip address of the host.
        user -- the username of the user (Usually it will be host).
        password -- the password.
        port -- the port to connect to. (Default is None)
        use_log -- True for logging the starting. (Default is None)
        """
        use_log = True
        if (use_log is None):
            self.ssh = SSH(hostip, user, password, port)
        else:
            self.ssh = SSH(hostip, user, password, port, use_log)

    def create(self, path, text):
        """ 
        creates a file at path with contents text. 
        example: createFile("~/file.txt", "test") will create a file named file.txt with contents "test" 
        """
        (_, out0, err0) = self.ssh.run('echo \"'+str(text)+'\" > '+str(path))
        #self._checkStreams(out0, err0, 'apt update failed', 'apt updated.')
