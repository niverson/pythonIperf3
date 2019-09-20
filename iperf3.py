#!/usr/bin/env python3

"""iperf3 test script.
This script allows the user to run a quick iperf3 test from a client on one system to the server on another system.
"""
import logging
import signal
from multiprocessing import Process
import concurrent.futures
from modules.scriptBaseClass import ScriptBase
from modules.iperfClientClass import IperfClient
from modules.iperfServerClass import IperfServer


class PoolListObj():
    pass

# function for threading the IO clients
def start_client_io(pool_obj):
    result = pool_obj.client_obj.start_iperf3_client(pool_obj.target_ip_address, pool_obj.useJson, pool_obj.port )
    return result

def start_client_io_process(pool_obj):
    result = start_client_io(pool_obj)
    exit(result.returncode)

# cleanup function to shutdown the iperf3 server
def clean_up(iperf_target):
    result = iperf_target.stop_iperf3_server_daemon()
    return result

def sigint_cleanup(signum, frame):
    # switch the CTRL-C handler to just exit if is pressed repeatedly
    signal.signal(signal.SIGINT, sigint_exit)
    logger.error('CTRL-C detected')
    clean_up(iperf_server)
    exit(1)

def sigint_exit(signum, frame):
    logger.error('multiple CTRL-C detected')
    exit(2)

# setup the script object
executable_name = 'iperf3'
script = ScriptBase(executable_name)
iperf_client_list=[]
iperf_target = None

# add other arguments here to supplement the default arguments in the script base class
script.parser.add_argument('-t','--thread', help="iperf3 client runs in a thread, instead of a process",
                           action="store_true")
script.parser.add_argument('-p','--port', help="iperf3 server user defined port", type=int)
script.parser.add_argument('-j','--useJson', help="iperf3 client return data in json", action="store_true")
script.parser.add_argument('server', help="iperf3 server ipAddress", type=str)
script.parser.add_argument('client', help="iperf3 client ipAddress", type=str)

# accumulate the arguments into an object
args = script.parser.parse_args()

# initialize the script logging once.
script.set_logging(args.slvl, args.flvl)

# create the logger object for this file
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# setup the clean-up handler
signal.signal(signal.SIGINT, sigint_cleanup)

iperf3_port = 5201  # this is the default value
if args.port:
    iperf3_port = args.port

returncode = 0

# create the iperf3 target object to test against
iperf_target = IperfServer(args.server)


# create a client as specified on the commandline and put them in an iterable object
pool_obj = PoolListObj()
logfile = f"{script.log_file_directory}/{executable_name}_{args.client}__{script.utcNow.strftime('%Y_%m_%d__%H_%M_%S')}.dat"
pool_obj.client_obj = IperfClient(args.client, logfile)
pool_obj.target_ip_address = args.server
pool_obj.port = iperf3_port
pool_obj.useJson = args.useJson
iperf_client_list.append(pool_obj)


# start the iperf3 server
result = iperf_target.start_iperf3_server_daemon(iperf3_port)

# check that the server returned success
if result.returncode != 0:
    returncode |= result.returncode


# A. using a process to run iperf3 client
if __name__ == '__main__' and not args.thread:
    processes = []
    for client in iperf_client_list:
        proc = Process(target=start_client_io_process, args=(client,))
        proc.start()
        processes.append(proc)

    for proc in processes:
        proc.join()
        if proc.exitcode:
            logger.error(f'{executable_name} returned {proc.exitcode}')
        else:
            logger.info(f'process based {executable_name} completed successfully')

        returncode |= proc.exitcode

else:
    # OR B. using a thread pool to run iperf3 client
    iperf_client_pool = concurrent.futures.ThreadPoolExecutor(max_workers=4)
    futures=[]
    # use the thread pool executor to have the iperf3 clients stream data
    with iperf_client_pool as executor:
        for client in iperf_client_list:
            fut = executor.submit(start_client_io, client)
            futures.append(fut)

    # As the jobs are completed, check the results
    for fut in concurrent.futures.as_completed(futures):
        if fut.result():
            returncode |= fut.result().returncode
            if returncode != 0:
                logger.error(fut.result())
            else:
                logger.info(f'thread based {executable_name} completed successfully')

# shutdown the iperf3 server
returncode |= clean_up(iperf_target)

exit(returncode)


