import logging
import re
from modules.hostBaseClass import hostBase

class iscsiadmTargets():
    def __init__(self, ipAddress, iqn, port):
        self.ipAddress = ipAddress
        self.iqn = iqn
        self.port = port

    def __str__(self):
        return f"{self.ipAddress}:{self.port} {self.iqn}"

    def __repr__(self):
        return f"{self.ipAddress}:{self.port} {self.iqn}"

class iscsiadm(hostBase):
    def __init__(self, ipAddress):
        super().__init__(ipAddress)
        self.iscsiadmLogger = logging.getLogger(__name__)
        self.iscsiadmLogger.setLevel(logging.DEBUG)
        self.targetList = []

    def __str__(self):
        return f"{self.ipAddress}"

    def __repr__(self):
        return f"{self.ipAddress}"

    def discoverTarget(self, targetIpAddress, port=3260):
        """discover the iscsi target and parse out target details on success. Creates target objects from response and
        puts those objects on target list"""
        iscsiAdmString = 'sudo iscsiadm --mode discovery --type sendtargets --portal %s:%d' % (targetIpAddress, port)
        self.iscsiadmLogger.info('iscsiAdm discovering %s:%d' % (targetIpAddress, port))
        result = self.executeBashCommand(iscsiAdmString)

        if result.returncode == 0:
            # split out each target line into a list to be processed
            listOfSplitResults = result.stdout.splitlines()

            for line in listOfSplitResults:

                # extract the ipv4 addresses from the line.
                list = re.findall(b'[0-9]+(?:\.[0-9]+){3}', line)
                admIp = list[0].decode("utf_8")

                # extract the port from the line
                list = re.findall(b'([0-9]+,)', result.stdout)
                # remove the comma from the part match
                admPort = re.sub(',','',list[0].decode("utf_8"))

                list= re.findall(b'(iqn+\S*)', line)
                admIqn = re.sub(',','',list[0].decode("utf_8"))

                self.iscsiadmLogger.info( "found %s at %s:%s" % ( admIqn, admIp, admPort))
                target = iscsiadmTargets(admIp, admIqn, admPort)
                self.targetList.append(target)
        else:
            self.iscsiadmLogger.info("failed to find targets at %s:%s" % (targetIpAddress, port))

        return result.returncode

    def logInToTargets(self):
        """logs into all targets on the instances targetList from discoverTargets"""
        result = 0
        for target in self.targetList:
            iscsiAdmString = 'sudo iscsiadm --mode node --targetname %s --portal %s:%s --login' % (target.iqn,
                                                                                                   target.ipAddress,
                                                                                                   target.port)
            self.iscsiadmLogger.info('logging into %s at %s:%s' % (target.iqn, target.ipAddress, target.port))
            response = self.executeBashCommand(iscsiAdmString)
            if response.returncode != 0:
                self.iscsiadmLogger.error('failed logging into at %s %s:%s' % (target.iqn, target.ipAddress,
                                                                            target.port))
                result = 1
            else:
                self.iscsiadmLogger.info('logged into %s at %s:%s' % (target.iqn, target.ipAddress, target.port))

        return result


    def logoutTargets(self):
        """logs outs all targets on the instances targetList from discoverTargets"""
        result = 0
        for target in self.targetList:
            iscsiAdmString = 'sudo iscsiadm --mode node --targetname %s --portal %s:%s --logout' % (target.iqn,
                                                                                                    target.ipAddress,
                                                                                                    target.port)
            self.iscsiadmLogger.info('logout %s at %s:%s' % (target.iqn, target.ipAddress, target.port))
            response = self.executeBashCommand(iscsiAdmString)
            if response.returncode != 0:
                self.iscsiadmLogger.error('failed logging out at %s %s:%s' % (target.iqn, target.ipAddress,
                                                                            target.port))
                result = 1
            else:
                self.iscsiadmLogger.info('logged out %s at %s:%s' % (target.iqn, target.ipAddress, target.port))

        return result