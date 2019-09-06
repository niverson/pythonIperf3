#!/usr/bin/env python3

"""iscsiadm script.
This script allows the user to perform an iscsi discovery and login from an iscsi initiator to an iscsi target
on another system.
The iscsi target has to be previously setup to allow the initiator to login with the proper credentials.
"""

import logging
import signal
import concurrent.futures
from modules.scriptBaseClass import ScriptBase
from modules.iscsiadmClass import Iscsiadm


class PoolListObj():
    pass

# function for threading the IO clients
def discover_targets( pool_obj ):
    result = pool_obj.iscsiadm_host.discover_target(pool_obj.target_ip_address, pool_obj.port)
    return result

# function for threading the IO clients
def log_in_to_targets( pool_obj ):
    result = pool_obj.iscsiadm_host.log_in_to_targets()
    return result

# function for threading the IO clients
def logout_targets( pool_obj ):
    result = pool_obj.iscsiadm_host.logout_targets()
    return result

# cleanup function to shutdown the iperf3 server
def clean_up(iscsi_adm_client_list):
    pass

def sigint_cleanup(signum, frame):
    # switch the CTRL-C handler to just exit if is pressed repeatedly
    signal.signal(signal.SIGINT, sigint_exit)
    logger.error('CTRL-C detected')
    clean_up(iscsiadm_client_list )
    exit(1)

def sigint_exit(signum, frame):
    logger.error('multiple CTRL-C detected')
    exit(2)

# setup the script object
executable_name = 'iscsiadm'
script = ScriptBase(executable_name)

# add other arguments here to supplement the default arguments in the script base class
script.parser.add_argument('-port', help="iscsi target user defined port", type=int)
script.parser.add_argument('target', help="iscsi target ipAddress", type=str)
script.parser.add_argument('iscsiAdmHost', help="iscsiadm host ipAddress", type=str, nargs='*')

# accumulate the arguments into an object
args = script.parser.parse_args()

# initialize the script logging once.
script.set_logging(args.slvl, args.flvl)

# create the logger object for this file
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

iscsiadm_client_list=[]
returncode = 0

iscsi_target_port = 3260  # this is the default value
if args.port:
    iscsi_target_port = args.port

# setup the clean-up handler
signal.signal(signal.SIGINT, sigint_cleanup)

# create as many iscsiadm hosts as specified on the commandline and put them in an iterable object
for host in args.iscsiAdmHost:
    pool_obj = PoolListObj()
    pool_obj.iscsiadm_host = Iscsiadm(host)
    pool_obj.target_ip_address = args.target
    pool_obj.port = iscsi_target_port
    iscsiadm_client_list.append(pool_obj)



discoveries_thread_pool = concurrent.futures.ThreadPoolExecutor(max_workers=4)
discoveries=[]
# use the discoveries thread pool executor to have iscsiadm discover targets.
with discoveries_thread_pool as discovery_executor:
    for client in iscsiadm_client_list:
        fut = discovery_executor.submit(discover_targets, client)
        discoveries.append(fut)

# As the jobs are completed, print out the results
for fut in concurrent.futures.as_completed(discoveries):
    if fut.result() != 0:
        returncode |= fut.result()


logins_thread_pool = concurrent.futures.ThreadPoolExecutor(max_workers=4)
logins=[]
# use the logins thread pool executor to have iscsiadm log in to the targets.
with logins_thread_pool as login_executor:
    for client in iscsiadm_client_list:
        fut = login_executor.submit(log_in_to_targets, client)
        logins.append(fut)

# As the jobs are completed, print out the results
for fut in concurrent.futures.as_completed(logins):
    if fut.result() != 0:
        returncode |= fut.result()



# FIXME add code here to run IO to the targets from or do some other testing


logout_thread_pool = concurrent.futures.ThreadPoolExecutor(max_workers=4)
logouts=[]
# use the logout thread pool executor to have iscsiadm logout all known targets.
with logout_thread_pool as logout_executor:
    for client in iscsiadm_client_list:
        fut = logout_executor.submit(logout_targets, client)
        logouts.append(fut)

# As the jobs are completed, print out the results
for fut in concurrent.futures.as_completed(logouts):
    if fut.result() != 0:
        returncode |= fut.result()

# shutdown the iperf3 server
clean_up(iscsiadm_client_list)

exit(returncode)


