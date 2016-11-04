# import default libraries
import yaml,time,json


# import defines MAPtm
from k0001def import appConfig, outputs, inputs, demands, conflicts, sequence, wachtgroen, timers, countData, \
    extend, BIT1, BIT2, BIT3, BIT4


# import functions MAPtm
from k0001func import initialise, reset, set_conflicts, set_wachtgroen, detectietijden, aanvragen, \
    set_meeaanvragen, set_cyclische_aanvragen, set_sequence, setDelay, verlengen, conflictStatus, meeverlengen

if appConfig['automaat']['raspberry_pi']:
    from k0001def import rpiConfig

if appConfig['simulatie']['sumo']:
    from k0001def import sumoConfig


# Raspberry Pi settings
if appConfig['automaat']['raspberry_pi']:
    print('TLC started...')

    import wiringpi

    # initialise wiringpi
    wiringpi.wiringPiSetup()

    if 'wiringpi' in rpiConfig:
        for wiringpiConfig in rpiConfig['wiringpi']:
            # lowest available starting number is 65
            pin_base = wiringpiConfig['pin_base']

            # A0, A1, A2 pins all wired to GND
            i2c_addr = wiringpiConfig['i2c_addr']

            wiringpi.mcp23017Setup(pin_base, i2c_addr)

    if 'fasecycli' in rpiConfig:
        for fc in rpiConfig['fasecycli']:
            if 'rood' in rpiConfig['fasecycli'][fc]:
                if rpiConfig['fasecycli'][fc]['rood']:
                    wiringpi.pinMode(rpiConfig['fasecycli'][fc]['rood'], 1)
                    wiringpi.digitalWrite(rpiConfig['fasecycli'][fc]['rood'], 0)

            if 'groen' in rpiConfig['fasecycli'][fc]:
                if rpiConfig['fasecycli'][fc]['groen']:
                    wiringpi.pinMode(rpiConfig['fasecycli'][fc]['groen'], 1)
                    wiringpi.digitalWrite(rpiConfig['fasecycli'][fc]['groen'], 0)

            if 'geel' in rpiConfig['fasecycli'][fc]:
                if rpiConfig['fasecycli'][fc]['geel']:
                    wiringpi.pinMode(rpiConfig['fasecycli'][fc]['geel'], 1)
                    wiringpi.digitalWrite(rpiConfig['fasecycli'][fc]['geel'], 0)

    if 'detectie' in rpiConfig:
        for d in appConfig['detectie']:
            if rpiConfig['detectie'][d]:
                wiringpi.pinMode(rpiConfig['detectie'][d], 0)
                wiringpi.digitalWrite(rpiConfig['detectie'][d], 0)


# vanaf hier gaan we regelen
try:
    step = 0

    initialise()

    amberState = False

    while True:
        if not appConfig['simulatie']['sumo']:
            now = time.time() * 10
        else:
            now = step

        if not appConfig['simulatie']['sumo']:
            try:
                with open('data/data_from_gui.yaml', 'r') as f:
                    guiData = yaml.load(f)
            except:
                pass

            if guiData:
                for d in guiData['d']:
                    inputs[d] = guiData['d'][d]

                for i in guiData['is']:
                    inputs[i] = guiData['is'][i]

        doven = False
        regelen = False
        geelKnipperen = False
        allesRood = False

        if inputs['is01']:
            doven = True
        elif inputs['is02']:
            geelKnipperen = True
        elif inputs['is03']:
            allesRood = True
        elif inputs['is04']:
            regelen = True

        # regelen
        if regelen:
            reset()
            # setCountData()
            set_conflicts()
            set_wachtgroen()

            if appConfig['simulatie']['sumo']:
                state_old = list(traci.trafficlights.getRedYellowGreenState("K0001"))

                for d in ['d011', 'd021', 'd031', 'd041', 'd051', 'd081', 'd091', 'd101', 'd111']:
                    try:
                        if traci.areal.getLastStepOccupancy(d) > 0:
                            inputs[d] = True
                        else:
                            inputs[d] = False
                    except:
                        pass

            for d in ['d011','d012','d021','d022','d031','d032','d041','d042','d051','d052','d081','d082','d091','d092',
                      'd101','d102','d111','d112']:
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

            set_meeaanvragen()
            set_cyclische_aanvragen()
            set_sequence()
            setDelay(now)

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
                    if not conflictStatus(fc):
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

                    if timers[fc]['VG'] > 0 and now - timers[fc]['VG'] >= timers[fc]['basis']['vastgroen']:
                        outputs[fc]['VG'] = False
                        outputs[fc]['VAG1'] = True

                if outputs[fc]['VAG1']:
                    if timers[fc]['VG'] > 0:
                        timers[fc]['VG'] = 0

                    if timers[fc]['VAG1'] == 0:
                        timers[fc]['VAG1'] = now

                    if not extend[fc]&BIT1 or timers[fc]['VAG1'] > 0 and now - timers[fc]['VAG1'] >= timers[fc]['maximum']['VAG1']:
                        outputs[fc]['VAG1'] = False
                        outputs[fc]['VAG2'] = True

                if outputs[fc]['VAG2']:
                    if timers[fc]['VAG1'] > 0:
                        timers[fc]['VAG1'] = 0

                    if timers[fc]['VAG2'] == 0:
                        timers[fc]['VAG2'] = now

                    if not extend[fc]&BIT2 or timers[fc]['VAG2'] > 0 and now - timers[fc]['VAG2'] >= timers[fc]['maximum']['VAG2']:
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

                    if not extend[fc]&BIT3 or timers[fc]['VAG3'] > 0 and now - timers[fc]['VAG3'] >= timers[fc]['maximum']['VAG3']:
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

                    if not extend[fc]&BIT4 or timers[fc]['VAG4'] > 0 and now - timers[fc]['VAG4'] >= timers[fc]['maximum']['VAG4']:
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
            outputs[fc]['delay'] = timers[fc]['delay']
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

        # stuur de lantaarns aan
        if appConfig['automaat']['raspberry_pi'] or appConfig['simulatie']['sumo']:
            for fc in appConfig['fasecycli']:
                if outputs[fc]['WR'] or outputs[fc]['RVG']:
                    if appConfig['automaat']['raspberry_pi']:
                        # Turn off the yellow LED
                        if fc in rpiConfig['fasecycli']:
                            if rpiConfig['fasecycli'][fc]['geel'] > 64:
                                wiringpi.digitalWrite(rpiConfig['fasecycli'][fc]['geel'], 0)

                        # Turn on the red LED
                        if fc in rpiConfig['fasecycli']:
                            if rpiConfig['fasecycli'][fc]['rood'] > 64:
                                wiringpi.digitalWrite(rpiConfig['fasecycli'][fc]['rood'], 1)

                    if appConfig['simulatie']['sumo']:
                        if sumoConfig['fasecycli'][fc]:
                            for sumo in sumoConfig['fasecycli'][fc]:
                                state_old[sumo] = 'r'

                elif outputs[fc]['VG'] or outputs[fc]['VAG1'] or outputs[fc]['VAG2'] or outputs[fc]['WG'] or outputs[fc]['VAG3'] or outputs[fc]['MVG'] or outputs[fc]['VAG4']:
                    if appConfig['automaat']['raspberry_pi']:
                        # Turn off the red LED
                        if fc in rpiConfig['fasecycli']:
                            if rpiConfig['fasecycli'][fc]['rood'] > 64:
                                wiringpi.digitalWrite(rpiConfig['fasecycli'][fc]['rood'], 0)

                        # Turn on the green LED
                        if fc in rpiConfig['fasecycli']:
                            if rpiConfig['fasecycli'][fc]['groen'] > 64:
                                wiringpi.digitalWrite(rpiConfig['fasecycli'][fc]['groen'], 1)

                    if appConfig['simulatie']['sumo']:
                        if sumoConfig['fasecycli'][fc]:
                            for sumo in sumoConfig['fasecycli'][fc]:
                                state_old[sumo] = 'G'

                elif outputs[fc]['GL']:
                    if appConfig['automaat']['raspberry_pi']:
                        # Turn off the green LED
                        if fc in rpiConfig['fasecycli']:
                            if rpiConfig['fasecycli'][fc]['groen'] > 64:
                                wiringpi.digitalWrite(rpiConfig['fasecycli'][fc]['groen'], 0)

                        # Turn on the yellow LED
                        if fc in rpiConfig['fasecycli']:
                            if rpiConfig['fasecycli'][fc]['geel'] > 64:
                                wiringpi.digitalWrite(rpiConfig['fasecycli'][fc]['geel'], 1)

                    if appConfig['simulatie']['sumo']:
                        if sumoConfig['fasecycli'][fc]:
                            for sumo in sumoConfig['fasecycli'][fc]:
                                state_old[sumo] = 'y'

                else:
                    if appConfig['automaat']['raspberry_pi']:
                        # Turn off the red LED
                        if fc in rpiConfig['fasecycli']:
                            if rpiConfig['fasecycli'][fc]['rood'] > 64:
                                wiringpi.digitalWrite(rpiConfig['fasecycli'][fc]['rood'], 0)

                        # Turn off the green LED
                        if fc in rpiConfig['fasecycli']:
                            if rpiConfig['fasecycli'][fc]['groen'] > 64:
                                wiringpi.digitalWrite(rpiConfig['fasecycli'][fc]['groen'], 0)

                        # Turn off the yellow LED
                        if fc in rpiConfig['fasecycli']:
                            if rpiConfig['fasecycli'][fc]['geel'] > 64:
                                wiringpi.digitalWrite(rpiConfig['fasecycli'][fc]['geel'], 0)

        if appConfig['simulatie']['sumo']:
            state_new = "".join(state_old)
            traci.trafficlights.setRedYellowGreenState("K0001", state_new)

        if not appConfig['automaat']['raspberry_pi'] or appConfig['simulatie']['sumo']:
            try:
                with open('D:\\xampp\\htdocs\\MAP_K0001\\data\\data_to_gui.json', 'w') as jsonFile:
                    jsonFile.write(json.dumps(outputs))
            except:
                pass

        if appConfig['automaat']['raspberry_pi']:
            try:
                with open('/websites/MAP_K0001/www/data/data_to_gui.json', 'w') as jsonFile:
                    jsonFile.write(json.dumps(outputs))
            except:
                pass

        if not appConfig['simulatie']['sumo']:
            # Delay for a 10th of a second (0.1 seconds)
            time.sleep(0.1)

        step += 1
finally:
    reset()

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

    if appConfig['automaat']['raspberry_pi']:
        try:
            with open('/websites/MAP_K0001/www/data/data_to_gui.json', 'w') as jsonFile:
                jsonFile.write(json.dumps(outputs))
        except:
            pass

        if 'fasecycli' in rpiConfig:
            for fc in rpiConfig['fasecycli']:
                if 'rood' in rpiConfig['fasecycli'][fc]:
                    if rpiConfig['fasecycli'][fc]['rood']:
                        wiringpi.digitalWrite(rpiConfig['fasecycli'][fc]['rood'], 0)
                        wiringpi.pinMode(rpiConfig['fasecycli'][fc]['rood'], 0)

                if 'groen' in rpiConfig['fasecycli'][fc]:
                    if rpiConfig['fasecycli'][fc]['groen']:
                        wiringpi.digitalWrite(rpiConfig['fasecycli'][fc]['groen'], 0)
                        wiringpi.pinMode(rpiConfig['fasecycli'][fc]['groen'], 0)

                if 'geel' in rpiConfig['fasecycli'][fc]:
                    if rpiConfig['fasecycli'][fc]['geel']:
                        wiringpi.digitalWrite(rpiConfig['fasecycli'][fc]['geel'], 0)
                        wiringpi.pinMode(rpiConfig['fasecycli'][fc]['geel'], 0)

        if 'detectie' in rpiConfig:
            for d in appConfig['detectie']:
                if rpiConfig['detectie'][d]:
                    wiringpi.digitalWrite(rpiConfig['detectie'][d], 0)
                    wiringpi.pinMode(rpiConfig['detectie'][d], 0)

    if appConfig['automaat']['raspberry_pi']:
        print('TLC stopped...')
