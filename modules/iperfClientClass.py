import logging
from modules.hostBaseClass import hostBase

class iperfClient(hostBase):
    def __init__(self, ipAddress):
        super().__init__(ipAddress)
        self.iperfClientLogger = logging.getLogger(__name__)
        self.iperfClientLogger.setLevel(logging.DEBUG)

    def startIperf3Client(self, targetIpAddress, port=5201):
        iperfClientString = 'iperf3 -c %s -f M -p %d' % (targetIpAddress, port)
        self.iperfClientLogger.info('iperf3 client running to %s:%d' % (targetIpAddress, port))
        result = self.executeBashCommand(iperfClientString)
        return result
