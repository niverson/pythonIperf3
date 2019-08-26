#!/usr/bin/env python3
import logging
import signal
import concurrent.futures
from modules.scriptBaseClass import scriptBase, threadPoolListObj
from modules.iperfClientClass import iperfClient
from modules.iperfServerClass import iperfServer

# function for threading the IO clients
def startClientIo( threadPoolObj ):
    result = threadPoolObj.clientObj.startIperf3Client(threadPoolObj.targetIpAddress, threadPoolObj.port)
    return result

# cleanup function to shutdown the iperf3 server
def cleanUp(iperfTarget):
    result = iperfTarget.stopIperf3ServerDaemon()
    return result

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
executableName = 'iperf3'
script = scriptBase(executableName)
iperfClientList=[]
iperfTarget = None

# add other arguments here to supplement the default arguments in the script base class
script.parser.add_argument('-p','--port', help="iperf3 server user defined port", type=int)
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

iperf3Port = 5201  # this is the default value
if args.port:
    iperf3Port = args.port

returncode = 0

# create the iperf3 target object to test against
iperfTarget = iperfServer(args.server)

# create as many clients as specified on the commandline and put them in an iterable object
for client in args.client:
    threadPoolObj = threadPoolListObj()
    logfile = f"{script.logfileDirectory}/{executableName}_{client}__{script.utcNow.strftime('%Y_%m_%d__%H_%M_%S')}.dat"
    threadPoolObj.clientObj = iperfClient(client, logfile)
    threadPoolObj.targetIpAddress = args.server
    threadPoolObj.port = iperf3Port
    iperfClientList.append(threadPoolObj)

# start the iperf3 server
result = iperfTarget.startIperf3ServerDaemon(iperf3Port)

# check that the server returned success
if result.returncode != 0:
    returncode |= result.returncode

iperfClientThreadPool = concurrent.futures.ThreadPoolExecutor(max_workers=4)
futures=[]
# use the thread pool executor to have the iperf3 clients stream data
with iperfClientThreadPool as executor:
    for client in iperfClientList:
        fut = executor.submit(startClientIo, client)
        futures.append(fut)

# As the jobs are completed, check the results
for fut in concurrent.futures.as_completed(futures):
    if fut.result():
        returncode |= fut.result().returncode
        if returncode != 0:
            logger.error( fut.result() )

# shutdown the iperf3 server
returncode |= cleanUp(iperfTarget)

exit(returncode)


