#!/usr/bin/env python3
import logging
import signal
from concurrent.futures import as_completed
from modules.scriptBaseClass import scriptBase, threadPoolListObj
from modules.iperfClientClass import iperfClient
from modules.iperfServerClass import iperfServer

# function for threading the IO clients
def startClientIo( threadPoolObj ):
    result = threadPoolObj.clientObj.startIperf3Client(threadPoolObj.targetIpAddress)
    return result

# cleanup function to shutdown the iperf3 server
def cleanUp(iperfTarget):
    iperfTarget.stopIperf3ServerDaemon()

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
script = scriptBase('iperf3')
iperfClientList=[]
iperfTarget = None

# add other arguments here to supplement the default arguments in the script base class
script.parser.add_argument('-p', help="iperf3 server user defined port", type=int)
script.parser.add_argument('server', help="iperf3 server ipAddress", type=str)
script.parser.add_argument('client', help="iperf3 client ipAddress", type=str, nargs='*')

# accumulate the arguments into an object
args = script.parser.parse_args()

# initialize the script logging once.
script.setLogging(args.slvl,args.flvl)

# create the logger object for this file
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# setup the clean-up handler
signal.signal(signal.SIGINT, sigint_cleanup)

# create the iperf3 object to test
iperfTarget = iperfServer(args.server)

# create as many clients as specified on the commandline and put them in an iterable object
for client in args.client:
    threadPoolObj = threadPoolListObj()
    threadPoolObj.clientObj = iperfClient(client)
    threadPoolObj.targetIpAddress = args.server
    iperfClientList.append(threadPoolObj)


# start the iperf3 server
iperfTarget.startIperf3ServerDaemon()

futures=[]
# use the script class thread pool executor to have the iperf3 clients stream data
with script.threadPool as executor:
    for client in iperfClientList:
        fut = executor.submit(startClientIo, client)
        futures.append(fut)

# As the jobs are completed, print out the results
for fut in as_completed(futures):
    print(fut.result())

# shutdown the iperf3 server
cleanUp(iperfTarget)

