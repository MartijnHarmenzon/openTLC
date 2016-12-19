#
import traci

#
from k0001def import inputs, outputs, appConfig, sumoConfig

#
def setSUMOInputs():
    for d in ['d011', 'd012', 'd021', 'd022', 'd031', 'd032', 'd041', 'd042', 'd051', 'd052', 'd081',
              'd082', 'd091', 'd092', 'd101', 'd102', 'd111', 'd112', 'd211', 'd241', 'd251', 'd271',
              'd311', 'd312', 'd321', 'd322', 'd331', 'd332', 'd351', 'd352', 'd361', 'd362', 'd371', 'd372']:
        try:
            if traci.areal.getLastStepOccupancy(d) > 0:
                inputs[d] = True
            else:
                inputs[d] = False
        except:
            pass

#
def setState():
    #
    state_old = list(traci.trafficlights.getRedYellowGreenState("K0001"))

    #
    for fc in appConfig['fasecycli']:
        if outputs[fc]['WR'] or outputs[fc]['RVG']:
            if sumoConfig['fasecycli'][fc]:
                for sumo in sumoConfig['fasecycli'][fc]:
                    state_old[sumo] = 'r'

        elif outputs[fc]['VG'] or outputs[fc]['VAG1'] or outputs[fc]['VAG2'] or outputs[fc]['WG'] or \
                outputs[fc]['VAG3'] or outputs[fc]['MVG'] or outputs[fc]['VAG4']:
            if sumoConfig['fasecycli'][fc]:
                for sumo in sumoConfig['fasecycli'][fc]:
                    state_old[sumo] = 'G'

        elif outputs[fc]['GL']:
            if sumoConfig['fasecycli'][fc]:
                for sumo in sumoConfig['fasecycli'][fc]:
                    state_old[sumo] = 'y'

    #
    if appConfig['simulatie']['sumo']:
        signalStateOff = [5, 15, 25]
        for signal in signalStateOff:
            state_old[signal] = 'O'

    #
    state_new = "".join(state_old)

    #
    traci.trafficlights.setRedYellowGreenState("K0001", state_new)
