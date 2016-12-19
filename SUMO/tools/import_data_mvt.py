import pandas as pd
import numpy as np
from lxml import etree

df3 = pd.DataFrame()

def get_data(file):
    df = pd.DataFrame()
    df2 = pd.DataFrame()
    dir = 'E:/Dropbox/My MAPtm/SUMO/openTLC/data/output/'

    tree = etree.parse(dir + file)
    root = tree.getroot()

    for element in root.iter("*"):
        if element.tag == 'interval':
            begin = float(element.attrib['begin'])
            end = float(element.attrib['end'])
            id = element.attrib['id']
            meanTravelTime = float(element.attrib['meanTravelTime'])
            meanSpeed = float(element.attrib['meanSpeed'])
            meanHaltsPerVehicle = float(element.attrib['meanHaltsPerVehicle'])
            vehicleSum = int(float(element.attrib['vehicleSum']))
            meanSpeedWithin = float(element.attrib['meanSpeedWithin'])
            meanHaltsPerVehicleWithin = float(element.attrib['meanHaltsPerVehicleWithin'])
            meanDurationWithin = float(element.attrib['meanDurationWithin'])
            vehicleSumWithin = int(float(element.attrib['vehicleSumWithin']))
            meanIntervalSpeedWithin = float(element.attrib['meanIntervalSpeedWithin'])
            meanIntervalHaltsPerVehicleWithin = float(element.attrib['meanIntervalHaltsPerVehicleWithin'])
            meanIntervalDurationWithin = float(element.attrib['meanIntervalDurationWithin'])

            if begin > 0 and end <= 8100:
                data = pd.DataFrame({'begin': [begin],
                                     'end': [end],
                                     'vehicleSum': vehicleSum,
                                     'meanTravelTime': meanTravelTime,
                                     'meanHaltsPerVehicle': meanHaltsPerVehicle/1000})
                df = df.append(data)

    df2 = pd.DataFrame({'id': [id],
                         'begin': [900],
                         'end': [8100],
                         'vehicleSum': df.vehicleSum.sum() / 2,
                         'meanTravelTime': df.meanTravelTime.median(),
                         'meanHaltsPerVehicle': df.meanHaltsPerVehicle.median()})
    return(df2)

files = ['tt_fc01.txt',
         'tt_fc02.txt',
         'tt_fc03.txt',
         'tt_fc04.txt',
         'tt_fc05.txt',
         'tt_fc06.txt',
         'tt_fc07.txt',
         'tt_fc08.txt',
         'tt_fc09.txt',
         'tt_fc10.txt',
         'tt_fc11.txt',
         'tt_fc12.txt']

for file in files:
    df2 = get_data(file)
    df3 = df3.append(df2)

df3['freeFlowTravelTime'] = [11.925,
                             13.880,
                             11.690,
                              4.415,
                             10.265,
                             10.935,
                             35.050,
                             35.395,
                             34.760,
                             12.600,
                             11.980,
                             11.515]

def calcLoS(delay):
    delay = delay['delay']
    # print(delay)
    if (delay < 10.0):
        return 'A'
    elif (delay < 20.0):
        return 'B'
    elif (delay < 35.0):
        return 'C'
    elif (delay < 55.0):
        return 'D'
    elif (delay < 80.0):
        return 'E'
    elif (delay >= 80.0):
        return 'F'
    else:
        return '-'

def calcLoS2(delay):
    delay = delay['vehicleDelay']
    # print(delay)
    if (delay < 10.0):
        return 'A'
    elif (delay < 20.0):
        return 'B'
    elif (delay < 35.0):
        return 'C'
    elif (delay < 55.0):
        return 'D'
    elif (delay < 80.0):
        return 'E'
    elif (delay >= 80.0):
        return 'F'
    else:
        return '-'

def calcLoS3(delay):
    delay = delay['vehicleDelay']
    # print(delay)
    if (delay < 10.0):
        return 'A'
    elif (delay < 20.0):
        return 'B'
    elif (delay < 35.0):
        return 'C'
    elif (delay < 55.0):
        return 'D'
    elif (delay < 80.0):
        return 'E'
    elif (delay >= 80.0):
        return 'F'
    else:
        return '-'

df3['delay'] = df3.meanTravelTime - df3.freeFlowTravelTime
df3['LoS'] = df3.apply(calcLoS, axis=1)
df3['totalDelay'] = (df3.vehicleSum * df3.delay ) / 3600
print(df3[[2,3,4,5,7,8]])

df4 = pd.DataFrame()
df4 = pd.DataFrame({'begin': [900],
                     'end': [8100],
                     'totalDelay': df3.totalDelay.sum(),
                     'vehicleSum': df3.vehicleSum.sum()})
df4['vehicleDelay'] = (df4.totalDelay * 3600) / df4.vehicleSum
df4['LoS'] = df4.apply(calcLoS2, axis=1)
print(df4)

# df5 = pd.DataFrame()
# df5['meanTravelTime'] = [51.3,
#                          45.2,
#                          51.1,
#                          40.6,
#                          58.7,
#                          51.6,
#                          20.2,
#                          18.4,
#                          31.9,
#                          36.9,
#                          51.8,
#                          49.8,]
# frames = [df5, df3.freeFlowTravelTime]
#
# df6 = pd.DataFrame()
# df6 = pd.concat(frames)
#
# print(df6)
