import logging
from modules.hostBaseClass import hostBase

class iperfServer(hostBase):
    def __init__(self, ipAddress ):
        super().__init__(ipAddress)
        self.iperfServerLogger = logging.getLogger(__name__)
        self.iperfServerLogger.setLevel(logging.DEBUG)
        self.iperf3Name = 'iperf3'

    def startIperf3ServerDaemon(self, port=5201):
        self.iperfServerLogger.info( '%s: iperf3 server started on port %d' % (self.ipAddress, port))
        iperfServerString = 'iperf3 -s -D -p %d' % (port)
        result = self.executeBashCommand(iperfServerString)
        return result

    def stopIperf3ServerDaemon(self):
        self.iperfServerLogger.info( '%s: iperf3 server shutting down' % (self.ipAddress))
        self.stopProcess(self.iperf3Name)



