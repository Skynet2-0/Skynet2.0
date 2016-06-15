from agent.VPSBuyer import VPSBuyer

class DummyVPSBuyer(VPSBuyer):
    """
    This class provides all data delivered by a zappiehostbuyer without actually buying
    """
    def __init__(self, SSHip = "", SSHUsername = "", SSHPassword = ""):
        """
        Creates a new ZappiehostBuyer.

        email -- The email address to use. (Default is '')
        password -- The password to use. (Default is '')
        SSHPassword -- The password to use for the ssh connection. (Default is '')
        """
        super(DummyVPSBuyer, self).__init__()
        self.IP = SSHip
        self.SSHUsername = SSHUsername
        self.SSHPassword = SSHPassword