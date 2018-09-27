# import libraries
import wiringpi
import yaml
import json
from k0001def import inputs, outputs, requests, sequence, timers, appConfig, rpiConfig
from k0001func import set_defaults


#
def start_func():
    print('TLC started...')

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


#
def set_gui_inputs():
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


#
def set_state():
    for fc in appConfig['fasecycli']:
        if outputs[fc]['WR'] or outputs[fc]['RVG']:
            # Turn off the yellow LED
            if fc in rpiConfig['fasecycli']:
                if rpiConfig['fasecycli'][fc]['geel'] > 64:
                    wiringpi.digitalWrite(rpiConfig['fasecycli'][fc]['geel'], 0)

            if fc in rpiConfig['fasecycli']:
                # Turn on the red LED
                if rpiConfig['fasecycli'][fc]['rood'] > 64:
                    wiringpi.digitalWrite(rpiConfig['fasecycli'][fc]['rood'], 1)

        #
        elif outputs[fc]['VG'] or outputs[fc]['VAG1'] or outputs[fc]['VAG2'] or outputs[fc]['WG'] or \
                outputs[fc]['VAG3'] or outputs[fc]['MVG'] or outputs[fc]['VAG4']:
            # Turn off the red LED
            if fc in rpiConfig['fasecycli']:
                if rpiConfig['fasecycli'][fc]['rood'] > 64:
                    wiringpi.digitalWrite(rpiConfig['fasecycli'][fc]['rood'], 0)

            # Turn on the green LED
            if fc in rpiConfig['fasecycli']:
                if rpiConfig['fasecycli'][fc]['groen'] > 64:
                    wiringpi.digitalWrite(rpiConfig['fasecycli'][fc]['groen'], 1)

        #
        elif outputs[fc]['GL']:
            # Turn off the green LED
            if fc in rpiConfig['fasecycli']:
                if rpiConfig['fasecycli'][fc]['groen'] > 64:
                    wiringpi.digitalWrite(rpiConfig['fasecycli'][fc]['groen'], 0)

            # Turn on the yellow LED
            if fc in rpiConfig['fasecycli']:
                if rpiConfig['fasecycli'][fc]['geel'] > 64:
                    wiringpi.digitalWrite(rpiConfig['fasecycli'][fc]['geel'], 1)

        #
        else:
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

    #
    try:
        with open('/websites/MAP_K0001/www/data/data_to_gui.json', 'w') as jsonFile:
            jsonFile.write(json.dumps(outputs))
    except:
        pass


#
def finally_func():
    #
    set_defaults()

    #
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
        requests[fc] = False
        sequence[fc] = 0
        timers[fc]['delay'] = 0

    #
    try:
        with open('/websites/MAP_K0001/www/data/data_to_gui.json', 'w') as jsonFile:
            jsonFile.write(json.dumps(outputs))
    except:
        pass

    #
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

    #
    if 'detectie' in rpiConfig:
        for d in appConfig['detectie']:
            if rpiConfig['detectie'][d]:
                wiringpi.digitalWrite(rpiConfig['detectie'][d], 0)
                wiringpi.pinMode(rpiConfig['detectie'][d], 0)
