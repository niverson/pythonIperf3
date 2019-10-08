#!/usr/bin/env python3

"""methodDispatchExample script.
This script uses objects that have singleDispatch extended to be used in instances to overload functions.
"""

import logging
import random
from modules.scriptBaseClass import ScriptBase
from modules.fcSwitchClass import FcSwitchClass
from modules.iscsiSwitchClass import IscsiSwitchClass

# setup the script object
executable_name = 'methodDispatchExample'
script = ScriptBase(executable_name)

# add other arguments here to supplement the default arguments in the script base class
script.parser.add_argument('ipAddress', help="switch ipAddress", type=str)

# accumulate the arguments into an object
args = script.parser.parse_args()

# initialize the script logging once.
script.set_logging(args.slvl, args.flvl)

# create the logger object for this file
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# could write a factory class that uses a database(or some other means) to look up the object that needs
# to be create based on the ipAddress.
# Then we can create a factory object and pass in the ipAddress to the factory object and have the
# factory object return the proper switch_under_test object.
# for now fake it
sut = None
if (random.randint(0,1) == 0):
    sut = IscsiSwitchClass(args.ipAddress)
else:
    sut = FcSwitchClass(args.ipAddress)

sut.port_manager.turn_off_port(sut.com_obj, 23)
sut.port_manager.turn_on_port(sut.com_obj, 23)
