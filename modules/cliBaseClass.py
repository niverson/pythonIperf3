import logging
import subprocess

class cliBase( ):
    def __init__(self, ipAddress ):
        self.ipAddress = ipAddress
        self.cliLogger = logging.getLogger(__name__)
        self.cliLogger.setLevel(logging.DEBUG)

    def executeBashCommand(self, cmdString):
        result = self.executeBashCommandWithTimeout(cmdString, 30)
        return result


    def executeBashCommandWithTimeout(self, cmdString, userTimeout):
        result = None
        self.cliLogger.info('sending %s' % cmdString)

        sshString = "ssh %s " % (self.ipAddress)
        sshString += '"' + cmdString + '"'
        try:
            result = subprocess.run(sshString, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                    timeout=userTimeout)

        except subprocess.TimeoutExpired:
            self.cliLogger.error('%s timedout!', sshString)

        if result.returncode != 0:
            self.cliLogger.error('%s', result.stderr)

        return result