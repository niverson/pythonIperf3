import logging
import re
from modules.hostBaseClass import hostBase

class iperfClient(hostBase):
    def __init__(self, ipAddress, logfile):
        super().__init__(ipAddress)
        self.iperfClientLogger = logging.getLogger(__name__)
        self.iperfClientLogger.setLevel(logging.DEBUG)
        self.logfile = logfile
        self.iperfClientLogger.info( 'iperf3 for %s uses logfile %s' % ( ipAddress, logfile))


    def startIperf3Client(self, targetIpAddress, port=5201):
        iperfClientString = 'iperf3 -c %s --logfile %s -i 5 -f M -p %d' % (targetIpAddress, self.logfile, port)
        self.iperfClientLogger.info('iperf3 client running to %s:%d' % (targetIpAddress, port))
        result = self.executeBashCommand(iperfClientString)
        return result

