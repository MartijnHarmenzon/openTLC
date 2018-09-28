# import default libraries
import time

from k0001def import appConfig, outputs, inputs, requests, sequence, wachtgroen, timers, countData, extend, \
    extend_vag1, extend_vag2, extend_vag3, extend_vag4

from k0001func import set_defaults, conflict_manager, set_remain_green, set_demand_timers, request_green, \
    sequence_evaluator, delay_manager, extend_green, conflict_status, meeverlengen

# if appConfig['automaat']['raspberry_pi']:
#     from k0001def import rpiConfig

# if appConfig['simulatie']['sumo']:
#     from k0001def import sumoConfig


#
def open_tlc(step):
    if not appConfig['simulatie']['sumo']:
        now = time.time() * 10
    else:
        now = step

    tlc_state_control = False
    tlc_state_all_off = False
    tlc_state_flashing_yellow = False
    tlc_state_all_red = False

    if not appConfig['simulatie']['sumo']:
        if inputs['is01']:
            tlc_state_all_off = True
        elif inputs['is02']:
            tlc_state_flashing_yellow = True
        elif inputs['is03']:
            tlc_state_all_red = True
        elif inputs['is04']:
            tlc_state_control = True
    else:
        tlc_state_control = True

    # tlc state - in control
    if tlc_state_control:
        set_defaults()
        # setCountData()
        conflict_manager()
        set_remain_green()

        detectors = ('d011', 'd012', 'd021', 'd022', 'd031', 'd032', 'd041', 'd042', 'd051', 'd052', 'd081', 'd082',
                     'd091', 'd092', 'd101', 'd102', 'd111', 'd112', 'd211', 'd241', 'd251', 'd271', 'd311', 'd312',
                     'd321', 'd322', 'd331', 'd332', 'd351', 'd352', 'd361', 'd362', 'd371', 'd372')

        for detector in detectors:
            set_demand_timers(detector, inputs[detector], now)

        request_green('fc01', 'd011', inputs['d011'], now)
        request_green('fc01', 'd012', inputs['d012'], now)
        request_green('fc02', 'd021', inputs['d021'], now)
        request_green('fc02', 'd022', inputs['d022'], now)
        request_green('fc03', 'd031', inputs['d031'], now)
        request_green('fc03', 'd032', inputs['d032'], now)
        request_green('fc04', 'd041', inputs['d041'], now)
        request_green('fc04', 'd042', inputs['d042'], now)
        request_green('fc05', 'd051', inputs['d051'], now)
        request_green('fc05', 'd052', inputs['d052'], now)
        request_green('fc08', 'd081', inputs['d081'], now)
        request_green('fc08', 'd082', inputs['d082'], now)
        request_green('fc09', 'd091', inputs['d091'], now)
        request_green('fc09', 'd092', inputs['d092'], now)
        request_green('fc10', 'd101', inputs['d101'], now)
        request_green('fc10', 'd102', inputs['d102'], now)
        request_green('fc11', 'd111', inputs['d111'], now)
        request_green('fc11', 'd112', inputs['d112'], now)
        request_green('fc21', 'd211', inputs['d211'], now)
        request_green('fc24', 'd241', inputs['d241'], now)
        request_green('fc25', 'd251', inputs['d251'], now)
        request_green('fc27', 'd271', inputs['d271'], now)
        request_green('fc31', 'd311', inputs['d311'], now)
        request_green('fc31', 'd312', inputs['d312'], now)
        request_green('fc32', 'd321', inputs['d321'], now)
        request_green('fc32', 'd322', inputs['d322'], now)
        request_green('fc33', 'd331', inputs['d331'], now)
        request_green('fc33', 'd332', inputs['d332'], now)
        request_green('fc35', 'd351', inputs['d351'], now)
        request_green('fc35', 'd352', inputs['d352'], now)
        request_green('fc36', 'd361', inputs['d361'], now)
        request_green('fc36', 'd362', inputs['d362'], now)
        request_green('fc37', 'd371', inputs['d371'], now)
        request_green('fc37', 'd372', inputs['d372'], now)

        # set_meeaanvragen()
        # set_cyclische_aanvragen()
        sequence_evaluator(now)
        delay_manager(now)

        extend_green('fc01', 'd011', inputs['d011'], now)
        extend_green('fc01', 'd012', inputs['d012'], now)
        extend_green('fc02', 'd021', inputs['d021'], now)
        extend_green('fc02', 'd022', inputs['d022'], now)
        extend_green('fc03', 'd031', inputs['d031'], now)
        extend_green('fc03', 'd032', inputs['d032'], now)
        extend_green('fc04', 'd041', inputs['d041'], now)
        extend_green('fc04', 'd042', inputs['d042'], now)
        extend_green('fc05', 'd051', inputs['d051'], now)
        extend_green('fc05', 'd052', inputs['d052'], now)
        extend_green('fc08', 'd081', inputs['d081'], now)
        extend_green('fc08', 'd082', inputs['d082'], now)
        extend_green('fc09', 'd091', inputs['d091'], now)
        extend_green('fc09', 'd092', inputs['d092'], now)
        extend_green('fc10', 'd101', inputs['d101'], now)
        extend_green('fc10', 'd102', inputs['d102'], now)
        extend_green('fc11', 'd111', inputs['d111'], now)
        extend_green('fc11', 'd112', inputs['d112'], now)
        extend_green('fc21', 'd211', inputs['d211'], now)
        extend_green('fc24', 'd241', inputs['d241'], now)
        extend_green('fc25', 'd251', inputs['d251'], now)
        extend_green('fc27', 'd271', inputs['d271'], now)

        # determine the state of the signal groups and set timers
        for signal_group in appConfig['fasecycli']:
            if outputs[signal_group]['WR']:
                if timers[signal_group]['GL'] > 0:
                    timers[signal_group]['GL'] = 0

                if timers[signal_group]['R'] == 0:
                    timers[signal_group]['R'] = now

                if sequence[signal_group] == 1:
                    outputs[signal_group]['WR'] = False
                    outputs[signal_group]['RVG'] = True

            if outputs[signal_group]['RVG']:
                if not conflict_status(signal_group):
                    outputs[signal_group]['RVG'] = False
                    outputs[signal_group]['VG'] = True

            if outputs[signal_group]['VG']:
                if sequence[signal_group] > 0:
                    sequence[signal_group] = 0

                if timers[signal_group]['R'] > 0:
                    timers[signal_group]['R'] = 0

                if timers[signal_group]['G'] == 0:
                    timers[signal_group]['G'] = now

                if timers[signal_group]['VG'] == 0:
                    timers[signal_group]['VG'] = now

                if timers[signal_group]['VAG1'] == 0:
                    timers[signal_group]['VAG1'] = now

                if timers[signal_group]['VAG2'] == 0:
                    timers[signal_group]['VAG2'] = now

                if timers[signal_group]['VG'] > 0 and now - timers[signal_group]['VG'] >= timers[signal_group]['basis']['vastgroen']:
                    outputs[signal_group]['VG'] = False
                    outputs[signal_group]['VAG1'] = True

            if outputs[signal_group]['VAG1']:
                if timers[signal_group]['VG'] > 0:
                    timers[signal_group]['VG'] = 0

                if not extend[signal_group] & extend_vag1 or timers[signal_group]['VAG1'] > 0 and now - timers[signal_group]['VAG1'] >= \
                        timers[signal_group]['maximum']['VAG1']:
                    outputs[signal_group]['VAG1'] = False
                    outputs[signal_group]['VAG2'] = True

            if outputs[signal_group]['VAG2']:
                if timers[signal_group]['VAG1'] > 0:
                    timers[signal_group]['VAG1'] = 0

                if not extend[signal_group] & extend_vag2 or timers[signal_group]['VAG2'] > 0 and now - timers[signal_group]['VAG2'] >= \
                        timers[signal_group]['maximum']['VAG2']:
                    outputs[signal_group]['VAG2'] = False
                    outputs[signal_group]['WG'] = True

            if outputs[signal_group]['WG']:
                if timers[signal_group]['VAG2'] > 0:
                    timers[signal_group]['VAG2'] = 0

                if not wachtgroen[signal_group]:
                    outputs[signal_group]['WG'] = False
                    outputs[signal_group]['VAG3'] = True

            if outputs[signal_group]['VAG3']:
                if timers[signal_group]['VAG3'] == 0:
                    timers[signal_group]['VAG3'] = now

                if not extend[signal_group] & extend_vag3 or timers[signal_group]['VAG3'] > 0 and now - timers[signal_group]['VAG3'] >= \
                        timers[signal_group]['maximum']['VAG3']:
                    outputs[signal_group]['VAG3'] = False
                    outputs[signal_group]['MVG'] = True

            if outputs[signal_group]['MVG']:
                if timers[signal_group]['VAG3'] > 0:
                    timers[signal_group]['VAG3'] = 0

                if not meeverlengen(signal_group):
                    outputs[signal_group]['MVG'] = False
                    outputs[signal_group]['VAG4'] = True

            if outputs[signal_group]['VAG4']:
                if timers[signal_group]['VAG4'] == 0:
                    timers[signal_group]['VAG4'] = now

                if not extend[signal_group] & extend_vag4 or timers[signal_group]['VAG4'] > 0 and now - timers[signal_group]['VAG4'] >= \
                        timers[signal_group]['maximum']['VAG4']:
                    outputs[signal_group]['VAG4'] = False
                    outputs[signal_group]['GL'] = True

            if outputs[signal_group]['GL']:
                if timers[signal_group]['G'] > 0:
                    timers[signal_group]['G'] = 0

                if timers[signal_group]['VAG4'] > 0:
                    timers[signal_group]['VAG4'] = 0

                if timers[signal_group]['GL'] == 0:
                    timers[signal_group]['GL'] = now

                if timers[signal_group]['GL'] > 0 and now - timers[signal_group]['GL'] >= timers[signal_group]['basis']['geel']:
                    outputs[signal_group]['GL'] = False
                    outputs[signal_group]['WR'] = True

        # set other outputs
        for signal_group in appConfig['fasecycli']:
            outputs[signal_group]['demand'] = requests[signal_group]
            outputs[signal_group]['sequence'] = sequence[signal_group]

            if timers[signal_group]['delay'] > 0:
                outputs[signal_group]['delay'] = now - timers[signal_group]['delay']
            else:
                outputs[signal_group]['delay'] = 0

            outputs[signal_group]['countData'] = countData[signal_group]

    # tlc state - flashing yellow
    if tlc_state_flashing_yellow:
        amber_state = False

        if step % 5 == 0:
            amber_state ^= True

        for signal_group in appConfig['fasecycli']:
            outputs[signal_group]['WR'] = False
            outputs[signal_group]['RVG'] = False
            outputs[signal_group]['VG'] = False
            outputs[signal_group]['VAG1'] = False
            outputs[signal_group]['VAG2'] = False
            outputs[signal_group]['WG'] = False
            outputs[signal_group]['VAG3'] = False
            outputs[signal_group]['MVG'] = False
            outputs[signal_group]['VAG4'] = False
            outputs[signal_group]['GL'] = amber_state
            outputs[signal_group]['demand'] = False
            outputs[signal_group]['sequence'] = 0
            outputs[signal_group]['delay'] = 0
            requests[signal_group] = False
            sequence[signal_group] = 0
            timers[signal_group]['delay'] = 0

    # tlc state - all red
    if tlc_state_all_red:
        for signal_group in appConfig['fasecycli']:
            outputs[signal_group]['WR'] = True
            outputs[signal_group]['RVG'] = False
            outputs[signal_group]['VG'] = False
            outputs[signal_group]['VAG1'] = False
            outputs[signal_group]['VAG2'] = False
            outputs[signal_group]['WG'] = False
            outputs[signal_group]['VAG3'] = False
            outputs[signal_group]['MVG'] = False
            outputs[signal_group]['VAG4'] = False
            outputs[signal_group]['GL'] = False
            outputs[signal_group]['demand'] = False
            outputs[signal_group]['sequence'] = 0
            outputs[signal_group]['delay'] = 0
            requests[signal_group] = False
            sequence[signal_group] = 0
            timers[signal_group]['delay'] = 0

    # tlc state - all off
    if tlc_state_all_off:
        for signal_group in appConfig['fasecycli']:
            outputs[signal_group]['WR'] = False
            outputs[signal_group]['RVG'] = False
            outputs[signal_group]['VG'] = False
            outputs[signal_group]['VAG1'] = False
            outputs[signal_group]['VAG2'] = False
            outputs[signal_group]['WG'] = False
            outputs[signal_group]['VAG3'] = False
            outputs[signal_group]['MVG'] = False
            outputs[signal_group]['VAG4'] = False
            outputs[signal_group]['GL'] = False
            outputs[signal_group]['demand'] = False
            outputs[signal_group]['sequence'] = 0
            outputs[signal_group]['delay'] = 0
            requests[signal_group] = False
            sequence[signal_group] = 0
            timers[signal_group]['delay'] = 0
