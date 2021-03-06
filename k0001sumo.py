# import libraries SUMO/TraCI
from __future__ import absolute_import
from __future__ import print_function
import traci

# import libraries openTLC
from k0001func import initialise
from k0001app import open_tlc
from k0001sumofunc import set_sumo_inputs, set_state

# import libraries other
import optparse
import os
import subprocess
import sys
# import time
# import random


# the port used for communicating with your sumo instance
traci_port = 8873


# we need to import python modules from the $SUMO_HOME/tools directory
try:
    sys.path.append(os.path.join(os.path.dirname(
        __file__), '..', '..', '..', '..', "tools"))  # tutorial in tests
    sys.path.append(os.path.join(os.environ.get("SUMO_HOME", os.path.join(
        os.path.dirname(__file__), "..", "..", "..")), "tools"))  # tutorial in docs
    from sumolib import checkBinary
except ImportError:
    sys.exit(
        """please declare environment variable 'SUMO_HOME' as the root directory of your sumo installation 
           (it should contain folders 'bin', 'tools' and 'docs')"""
    )


#
def run():
    #
    traci.init(traci_port)

    #
    step = 0
    # amber_state = False

    #
    initialise()

    #
    while traci.simulation.getMinExpectedNumber() > 0:
        #
        traci.simulationStep()

        #
        # if step % 5 == 0:
        #     amber_state ^= True

        #
        set_sumo_inputs()

        #
        open_tlc(step)
        # open_tlc(step, amber_state)

        #
        set_state()

        #
        step += 1

    #
    traci.close()
    sys.stdout.flush()


#
def get_options():
    opt_parser = optparse.OptionParser()
    opt_parser.add_option("--nogui", action="store_true", default=False, help="run the commandline version of sumo")
    options, args = opt_parser.parse_args()
    return options


# this is the main entry point of this script
if __name__ == "__main__":
    # this script has been called from the command line. It will start sumo as a server, then connect and run
    if get_options().nogui:
        sumo_binary = checkBinary('sumo')
    else:
        sumo_binary = checkBinary('sumo-gui')

    # first, generate the route file for this simulation generate_routefile()

    # this is the normal way of using traci. sumo is started as a subprocess and then the python script connects and
    # runs sumoProcess = subprocess.Popen([sumoBinary, "-c", "data/MAP_K0001.sumo.cfg", "--tripinfo-output",
    # "tripinfo.xml", "--remote-port", str(PORT)], stdout=sys.stdout, stderr=sys.stderr)

    sumo_process = subprocess.Popen([sumo_binary, "-c", "SUMO/k0001.sumocfg", "--remote-port", str(traci_port)],
                                    stdout=sys.stdout, stderr=sys.stderr)
    run()
    sumo_process.wait()
