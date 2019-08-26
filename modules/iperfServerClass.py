import logging
from modules.hostBaseClass import hostBase

class iperfServer(hostBase):
    def __init__(self, ipAddress ):
        super().__init__(ipAddress)
        self.iperfServerLogger = logging.getLogger(__name__)
        self.iperfServerLogger.setLevel(logging.DEBUG)
        self.iperf3Name = 'iperf3'

    def __str__(self):
        return f"{self.ipAddress}"

    def __repr__(self):
        return f"{self.ipAddress}"

    def startIperf3ServerDaemon(self, port=5201):
        """setup the iperf3 server on the host"""
        self.iperfServerLogger.info( '%s: iperf3 server started on port %d' % (self.ipAddress, port))
        iperfServerString = f'{self.iperf3Name} -s -D -p {port}'
        result = self.executeBashCommand(iperfServerString)
        return result

    def stopIperf3ServerDaemon(self):
        """stop the iperf3 server on the host"""
        self.iperfServerLogger.info( '%s: iperf3 server shutting down' % (self.ipAddress))
        result = self.stopProcess(self.iperf3Name)
        return result


