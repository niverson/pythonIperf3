import logging
import subprocess

class CliBase( ):
    """This is a generic cli class that is used to ssh into a server and execute a shell command.
    This class takes an ip address. The object will use that ip address to target the system
    whenever the instance methods are called. """
    def __init__(self, ip_address ):
        self.ip_address = ip_address
        self.cli_logger = logging.getLogger(__name__)
        self.cli_logger.setLevel(logging.DEBUG)

    def __str__(self):
        return f"{self.ip_address}"

    def __repr__(self):
        return f"{self.ip_address}"

    def execute_bash_command(self, cmd_string):
        """ssh into the server and execute the passed in command. return the result"""
        result = self.execute_bash_command_with_timeout(cmd_string, 30)
        return result


    def execute_bash_command_with_timeout(self, cmd_string, user_timeout):
        """ssh into the server and execute the passed in command with user defined timeout. return the result"""
        result = None
        self.cli_logger.info('sending %s' % cmd_string)

        ssh_string = "ssh %s " % (self.ip_address)
        ssh_string += '"' + cmd_string + '"'

        self.cli_logger.debug('sending %s' % ssh_string)
        try:
            result = subprocess.run(ssh_string, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                    timeout=user_timeout)

        except subprocess.TimeoutExpired:
            self.cli_logger.error('%s timedout!', ssh_string)

        if result.returncode != 0:
            self.cli_logger.error('%s', result.stderr)

        return result