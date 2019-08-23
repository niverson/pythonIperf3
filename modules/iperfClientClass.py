import logging
import re
from modules.hostBaseClass import hostBase

class iperfClient(hostBase):
    def __init__(self, ipAddress):
        super().__init__(ipAddress)
        self.iperfClientLogger = logging.getLogger(__name__)
        self.iperfClientLogger.setLevel(logging.DEBUG)
        self.fullQualifiedIperf = ''
        self.getFullyQualifiedIperf()

    def getFullyQualifiedIperf(self):
        result = self.executeBashCommand('which iperf3')
        if result.returncode == 0:
            string = result.stdout.decode("utf-8")
            cleaned = re.sub("\n","",string)
            self.fullQualifiedIperf = cleaned
        else:
            self.iperfClientLogger( '%s' % result.stderr )

    def startIperf3Client(self, targetIpAddress, port=5201):
        iperfClientString = 'iperf3 -c %s -f M -p %d' % (targetIpAddress, port)
        self.iperfClientLogger.info('iperf3 client running to %s:%d' % (targetIpAddress, port))
        result = self.executeBashCommand(iperfClientString)
        return result

