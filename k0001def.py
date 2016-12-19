# import default libraries
import yaml

# define dictionaries
outputs = {}
inputs = {}
demands = {}
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
BIT1 = 0x01
BIT2 = 0x02
BIT3 = 0x04
BIT4 = 0x08
