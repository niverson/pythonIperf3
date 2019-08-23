#!/usr/bin/env python3
import logging
import signal
import concurrent.futures
from modules.scriptBaseClass import scriptBase, threadPoolListObj
from modules.iscsiadmClass import iscsiadm


# function for threading the IO clients
def discoverTargets( threadPoolObj ):
    result = threadPoolObj.iscsiadmHost.discoverTarget(threadPoolObj.targetIpAddress, threadPoolObj.port)
    return result

# function for threading the IO clients
def logIntoTargets( threadPoolObj ):
    result = threadPoolObj.iscsiadmHost.logInToTargets()
    return result

# function for threading the IO clients
def logoutTargets( threadPoolObj ):
    result = threadPoolObj.iscsiadmHost.logoutTargets()
    return result

# cleanup function to shutdown the iperf3 server
def cleanUp(iscsiAdmClientList):
    pass

def sigint_cleanup(signum, frame):
    # switch the CTRL-C handler to just exit if is pressed repeatedly
    signal.signal(signal.SIGINT, sigint_exit)
    logger.error('CTRL-C detected')
    cleanUp(iperfServer )
    exit(1)

def sigint_exit(signum, frame):
    logger.error('multiple CTRL-C detected')
    exit(2)

# setup the script object
script = scriptBase('iscsiAdm')
iscsiAdmClientList=[]


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

# setup the clean-up handler
signal.signal(signal.SIGINT, sigint_cleanup)

# create as many iscsiadm hosts as specified on the commandline and put them in an iterable object
for host in args.iscsiAdmHost:
    threadPoolObj = threadPoolListObj()
    threadPoolObj.iscsiadmHost = iscsiadm(host)
    threadPoolObj.targetIpAddress = args.target
    if args.port:
        threadPoolObj.port = args.port
    iscsiAdmClientList.append(threadPoolObj)



discoveriesThreadPool = concurrent.futures.ThreadPoolExecutor(max_workers=4)
discoveries=[]
# use the script class thread pool executor to have iscsiadm discover targets.
with discoveriesThreadPool as discoveryExecutor:
    for client in iscsiAdmClientList:
        fut = discoveryExecutor.submit(discoverTargets, client)
        discoveries.append(fut)

# As the jobs are completed, print out the results
for fut in concurrent.futures.as_completed(discoveries):
    if fut.result() != 0:
        # FIXME do something about the fail host or just continue on if not all failed?
        pass

loginsThreadPool = concurrent.futures.ThreadPoolExecutor(max_workers=4)
logins=[]
# use the script class thread pool executor to have iscsiadm discover targets.
with loginsThreadPool as loginExecutor:
    for client in iscsiAdmClientList:
        fut = loginExecutor.submit(logIntoTargets, client)
        logins.append(fut)

# As the jobs are completed, print out the results
for fut in concurrent.futures.as_completed(logins):
    if fut.result() != 0:
        # FIXME do something about the fail host or just continue on if not all failed?
        pass


logoutThreadPool = concurrent.futures.ThreadPoolExecutor(max_workers=4)
logouts=[]
# use the script class thread pool executor to have iscsiadm discover targets.
with logoutThreadPool as logoutExecutor:
    for client in iscsiAdmClientList:
        fut = logoutExecutor.submit(logoutTargets, client)
        logouts.append(fut)

# As the jobs are completed, print out the results
for fut in concurrent.futures.as_completed(logouts):
    if fut.result() != 0:
        # FIXME do something about the fail host or just continue on if not all failed?
        pass

# shutdown the iperf3 server
cleanUp(iscsiAdmClientList)


