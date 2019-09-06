import logging
from modules.cliBaseClass import CliBase

class HostBase(CliBase):
    """This class that is used to execute a shell command on a targeted server and handle command specific responses.
    This class takes an ip address."""
    def __init__(self, ip_address ):
        super().__init__(ip_address)
        self.host_logger = logging.getLogger(__name__)
        self.host_logger.setLevel(logging.DEBUG)

    def __str__(self):
        return f"{self.ip_address}"

    def __repr__(self):
        return f"{self.ip_address}"

    def stop_process(self, process_name ):
        """look up and kill a process on the host"""
        self.host_logger.info( 'looking for %s on %s' % (process_name, self.ip_address))

        # get the process id with the process is running on the host
        result = self.execute_bash_command('pgrep %s' % process_name)

        if result.returncode == 0:
            # kill the process on the host
            result = self.execute_bash_command('kill -6 %s' % result.stdout.decode())
            if result.returncode == 0:
                self.host_logger.info('%s stopped on %s' % (process_name, self.ip_address))
            else:
                self.host_logger.error('kill %s returned %s' % (process_name,result.returncode))
        else:
            self.host_logger.error('pgrep returned %s' % (result.returncode))

        return result.returncode