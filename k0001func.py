# import libraries
import operator
import random
from k0001def import appConfig, outputs, inputs, requests, conflicts, sequence, wachtgroen, timers, countData, \
    detector_status, extend, extend_vag1, extend_vag2, extend_vag3, extend_vag4

if appConfig['automaat']['raspberry_pi']:
    from k0001def import rpiConfig

if appConfig['simulatie']['sumo']:
    from k0001def import sumoConfig


#
def initialise():
    for signal_group in appConfig['fasecycli']:
        outputs[signal_group] = {
            'WR': True,
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
            'sequence': 0
        }
        requests[signal_group] = False
        conflicts[signal_group] = {}
        sequence[signal_group] = 0
        wachtgroen[signal_group] = False
        timers[signal_group] = {
            'R': 0,
            'G': 0,
            'VG': 0,
            'VAG1': 0,
            'VAG2': 0,
            'VAG3': 0,
            'VAG4': 0,
            'GL': 0,
            'delay': 0
        }
        countData[signal_group] = 0
        extend[signal_group] = False
        timers[signal_group]['garantie'] = {
            'rood': appConfig['fasecycli'][signal_group]['tijden']['garantie']['rood'],
            'groen': appConfig['fasecycli'][signal_group]['tijden']['garantie']['groen'],
            'geel': appConfig['fasecycli'][signal_group]['tijden']['garantie']['geel']
        }

        # stel eerst de garantie tijden in als basis tijden
        timers[signal_group]['basis'] = {
            'vastgroen': appConfig['fasecycli'][signal_group]['tijden']['basis']['groen'],
            'geel': appConfig['fasecycli'][signal_group]['tijden']['basis']['geel']
        }

        timers[signal_group]['maximum'] = {
            'VAG1': appConfig['fasecycli'][signal_group]['tijden']['maximum']['VAG1'],
            'VAG2': appConfig['fasecycli'][signal_group]['tijden']['maximum']['VAG2'],
            'VAG3': appConfig['fasecycli'][signal_group]['tijden']['maximum']['VAG3'],
            'VAG4': appConfig['fasecycli'][signal_group]['tijden']['maximum']['VAG4']
        }

        # stel de basis tijden in als deze groter zijn dan de garantie tijden
        if appConfig['fasecycli'][signal_group]['tijden']['garantie']['groen'] > \
                timers[signal_group]['basis']['vastgroen']:
            timers[signal_group]['basis']['vastgroen'] = \
                appConfig['fasecycli'][signal_group]['tijden']['garantie']['groen']
        if appConfig['fasecycli'][signal_group]['tijden']['garantie']['geel'] > \
                timers[signal_group]['basis']['geel']:
            timers[signal_group]['basis']['geel'] = appConfig['fasecycli'][signal_group]['tijden']['garantie']['geel']
            
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
def set_demand_timers(detector, status, now):
    # occupancy time
    try:
        if status:
            if timers[detector]['bezettijd'] == 0:
                timers[detector]['bezettijd'] = now
        else:
            if timers[detector]['bezettijd']:
                timers[detector]['bezettijd'] = 0
    except:
        pass

    # gap time
    try:
        if status:
            if timers[detector]['hiaattijd']:
                timers[detector]['hiaattijd'] = 0
        else:
            if timers[detector]['hiaattijd'] == 0:
                timers[detector]['hiaattijd'] = now
    except:
        pass


#
def request_green(signal_group, detector, status, now):
    try:
        request_type = appConfig['detectie'][detector]['parameters']['aanvraag']
        criteria = False

        if not appConfig['detectie'][detector]['type'] == 'drukknop':
            if status and now - timers[detector]['bezettijd'] >= appConfig['detectie'][detector]['tijden']['bezettijd']:
                criteria = True
            else:
                criteria = False
        else:
            if status:
                criteria = True

        if criteria:
            if request_type == 1:
                if outputs[signal_group]['WR'] and timers[signal_group]['R'] > 0 and \
                        now - timers[signal_group]['R'] >= timers[signal_group]['garantie']['rood']:
                    requests[signal_group] = True
                    # print(fc, d, demands[fc], detector_status[d], 1)
            elif request_type == 2:
                if outputs[signal_group]['WR']:
                    requests[signal_group] = True
                    # print(fc, d, demands[fc], detector_status[d], 2)
            elif request_type == 3:
                if not outputs[signal_group]['VG']:
                    requests[signal_group] = True
                    # print(fc, d, demands[fc], detector_status[d], 3)
    except:
        pass


#
def extend_green(signal_group, detector, status, now):
    try:
        gap_time = appConfig['detectie'][detector]['tijden']['hiaattijd']
        extend_type = appConfig['detectie'][detector]['parameters']['verleng']
        gap_time_timer = timers[detector]['hiaattijd']

        if status and gap_time_timer == 0 or (now - gap_time_timer) < gap_time:
            if extend_type & extend_vag1:
                extend[signal_group] |= extend_vag1
            if extend_type & extend_vag2:
                extend[signal_group] |= extend_vag2
            if extend_type & extend_vag3:
                extend[signal_group] |= extend_vag3
            if extend_type & extend_vag4:
                extend[signal_group] |= extend_vag4
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
    for signal_group in appConfig['fasecycli']:
        requests[signal_group] = False
        # conflicts[signal_group] = {}
        # sequence[signal_group] = 0
        wachtgroen[signal_group] = False
        # timers[signal_group] = {
        #     'R': 0,
        #     'G': 0,
        #     'VG': 0,
        #     'VAG1': 0,
        #     'VAG2': 0,
        #     'WG': 0,
        #     'VAG3': 0,
        #     'MG': 0,
        #     'VAG4': 0,
        #     'GL': 0,
        #     'delay': 0
        # }
        # countData[signal_group] = 0
        extend[signal_group] = 0

    for signal_group_1 in appConfig['conflicten']:
        for signal_group_2 in appConfig['conflicten'][signal_group_1]:
            # print(signal_group_1, signal_group_2, conflicts[signal_group_1])
            conflicts[signal_group_1][signal_group_2] = False

    # for d in appConfig['detectie']:
        # inputs[d] = False

    # for i in appConfig['ingangssignalen']:
        # inputs[i] = False


#
def set_cyclische_aanvragen():
    for signal_group in appConfig['fasecycli']:
        if appConfig['fasecycli'][signal_group]['schakelaars']['cyclisch_aanvragen']:
            requests[signal_group] = True


#
def conflict_manager():
    for signal_group_1 in appConfig['conflicten']:
        for signal_group_2 in appConfig['conflicten'][signal_group_1]:
            if outputs[signal_group_1]['WR'] or outputs[signal_group_1]['RVG']:
                if not outputs[signal_group_2]['WR']:
                    conflicts[signal_group_1][signal_group_2] = True


#
def conflict_status(signal_group_1):
    state = False
    for signal_group_2 in appConfig['conflicten'][signal_group_1]:
        if outputs[signal_group_1]['WR'] or outputs[signal_group_1]['RVG']:
            if not (outputs[signal_group_2]['WR'] or outputs[signal_group_2]['RVG']):
                state = True
                break
        else:
            if outputs[signal_group_2]['RVG']:
                state = True
                break
    return state


#
def conflict_demand(signal_group_1):
    state = False
    for signal_group_2 in appConfig['conflicten'][signal_group_1]:
        if outputs[signal_group_2]['RVG']:
            state = True
            break
    return state


#
def conflict_demand_list(signal_group_1):
    list = []

    for signal_group_2 in appConfig['conflicten'][signal_group_1]:
        if outputs[signal_group_2]['RVG']:
            list.append(signal_group_2)
    return list


#
def conflict_green(signal_groups):
    state = False
    for signal_group_1 in signal_groups:
        for signal_group_2 in appConfig['conflicten'][signal_group_1]:
            if not (outputs[signal_group_2]['GL'] or outputs[signal_group_2]['WR'] or
                    outputs[signal_group_2]['RVG'] or outputs[signal_group_2]['MVG']):
                state = True
                break
    return state


#
def non_conflicts_mvg(signal_group_1):
    state = False

    non_conflicts_list = []
    for signal_group in appConfig['fasecycli']:
        non_conflicts_list.append(signal_group)

    non_conflicts_list.remove(signal_group_1)

    for signal_group in conflicts[signal_group_1]:
        try:
            non_conflicts_list.remove(signal_group)
        except:
            pass

    for signal_group_2 in non_conflicts_list:
        if outputs[signal_group_2]['MVG']:
            state = True

    return state


#
def non_conflicts(signal_groups):
    non_conflicts_list = []

    for signal_group in appConfig['fasecycli']:
        non_conflicts_list.append(signal_group)

    non_conflicts_list.remove(signal_groups)

    for signal_group in conflicts[signal_groups]:
        non_conflicts_list.remove(signal_group)

    return non_conflicts_list


#
def non_green(signal_group_1):
    state = False
    non_green_list = []

    for signal_group in appConfig['fasecycli']:
        non_green_list.append(signal_group)

    non_green_list.remove(signal_group_1)

    for signal_group_2 in non_green_list:
        if not (outputs[signal_group_2]['WR'] or outputs[signal_group_2]['RVG']):
            state = True
            break

    return state


#
def meeverlengen(signal_group):
    state = True

    if outputs[signal_group]['MVG']:
        if conflict_demand(signal_group) and not conflict_green(conflict_demand_list(signal_group)):
            state = False
        if not appConfig['fasecycli'][signal_group]['schakelaars']['meeverlengen']:
            state = False

    if non_conflicts_mvg(signal_group):
        state = False

    if not non_green(signal_group):
        state = False

    return state


#
def set_meeaanvragen():
    for signal_group_1 in appConfig['fasecycli']:
        if 'meeaanvragen' in appConfig['fasecycli'][signal_group_1]['schakelaars']:
            for signal_group_2 in appConfig['fasecycli'][signal_group_1]['schakelaars']['meeaanvragen']:
                if appConfig['fasecycli'][signal_group_1]['schakelaars']['meeaanvragen'][signal_group_2] and \
                        outputs[signal_group_2]['RVG']:
                    requests[signal_group_1] = True


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

    for signal_group_1 in appConfig['fasecycli']:
        if sequence[signal_group_1] == 0:
            if requests[signal_group_1] and outputs[signal_group_1]['WR']:
                sequence[signal_group_1] = value_max_sequence + 1

                list1 = []
                for signal_group_2 in appConfig['fasecycli']:
                    if requests[signal_group_2] and sequence[signal_group_2] == 0:
                        list1.append(signal_group_2)

                for signal_group_3 in conflicts[signal_group_1]:
                    try:
                        list1.remove(signal_group_3)
                    except:
                        pass

                list2 = list1
                for signal_group_4 in list1:
                    for signal_group_5 in conflicts[signal_group_4]:
                        if requests[signal_group_5] and sequence[signal_group_5] == 0:
                            try:
                                list2.remove(signal_group_5)
                            except:
                                pass

                for signal_group_6 in list2:
                    sequence[signal_group_6] = value_max_sequence + 1

                value_max_sequence += 1

    for signal_group_1 in appConfig['fasecycli']:
        criteria = False

        if timers[signal_group_1]['VG'] > 0 and now - timers[signal_group_1]['VG'] < timers[signal_group_1]['garantie']['groen']:
            list1 = non_conflicts(signal_group_1)

            for signal_group_2 in list1:
                list2 = []
                for signal_group_3 in conflicts[signal_group_2]:
                    list2.append(signal_group_3)
                    if now - timers[signal_group_3]['delay'] > 900:
                        criteria = True

            for signal_group_4 in list1:
                if sequence[signal_group_4] >= 1 and appConfig['fasecycli'][signal_group_4]['modaliteit'] == 'motorvoertuig' and not criteria:
                    # and not conflictGreen(list2)
                    sequence[signal_group_4] = 1


#
def delay_manager(now):
    for signal_group in appConfig['fasecycli']:
        if outputs[signal_group]['WR'] or outputs[signal_group]['RVG']:
            if requests[signal_group] and timers[signal_group]['delay'] == 0:
                timers[signal_group]['delay'] = now
        else:
            timers[signal_group]['delay'] = 0


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
