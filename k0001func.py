# import libraries
import operator
import random
from k0001def import appConfig, outputs, inputs, demands, conflicts, sequence, wachtgroen, timers, countData, \
    detector_status, extend, BIT1, BIT2, BIT3, BIT4

if appConfig['automaat']['raspberry_pi']:
    from k0001def import rpiConfig

if appConfig['simulatie']['sumo']:
    from k0001def import sumoConfig


#
def initialise():
    for fc in appConfig['fasecycli']:
        outputs[fc] = {'WR': True, 
                       'RVG': False, 
                       'VG': False, 
                       'VAG1': False, 
                       'VAG2': False, 
                       'WG': False, 
                       'VAG3': False,
                       'MVG': False, 
                       'VAG4': False, 
                       'GL': False, 
                       'demand': False, 
                       'sequence': 0}
        demands[fc] = False
        conflicts[fc] = {}
        sequence[fc] = 0
        wachtgroen[fc] = False
        timers[fc] = {'R': 0,
                      'G': 0,
                      'VG': 0,
                      'VAG1': 0,
                      'VAG2': 0,
                      'VAG3': 0,
                      'VAG4': 0,
                      'GL': 0,
                      'delay': 0}
        countData[fc] = 0
        extend[fc] = False
        timers[fc]['garantie'] = {'rood': appConfig['fasecycli'][fc]['tijden']['garantie']['rood'],
                                  'groen': appConfig['fasecycli'][fc]['tijden']['garantie']['groen'],
                                  'geel': appConfig['fasecycli'][fc]['tijden']['garantie']['geel']}

        # stel eerst de garantie tijden in als basis tijden
        timers[fc]['basis'] = {'vastgroen': appConfig['fasecycli'][fc]['tijden']['basis']['groen'],
                               'geel': appConfig['fasecycli'][fc]['tijden']['basis']['geel']}

        timers[fc]['maximum'] = {'VAG1': appConfig['fasecycli'][fc]['tijden']['maximum']['VAG1'],
                                 'VAG2': appConfig['fasecycli'][fc]['tijden']['maximum']['VAG2'],
                                 'VAG3': appConfig['fasecycli'][fc]['tijden']['maximum']['VAG3'],
                                 'VAG4': appConfig['fasecycli'][fc]['tijden']['maximum']['VAG4']}

        # stel de basis tijden in als deze groter zijn dan de garantie tijden
        if appConfig['fasecycli'][fc]['tijden']['garantie']['groen'] > timers[fc]['basis']['vastgroen']:
            timers[fc]['basis']['vastgroen'] = appConfig['fasecycli'][fc]['tijden']['garantie']['groen']
        if appConfig['fasecycli'][fc]['tijden']['garantie']['geel'] > timers[fc]['basis']['geel']:
            timers[fc]['basis']['geel'] = appConfig['fasecycli'][fc]['tijden']['garantie']['geel']
            
    for fc1 in appConfig['conflicten']:
        for fc2 in appConfig['conflicten'][fc1]:
            conflicts[fc1][fc2] = False    
            
    for d in appConfig['detectie']:
        timers[d] = {'bezettijd': 0,
                     'hiaattijd': 0}
        inputs[d] = False

    for i in appConfig['ingangssignalen']:
        inputs[i] = False


#
def detectietijden(d, detector_status, now):
    # bezettijd
    try:
        if detector_status:
            if timers[d]['bezettijd'] == 0:
                timers[d]['bezettijd'] = now
        else:
            if timers[d]['bezettijd']:
                timers[d]['bezettijd'] = 0
    except:
        pass

    # hiaattijd
    try:
        if detector_status:
            if timers[d]['hiaattijd']:
                timers[d]['hiaattijd'] = 0
        else:
            if timers[d]['hiaattijd'] == 0:
                timers[d]['hiaattijd'] = now
    except:
        pass


#
def request_green(fc, d, detector_status, now):
    try:
        aanvraagfunctie = appConfig['detectie'][d]['parameters']['aanvraag']
        type = appConfig['detectie'][d]['type']
        bool = False

        if not type == 'drukknop':
            bezettijd = appConfig['detectie'][d]['tijden']['bezettijd']
            bezettijdTimer = timers[d]['bezettijd']
            if detector_status and now - bezettijdTimer >= bezettijd:
                bool = True
            else:
                bool = False
        else:
            if detector_status:
                bool = True

        if bool:
            if aanvraagfunctie == 1:
                if outputs[fc]['WR'] and timers[fc]['R'] > 0 and now - timers[fc]['R'] >= timers[fc]['garantie']['rood']:
                    demands[fc] = True
                    # print(fc, d, demands[fc], detector_status[d], 1)
            elif aanvraagfunctie == 2:
                if outputs[fc]['WR']:
                    demands[fc] = True
                    # print(fc, d, demands[fc], detector_status[d], 2)
            elif aanvraagfunctie == 3:
                if not outputs[fc]['VG']:
                    demands[fc] = True
                    # print(fc, d, demands[fc], detector_status[d], 3)
    except:
        pass


#
def extend_green(fc, d, detector_status, now):
    try:
        hiaattijd = appConfig['detectie'][d]['tijden']['hiaattijd']
        verlengfunctie = appConfig['detectie'][d]['parameters']['verleng']
        hiaattijdTimer = timers[d]['hiaattijd']

        if detector_status and hiaattijdTimer == 0 or now - hiaattijdTimer < hiaattijd:
            if verlengfunctie & BIT1:
                extend[fc] |= BIT1
            if verlengfunctie & BIT2:
                extend[fc] |= BIT2
            if verlengfunctie & BIT3:
                extend[fc] |= BIT3
            if verlengfunctie & BIT4:
                extend[fc] |= BIT4
    except:
        pass


#
def set_remain_green():
    for fc in appConfig['fasecycli']:
        try:
            if appConfig['fasecycli'][fc]['schakelaars']['wachtgroen'] and not conflict_status(fc):
                wachtgroen[fc] = True
        except:
            pass


#
def set_defaults():
    for fc in appConfig['fasecycli']:
        demands[fc] = False
        # conflicts[fc] = {}
        # sequence[fc] = 0
        wachtgroen[fc] = False
        # timers[fc] = {'R': 0,
                      # 'G': 0,
                      # 'VG': 0,
                      # 'VAG1': 0,
                      # 'VAG2': 0,
                      # 'WG': 0,
                      # 'VAG3': 0,
                      # 'MG': 0,
                      # 'VAG4': 0,
                      # 'GL': 0,
                      # 'delay': 0}
        # countData[fc] = 0
        extend[fc] = 0

    for fc1 in appConfig['conflicten']:
        for fc2 in appConfig['conflicten'][fc1]:
            # print(fc1, fc2, conflicts[fc1])
            conflicts[fc1][fc2] = False

    # for d in appConfig['detectie']:
        # inputs[d] = False

    # for i in appConfig['ingangssignalen']:
        # inputs[i] = False


#
def set_cyclische_aanvragen():
    for fc in appConfig['fasecycli']:
        if appConfig['fasecycli'][fc]['schakelaars']['cyclisch_aanvragen']:
            demands[fc] = True


#
def conflict_manager():
    for fc1 in appConfig['conflicten']:
        for fc2 in appConfig['conflicten'][fc1]:
            if outputs[fc1]['WR'] or outputs[fc1]['RVG']:
                if not outputs[fc2]['WR']:
                    conflicts[fc1][fc2] = True


#
def conflict_status(fc1):
    state = False
    for fc2 in appConfig['conflicten'][fc1]:
        if outputs[fc1]['WR'] or outputs[fc1]['RVG']:
            if not (outputs[fc2]['WR'] or outputs[fc2]['RVG']):
                state = True
                break
        else:
            if outputs[fc2]['RVG']:
                state = True
                break
    return state


#
def conflict_demand(fc1):
    state = False
    for fc2 in appConfig['conflicten'][fc1]:
        if outputs[fc2]['RVG']:
            state = True
            break
    return state


#
def conflict_demand_list(fc1):
    list = []

    for fc2 in appConfig['conflicten'][fc1]:
        if outputs[fc2]['RVG']:
            list.append(fc2)
    return list


#
def conflict_green(list):
    state = False
    for fc1 in list:
        for fc2 in appConfig['conflicten'][fc1]:
            if not (outputs[fc2]['GL'] or outputs[fc2]['WR'] or outputs[fc2]['RVG'] or outputs[fc2]['MVG']):
                state = True
                break
    return state


#
def non_conflicts_mvg(fc1):
    state = False

    list = []
    for fc in appConfig['fasecycli']:
        list.append(fc)

    list.remove(fc1)

    for fc in conflicts[fc1]:
        try:
            list.remove(fc)
        except:
            pass

    for fc2 in list:
        if outputs[fc2]['MVG']:
            state = True

    return state


#
def non_conflicts(fc1):
    list = []
    for fc in appConfig['fasecycli']:
        list.append(fc)

    list.remove(fc1)

    for fc in conflicts[fc1]:
        list.remove(fc)

    return list


#
def non_green(fc1):
    state = False

    list = []
    for fc in appConfig['fasecycli']:
        list.append(fc)

    list.remove(fc1)

    for fc2 in list:
        if not (outputs[fc2]['WR'] or outputs[fc2]['RVG']):
            state = True
            break

    return state


#
def meeverlengen(fc1):
    state = True

    if outputs[fc1]['MVG']:
        if conflict_demand(fc1) and not conflict_green(conflict_demand_list(fc1)):
            state = False
        if not appConfig['fasecycli'][fc1]['schakelaars']['meeverlengen']:
            state = False

    if non_conflicts_mvg(fc1):
        state = False

    if not non_green(fc1):
        state = False

    return state


#
def set_meeaanvragen():
    for fc1 in appConfig['fasecycli']:
        if 'meeaanvragen' in appConfig['fasecycli'][fc1]['schakelaars']:
            for fc2 in appConfig['fasecycli'][fc1]['schakelaars']['meeaanvragen']:
                if appConfig['fasecycli'][fc1]['schakelaars']['meeaanvragen'][fc2] and outputs[fc2]['RVG']:
                    demands[fc1] = True


#
def sequence_evaluator(now):
    key_max_sequence = max(sequence.keys(), key=(lambda key: sequence[key]))
    value_max_sequence = sequence[key_max_sequence]

    # if not (1 in sequence.values()):
    #    for fc in sequence:
    #        if sequence[fc] > 0:
    #            sequence[fc] -= 1

    sorted_sequence = sorted(sequence.items(), key=operator.itemgetter(1))

    for i in range(len(sorted_sequence) - 1):
        value = sorted_sequence[i + 1][1] - sorted_sequence[i][1]

        if value > 1:
            sequence[sorted_sequence[i + 1][0]] -= 1
            sorted_sequence = sorted(sequence.items(), key=operator.itemgetter(1))

    for fc1 in appConfig['fasecycli']:
        if sequence[fc1] == 0:
            if demands[fc1] and outputs[fc1]['WR']:
                sequence[fc1] = value_max_sequence + 1

                list = []
                for fc2 in appConfig['fasecycli']:
                    if demands[fc2] and sequence[fc2] == 0:
                        list.append(fc2)

                for fc3 in conflicts[fc1]:
                    try:
                        list.remove(fc3)
                    except:
                        pass

                list2 = list
                for fc4 in list:
                    for fc5 in conflicts[fc4]:
                        if demands[fc5] and sequence[fc5] == 0:
                            try:
                                list2.remove(fc5)
                            except:
                                pass

                for fc6 in list2:
                    sequence[fc6] = value_max_sequence + 1

                value_max_sequence += 1

    for fc1 in appConfig['fasecycli']:
        bool = False

        if timers[fc1]['VG'] > 0 and now - timers[fc1]['VG'] < timers[fc1]['garantie']['groen']:
            list = non_conflicts(fc1)

            for fc2 in list:
                list2 = []
                for fc3 in conflicts[fc2]:
                    list2.append(fc3)
                    if now - timers[fc3]['delay'] > 900:
                        bool = True

            for fc4 in list:
                if sequence[fc4] >= 1 and appConfig['fasecycli'][fc4]['modaliteit'] == 'motorvoertuig' and not bool: # and not conflictGreen(list2)
                    sequence[fc4] = 1


#
def delay_manager(now):
    for fc in appConfig['fasecycli']:
        if outputs[fc]['WR'] or outputs[fc]['RVG']:
            if demands[fc] and timers[fc]['delay'] == 0:
                timers[fc]['delay'] = now
        else:
            timers[fc]['delay'] = 0


#
def set_count_data():
    countData['fc01'] = random.randrange(0, 101, 2)
    countData['fc02'] = random.randrange(750, 1001, 2)
    countData['fc03'] = random.randrange(0, 101, 2)
    countData['fc04'] = random.randrange(0, 101, 2)
    countData['fc05'] = random.randrange(0, 101, 2)
    countData['fc08'] = random.randrange(750, 1001, 2)
    countData['fc09'] = random.randrange(200, 301, 2)
    countData['fc10'] = random.randrange(400, 501, 2)
    countData['fc11'] = random.randrange(0, 101, 2)
