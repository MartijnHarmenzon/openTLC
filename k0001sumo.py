# import libraries SUMO/TraCI
from __future__ import absolute_import
from __future__ import print_function

import optparse, os, subprocess, sys, time, random

# we need to import python modules from the $SUMO_HOME/tools directory
try:
    sys.path.append(os.path.join(os.path.dirname(
        __file__), '..', '..', '..', '..', "tools"))  # tutorial in tests
    sys.path.append(os.path.join(os.environ.get("SUMO_HOME", os.path.join(
        os.path.dirname(__file__), "..", "..", "..")), "tools"))  # tutorial in docs
    from sumolib import checkBinary
except ImportError:
    sys.exit(
        "please declare environment variable 'SUMO_HOME' as the root directory of your sumo installation (it should contain folders 'bin', 'tools' and 'docs')")

import traci
# the port used for communicating with your sumo instance
PORT = 8873

#
from k0001func import initialise
from k0001app import openTLC
from k0001sumofunc import setSUMOInputs, setState

#
def run():
    #
    traci.init(PORT)

    #
    step = 0
    amberState = False

    #
    initialise()

    #
    while traci.simulation.getMinExpectedNumber() > 0:
        #
        traci.simulationStep()

        #
        if step % 5 == 0:
            amberState ^= True

        #
        setSUMOInputs()

        #
        openTLC(step, amberState)

        #
        setState()

        #
        step += 1

    #
    traci.close()
    sys.stdout.flush()

#
def get_options():
    optParser = optparse.OptionParser()
    optParser.add_option("--nogui", action="store_true",
                         default=False, help="run the commandline version of sumo")
    options, args = optParser.parse_args()
    return options

# this is the main entry point of this script
if __name__ == "__main__":
    options = get_options()

    # this script has been called from the command line. It will start sumo as a
    # server, then connect and run
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    # first, generate the route file for this simulation
    # generate_routefile()

    # this is the normal way of using traci. sumo is started as a
    # subprocess and then the python script connects and runs
    # sumoProcess = subprocess.Popen([sumoBinary, "-c", "data/MAP_K0001.sumo.cfg", "--tripinfo-output",
    #                                 "tripinfo.xml", "--remote-port", str(PORT)], stdout=sys.stdout, stderr=sys.stderr)

    sumoProcess = subprocess.Popen([sumoBinary, "-c", "SUMO/k0001.sumocfg", "--remote-port", str(PORT)],
                                   stdout=sys.stdout, stderr=sys.stderr)
    run()
    sumoProcess.wait()
