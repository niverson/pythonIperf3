import logging
import re
from modules.hostBaseClass import HostBase

class IperfClient(HostBase):
    """This class is used to start an iperf3 client to stream data to the iperf3 server.
        This class takes an ip address and an iperf3 log file name."""
    def __init__(self, ip_address, log_file):
        super().__init__(ip_address)
        self.iperf_client_logger = logging.getLogger(__name__)
        self.iperf_client_logger.setLevel(logging.DEBUG)
        self.log_file = log_file
        self.iperf_client_logger.info( 'iperf3 for %s uses logfile %s' % ( ip_address, log_file))

    def __str__(self):
        return f"{self.ip_address}"

    def __repr__(self):
        return f"{self.ip_address}"


    def start_iperf3_client(self, target_ip_address, port=5201):
        """have the iperf3 client system start simple bandwidth test. results are saved to a file."""
        iperf_client_string = 'iperf3 -c %s --logfile %s -i 5 -f M -p %d' % (target_ip_address, self.log_file, port)
        self.iperf_client_logger.info('iperf3 client running to %s:%d' % (target_ip_address, port))
        result = self.execute_bash_command(iperf_client_string)
        return result

