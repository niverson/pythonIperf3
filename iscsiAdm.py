#!/usr/bin/env python3
import logging
import signal
import concurrent.futures
from modules.scriptBaseClass import scriptBase
from modules.iscsiadmClass import iscsiadm


class poolListObj():
    pass

# function for threading the IO clients
def discoverTargets( poolObj ):
    result = poolObj.iscsiadmHost.discoverTarget(poolObj.targetIpAddress, poolObj.port)
    return result

# function for threading the IO clients
def logIntoTargets( poolObj ):
    result = poolObj.iscsiadmHost.logInToTargets()
    return result

# function for threading the IO clients
def logoutTargets( poolObj ):
    result = poolObj.iscsiadmHost.logoutTargets()
    return result

# cleanup function to shutdown the iperf3 server
def cleanUp(iscsiAdmClientList):
    pass

def sigint_cleanup(signum, frame):
    # switch the CTRL-C handler to just exit if is pressed repeatedly
    signal.signal(signal.SIGINT, sigint_exit)
    logger.error('CTRL-C detected')
    cleanUp(iscsiAdmClientList )
    exit(1)

def sigint_exit(signum, frame):
    logger.error('multiple CTRL-C detected')
    exit(2)

# setup the script object
executableName = 'iscsiadm'
script = scriptBase(executableName)

# add other arguments here to supplement the default arguments in the script base class
script.parser.add_argument('-port', help="iscsi target user defined port", type=int)
script.parser.add_argument('target', help="iscsi target ipAddress", type=str)
script.parser.add_argument('iscsiAdmHost', help="iscsiadm host ipAddress", type=str, nargs='*')

# accumulate the arguments into an object
args = script.parser.parse_args()

# initialize the script logging once.
script.setLogging(args.slvl,args.flvl)

# create the logger object for this file
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

iscsiAdmClientList=[]
returncode = 0

iscsiTargetPort = 3260  # this is the default value
if args.port:
    iscsiTargetPort = args.port

# setup the clean-up handler
signal.signal(signal.SIGINT, sigint_cleanup)

# create as many iscsiadm hosts as specified on the commandline and put them in an iterable object
for host in args.iscsiAdmHost:
    poolObj = poolListObj()
    poolObj.iscsiadmHost = iscsiadm(host)
    poolObj.targetIpAddress = args.target
    poolObj.port = iscsiTargetPort
    iscsiAdmClientList.append(poolObj)



discoveriesThreadPool = concurrent.futures.ThreadPoolExecutor(max_workers=4)
discoveries=[]
# use the discoveries thread pool executor to have iscsiadm discover targets.
with discoveriesThreadPool as discoveryExecutor:
    for client in iscsiAdmClientList:
        fut = discoveryExecutor.submit(discoverTargets, client)
        discoveries.append(fut)

# As the jobs are completed, print out the results
for fut in concurrent.futures.as_completed(discoveries):
    if fut.result() != 0:
        returncode |= fut.result()


loginsThreadPool = concurrent.futures.ThreadPoolExecutor(max_workers=4)
logins=[]
# use the logins thread pool executor to have iscsiadm log in to the targets.
with loginsThreadPool as loginExecutor:
    for client in iscsiAdmClientList:
        fut = loginExecutor.submit(logIntoTargets, client)
        logins.append(fut)

# As the jobs are completed, print out the results
for fut in concurrent.futures.as_completed(logins):
    if fut.result() != 0:
        returncode |= fut.result()



# FIXME add code here to run IO to the targets from or do some other testing


logoutThreadPool = concurrent.futures.ThreadPoolExecutor(max_workers=4)
logouts=[]
# use the logout thread pool executor to have iscsiadm logout all known targets.
with logoutThreadPool as logoutExecutor:
    for client in iscsiAdmClientList:
        fut = logoutExecutor.submit(logoutTargets, client)
        logouts.append(fut)

# As the jobs are completed, print out the results
for fut in concurrent.futures.as_completed(logouts):
    if fut.result() != 0:
        returncode |= fut.result()

# shutdown the iperf3 server
cleanUp(iscsiAdmClientList)

exit(returncode)


