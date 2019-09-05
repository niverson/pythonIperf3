import logging
import re
from modules.hostBaseClass import HostBase

class IscsiadmTargets():
    def __init__(self, ip_address, iqn, port):
        self.ip_address = ip_address
        self.iqn = iqn
        self.port = port

    def __str__(self):
        return f"{self.ip_address}:{self.port} {self.iqn}"

    def __repr__(self):
        return f"{self.ip_address}:{self.port} {self.iqn}"


class Iscsiadm(HostBase):

    def __init__(self, ip_address):
        super().__init__(ip_address)
        self.iscsiadm_logger = logging.getLogger(__name__)
        self.iscsiadm_logger.setLevel(logging.DEBUG)
        self.target_list = []

    def __str__(self):
        return f"{self.ip_address}"

    def __repr__(self):
        return f"{self.ip_address}"

    def discover_target(self, target_ip_address, port=3260):
        """discover the iscsi target and parse out target details on success. Creates target objects from response and
        puts those objects on target list"""
        iscsi_adm_string = 'sudo iscsiadm --mode discovery --type sendtargets --portal %s:%d' % \
                           (target_ip_address, port)
        self.iscsiadm_logger.info('iscsiadm discovering %s:%d' % (target_ip_address, port))
        result = self.execute_bash_command(iscsi_adm_string)

        if result.returncode == 0:
            # split out each target line into a list to be processed
            list_Of_split_results = result.stdout.splitlines()

            for line in list_Of_split_results:

                # extract the ipv4 addresses from the line.
                list = re.findall(b'[0-9]+(?:\.[0-9]+){3}', line)
                adm_ip = list[0].decode("utf_8")

                # extract the port from the line
                list = re.findall(b'([0-9]+,)', result.stdout)
                # remove the comma from the part match
                adm_port = re.sub(',','',list[0].decode("utf_8"))

                list= re.findall(b'(iqn+\S*)', line)
                adm_iqn = re.sub(',','',list[0].decode("utf_8"))

                self.iscsiadm_logger.info( "found %s at %s:%s" % ( adm_iqn, adm_ip, adm_port))
                target = IscsiadmTargets(adm_ip, adm_iqn, adm_port)
                self.target_list.append(target)
        else:
            self.iscsiadm_logger.info("failed to find targets at %s:%s" % (target_ip_address, port))

        return result.returncode

    def log_in_to_targets(self):
        """logs into all targets on the instances target_List from discover_target"""
        result = 0
        for target in self.target_list:
            iscsi_adm_string = 'sudo iscsiadm --mode node --targetname %s --portal %s:%s --login' % (target.iqn,
                                                                                                     target.ip_address,
                                                                                                     target.port)
            self.iscsiadm_logger.info('logging into %s at %s:%s' % (target.iqn, target.ip_address, target.port))
            response = self.execute_bash_command(iscsi_adm_string)
            if response.returncode != 0:
                self.iscsiadm_logger.error('failed logging into at %s %s:%s' % (target.iqn, target.ip_address,
                                                                                target.port))
                result = 1
            else:
                self.iscsiadm_logger.info('logged into %s at %s:%s' % (target.iqn, target.ip_address, target.port))

        return result


    def logout_targets(self):
        """logs outs all targets on the instances targetList from discoverTargets"""
        result = 0
        for target in self.target_list:
            iscsi_adm_string = 'sudo iscsiadm --mode node --targetname %s --portal %s:%s --logout' % (target.iqn,
                                                                                                      target.ip_address,
                                                                                                      target.port)
            self.iscsiadm_logger.info('logout %s at %s:%s' % (target.iqn, target.ip_address, target.port))
            response = self.execute_bash_command(iscsi_adm_string)
            if response.returncode != 0:
                self.iscsiadm_logger.error('failed logging out at %s %s:%s' % (target.iqn, target.ip_address,
                                                                               target.port))
                result = 1
            else:
                self.iscsiadm_logger.info('logged out %s at %s:%s' % (target.iqn, target.ip_address, target.port))

        return result