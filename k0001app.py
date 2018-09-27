# import default libraries
import time

from k0001def import appConfig, outputs, inputs, demands, sequence, wachtgroen, timers, countData, \
    extend, BIT1, BIT2, BIT3, BIT4

from k0001func import initialise, reset, set_conflicts, set_wachtgroen, detectietijden, aanvragen, \
    set_sequence, set_delay, verlengen, conflict_status, meeverlengen

if appConfig['automaat']['raspberry_pi']:
    from k0001def import rpiConfig

if appConfig['simulatie']['sumo']:
    from k0001def import sumoConfig


#
def openTLC(step, amberState):
    if not appConfig['simulatie']['sumo']:
        now = time.time() * 10
    else:
        now = step

    doven = False
    regelen = False
    geelKnipperen = False
    allesRood = False

    if not appConfig['simulatie']['sumo']:
        if inputs['is01']:
            doven = True
        elif inputs['is02']:
            geelKnipperen = True
        elif inputs['is03']:
            allesRood = True
        elif inputs['is04']:
            regelen = True
    else:
        regelen = True

    # regelen
    if regelen:
        reset()
        # setCountData()
        set_conflicts()
        set_wachtgroen()

        for d in ['d011', 'd012', 'd021', 'd022', 'd031', 'd032', 'd041', 'd042', 'd051', 'd052', 'd081', 'd082',
                  'd091', 'd092', 'd101', 'd102', 'd111', 'd112', 'd211', 'd241', 'd251', 'd271', 'd311', 'd312',
                  'd321', 'd322', 'd331', 'd332', 'd351', 'd352', 'd361', 'd362', 'd371', 'd372']:
            detectietijden(d, inputs[d], now)

        aanvragen('fc01', 'd011', inputs['d011'], now)
        aanvragen('fc01', 'd012', inputs['d012'], now)
        aanvragen('fc02', 'd021', inputs['d021'], now)
        aanvragen('fc02', 'd022', inputs['d022'], now)
        aanvragen('fc03', 'd031', inputs['d031'], now)
        aanvragen('fc03', 'd032', inputs['d032'], now)
        aanvragen('fc04', 'd041', inputs['d041'], now)
        aanvragen('fc04', 'd042', inputs['d042'], now)
        aanvragen('fc05', 'd051', inputs['d051'], now)
        aanvragen('fc05', 'd052', inputs['d052'], now)
        aanvragen('fc08', 'd081', inputs['d081'], now)
        aanvragen('fc08', 'd082', inputs['d082'], now)
        aanvragen('fc09', 'd091', inputs['d091'], now)
        aanvragen('fc09', 'd092', inputs['d092'], now)
        aanvragen('fc10', 'd101', inputs['d101'], now)
        aanvragen('fc10', 'd102', inputs['d102'], now)
        aanvragen('fc11', 'd111', inputs['d111'], now)
        aanvragen('fc11', 'd112', inputs['d112'], now)
        aanvragen('fc21', 'd211', inputs['d211'], now)
        aanvragen('fc24', 'd241', inputs['d241'], now)
        aanvragen('fc25', 'd251', inputs['d251'], now)
        aanvragen('fc27', 'd271', inputs['d271'], now)
        aanvragen('fc31', 'd311', inputs['d311'], now)
        aanvragen('fc31', 'd312', inputs['d312'], now)
        aanvragen('fc32', 'd321', inputs['d321'], now)
        aanvragen('fc32', 'd322', inputs['d322'], now)
        aanvragen('fc33', 'd331', inputs['d331'], now)
        aanvragen('fc33', 'd332', inputs['d332'], now)
        aanvragen('fc35', 'd351', inputs['d351'], now)
        aanvragen('fc35', 'd352', inputs['d352'], now)
        aanvragen('fc36', 'd361', inputs['d361'], now)
        aanvragen('fc36', 'd362', inputs['d362'], now)
        aanvragen('fc37', 'd371', inputs['d371'], now)
        aanvragen('fc37', 'd372', inputs['d372'], now)

        # set_meeaanvragen()
        # set_cyclische_aanvragen()
        set_sequence(now)
        set_delay(now)

        verlengen('fc01', 'd011', inputs['d011'], now)
        verlengen('fc01', 'd012', inputs['d012'], now)
        verlengen('fc02', 'd021', inputs['d021'], now)
        verlengen('fc02', 'd022', inputs['d022'], now)
        verlengen('fc03', 'd031', inputs['d031'], now)
        verlengen('fc03', 'd032', inputs['d032'], now)
        verlengen('fc04', 'd041', inputs['d041'], now)
        verlengen('fc04', 'd042', inputs['d042'], now)
        verlengen('fc05', 'd051', inputs['d051'], now)
        verlengen('fc05', 'd052', inputs['d052'], now)
        verlengen('fc08', 'd081', inputs['d081'], now)
        verlengen('fc08', 'd082', inputs['d082'], now)
        verlengen('fc09', 'd091', inputs['d091'], now)
        verlengen('fc09', 'd092', inputs['d092'], now)
        verlengen('fc10', 'd101', inputs['d101'], now)
        verlengen('fc10', 'd102', inputs['d102'], now)
        verlengen('fc11', 'd111', inputs['d111'], now)
        verlengen('fc11', 'd112', inputs['d112'], now)
        verlengen('fc21', 'd211', inputs['d211'], now)
        verlengen('fc24', 'd241', inputs['d241'], now)
        verlengen('fc25', 'd251', inputs['d251'], now)
        verlengen('fc27', 'd271', inputs['d271'], now)

        # verander de status van de lantaarns
        for fc in appConfig['fasecycli']:
            if outputs[fc]['WR']:
                if timers[fc]['GL'] > 0:
                    timers[fc]['GL'] = 0

                if timers[fc]['R'] == 0:
                    timers[fc]['R'] = now

                if sequence[fc] == 1:
                    outputs[fc]['WR'] = False
                    outputs[fc]['RVG'] = True

            if outputs[fc]['RVG']:
                if not conflict_status(fc):
                    outputs[fc]['RVG'] = False
                    outputs[fc]['VG'] = True

            if outputs[fc]['VG']:
                if sequence[fc] > 0:
                    sequence[fc] = 0

                if timers[fc]['R'] > 0:
                    timers[fc]['R'] = 0

                if timers[fc]['G'] == 0:
                    timers[fc]['G'] = now

                if timers[fc]['VG'] == 0:
                    timers[fc]['VG'] = now

                if timers[fc]['VAG1'] == 0:
                    timers[fc]['VAG1'] = now

                if timers[fc]['VAG2'] == 0:
                    timers[fc]['VAG2'] = now

                if timers[fc]['VG'] > 0 and now - timers[fc]['VG'] >= timers[fc]['basis']['vastgroen']:
                    outputs[fc]['VG'] = False
                    outputs[fc]['VAG1'] = True

            if outputs[fc]['VAG1']:
                if timers[fc]['VG'] > 0:
                    timers[fc]['VG'] = 0

                if not extend[fc] & BIT1 or timers[fc]['VAG1'] > 0 and now - timers[fc]['VAG1'] >= \
                        timers[fc]['maximum']['VAG1']:
                    outputs[fc]['VAG1'] = False
                    outputs[fc]['VAG2'] = True

            if outputs[fc]['VAG2']:
                if timers[fc]['VAG1'] > 0:
                    timers[fc]['VAG1'] = 0

                if not extend[fc] & BIT2 or timers[fc]['VAG2'] > 0 and now - timers[fc]['VAG2'] >= \
                        timers[fc]['maximum']['VAG2']:
                    outputs[fc]['VAG2'] = False
                    outputs[fc]['WG'] = True

            if outputs[fc]['WG']:
                if timers[fc]['VAG2'] > 0:
                    timers[fc]['VAG2'] = 0

                if not wachtgroen[fc]:
                    outputs[fc]['WG'] = False
                    outputs[fc]['VAG3'] = True

            if outputs[fc]['VAG3']:
                if timers[fc]['VAG3'] == 0:
                    timers[fc]['VAG3'] = now

                if not extend[fc] & BIT3 or timers[fc]['VAG3'] > 0 and now - timers[fc]['VAG3'] >= \
                        timers[fc]['maximum']['VAG3']:
                    outputs[fc]['VAG3'] = False
                    outputs[fc]['MVG'] = True

            if outputs[fc]['MVG']:
                if timers[fc]['VAG3'] > 0:
                    timers[fc]['VAG3'] = 0

                if not meeverlengen(fc):
                    outputs[fc]['MVG'] = False
                    outputs[fc]['VAG4'] = True

            if outputs[fc]['VAG4']:
                if timers[fc]['VAG4'] == 0:
                    timers[fc]['VAG4'] = now

                if not extend[fc] & BIT4 or timers[fc]['VAG4'] > 0 and now - timers[fc]['VAG4'] >= \
                        timers[fc]['maximum']['VAG4']:
                    outputs[fc]['VAG4'] = False
                    outputs[fc]['GL'] = True

            if outputs[fc]['GL']:
                if timers[fc]['G'] > 0:
                    timers[fc]['G'] = 0

                if timers[fc]['VAG4'] > 0:
                    timers[fc]['VAG4'] = 0

                if timers[fc]['GL'] == 0:
                    timers[fc]['GL'] = now

                if timers[fc]['GL'] > 0 and now - timers[fc]['GL'] >= timers[fc]['basis']['geel']:
                    outputs[fc]['GL'] = False
                    outputs[fc]['WR'] = True

        #
        for fc in appConfig['fasecycli']:
            outputs[fc]['demand'] = demands[fc]
            outputs[fc]['sequence'] = sequence[fc]
            if timers[fc]['delay'] > 0:
                outputs[fc]['delay'] = now - timers[fc]['delay']
            else:
                outputs[fc]['delay'] = 0
            outputs[fc]['countData'] = countData[fc]

    # geel knipperen
    if geelKnipperen:
        if step % 5 == 0:
            amberState ^= True

        for fc in appConfig['fasecycli']:
            outputs[fc]['WR'] = False
            outputs[fc]['RVG'] = False
            outputs[fc]['VG'] = False
            outputs[fc]['VAG1'] = False
            outputs[fc]['VAG2'] = False
            outputs[fc]['WG'] = False
            outputs[fc]['VAG3'] = False
            outputs[fc]['MVG'] = False
            outputs[fc]['VAG4'] = False
            outputs[fc]['GL'] = amberState
            outputs[fc]['demand'] = False
            outputs[fc]['sequence'] = 0
            outputs[fc]['delay'] = 0
            demands[fc] = False
            sequence[fc] = 0
            timers[fc]['delay'] = 0

    # alles rood
    if allesRood:
        for fc in appConfig['fasecycli']:
            outputs[fc]['WR'] = True
            outputs[fc]['RVG'] = False
            outputs[fc]['VG'] = False
            outputs[fc]['VAG1'] = False
            outputs[fc]['VAG2'] = False
            outputs[fc]['WG'] = False
            outputs[fc]['VAG3'] = False
            outputs[fc]['MVG'] = False
            outputs[fc]['VAG4'] = False
            outputs[fc]['GL'] = False
            outputs[fc]['demand'] = False
            outputs[fc]['sequence'] = 0
            outputs[fc]['delay'] = 0
            demands[fc] = False
            sequence[fc] = 0
            timers[fc]['delay'] = 0

    # doven
    if doven:
        for fc in appConfig['fasecycli']:
            outputs[fc]['WR'] = False
            outputs[fc]['RVG'] = False
            outputs[fc]['VG'] = False
            outputs[fc]['VAG1'] = False
            outputs[fc]['VAG2'] = False
            outputs[fc]['WG'] = False
            outputs[fc]['VAG3'] = False
            outputs[fc]['MVG'] = False
            outputs[fc]['VAG4'] = False
            outputs[fc]['GL'] = False
            outputs[fc]['demand'] = False
            outputs[fc]['sequence'] = 0
            outputs[fc]['delay'] = 0
            demands[fc] = False
            sequence[fc] = 0
            timers[fc]['delay'] = 0
