import logging
from modules.hostBaseClass import HostBase

class IperfServer(HostBase):
    def __init__(self, ip_address ):
        super().__init__(ip_address)
        self.iperf_server_logger = logging.getLogger(__name__)
        self.iperf_server_logger.setLevel(logging.DEBUG)
        self.iperf3_name = 'iperf3'

    def __str__(self):
        return f"{self.ip_address}"

    def __repr__(self):
        return f"{self.ip_address}"

    def start_iperf3_server_daemon(self, port=5201):
        """setup the iperf3 server on the host"""
        self.iperf_server_logger.info( '%s: iperf3 server started on port %d' % (self.ip_address, port))
        iperf_server_string = f'{self.iperf3_name} -s -D -p {port}'
        result = self.execute_bash_command(iperf_server_string)
        return result

    def stop_iperf3_server_daemon(self):
        """stop the iperf3 server on the host"""
        self.iperf_server_logger.info( '%s: iperf3 server shutting down' % (self.ip_address))
        result = self.stop_process(self.iperf3_name)
        return result


