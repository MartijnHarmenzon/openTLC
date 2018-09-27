# import default libraries
import yaml


# define dictionaries
outputs = {}
inputs = {}
requests = {}
conflicts = {}
sequence = {}
wachtgroen = {}
timers = {}
countData = {}
detector_status = {}
extend = {}

# define settings
with open('k0001appconf.yaml', 'r') as f:
    appConfig = yaml.load(f)

if appConfig['automaat']['raspberry_pi']:
    with open('k0001rpiconf.yaml', 'r') as f:
        rpiConfig = yaml.load(f)

if appConfig['simulatie']['sumo']:
    with open('k0001sumoconf.yaml', 'r') as f:
        sumoConfig = yaml.load(f)

# define BITS
extend_vag1 = 0x01
extend_vag2 = 0x02
extend_vag3 = 0x04
extend_vag4 = 0x08
