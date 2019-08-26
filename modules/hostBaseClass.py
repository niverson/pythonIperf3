import logging
from modules.cliBaseClass import cliBase

class hostBase(cliBase):
    def __init__(self, ipAddress ):
        super().__init__(ipAddress)
        self.hostLogger = logging.getLogger(__name__)
        self.hostLogger.setLevel(logging.DEBUG)

    def __str__(self):
        return f"{self.ipAddress}"

    def __repr__(self):
        return f"{self.ipAddress}"

    def stopProcess(self, processName ):
        """look up and kill a process on the host"""
        self.hostLogger.info( 'looking for %s on %s' % (processName, self.ipAddress))

        # get the process id with the process is running on the host
        result = self.executeBashCommand('pgrep %s' % processName)

        if result.returncode == 0:
            # kill the process on the host
            result = self.executeBashCommand('kill -6 %s' % result.stdout.decode())
            if result.returncode == 0:
                self.hostLogger.info('%s stopped on %s' % (processName,self.ipAddress))
            else:
                self.hostLogger.error('kill %s returned %s' % (processName,result.returncode))
        else:
            self.hostLogger.error('pgrep returned %s' % (result.returncode))

        return result.returncode