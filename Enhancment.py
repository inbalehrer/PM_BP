import math
import pandas as pd
import pm4py


def modal(el):
    event_attribute_values = pm4py.get_event_attribute_values(el, attribute="concept:name")
    n_activities = len(event_attribute_values)
    print("Number of activities: ", str(n_activities), "\n Values: ", event_attribute_values)

    adm_loc_attribute_values = pm4py.get_trace_attribute_values(el, attribute="admission_location")
    n_adm_loc = len(adm_loc_attribute_values)
    print("Number of adm_loc: ", str(n_adm_loc), "\n Values: ", adm_loc_attribute_values)

    dcr_loc_attribute_values = pm4py.get_trace_attribute_values(el, attribute="discharge_location")
    n_dcr_loc = len(dcr_loc_attribute_values)
    print("Number of dcr loc: ", str(n_dcr_loc), "Values: ", dcr_loc_attribute_values)

    race_attribute_values = pm4py.get_trace_attribute_values(el, attribute="race")
    n_race = len(race_attribute_values)
    print("Number of race: ", str(n_race), "Values: ", race_attribute_values)

    insurance_attribute_values = pm4py.get_trace_attribute_values(el, attribute="insurance")
    n_insurance = len(insurance_attribute_values)
    print("Number of insurance: ", str(n_insurance), "Values: ", insurance_attribute_values)

    language_attribute_values = pm4py.get_trace_attribute_values(el, attribute="language")
    n_language = len(language_attribute_values)
    print("Number of lang: ", str(n_language), "Values: ", language_attribute_values)

    gender_attribute_values = pm4py.get_trace_attribute_values(el, attribute="gender")
    n_gender = len(gender_attribute_values)
    print("Number of gender: ", str(n_gender), "Values: ", gender_attribute_values)

    age_attribute_values = pm4py.get_trace_attribute_values(el, attribute="age")
    n_age = len(age_attribute_values)
    print("Number of age: ", str(n_age), "Values: ", age_attribute_values)


def ages(el):
    ages = []
    for trace in el._list:
        # for event in trace._list[0]
        ages.append(trace._attributes['age'])
    ages = [x for x in ages if math.isnan(x) == False]
    print("Youngest: ", min(ages))
    print("Oldest: ", max(ages))
    print("Avg age:", round(sum(ages) / len(ages), 2))


def rework(el):
    '''
    Analyse how many traces include reworked activities
    :param el: event log
    :return: dict of all activities that were reworked and the corresponding cases
    '''
    from pm4py import get_rework_cases_per_activity
    dic = get_rework_cases_per_activity(el)
    print("Rework:")
    for i in dic:
        print(f"{i} : {dic[i]} ({round(dic[i] * 100 / len(el), 2)}%)")
    return dic

def avg_hospital_time(el):
    # Collect case:admittime - case:dischtime
    avg_time = 0
    return avg_time

#def sojo(el):
#    '''
#    Print Sojourn Time for activities in the event log, AVG duration of activity
#    :param el: event log
#    :return: dict of ech activity and the corresponding sojo time
#    '''
#    from pm4py.statistics.sojourn_time.log import get as soj_time_get
#    sojo_time = soj_time_get.apply(el, parameters={soj_time_get.Parameters.TIMESTAMP_KEY: "endtime",
#                                                   soj_time_get.Parameters.START_TIMESTAMP_KEY: "created"})
#    print(f"Sojo time: {sojo_time}")
#    return sojo_time

def batch(el):
    '''
    Collect batches from an event log
    :param el: event log to analyse
    :return: Batches list of a given event log
    '''
    from pm4py.algo.discovery.batches import algorithm
    batches = algorithm.apply(el)
    print("Batches:")
    for act in batches:
        print(f"{act[0][0]} / {act[0][1]} ({str(act[1])}) \n")
    return batches

def sub_had(el):
    sub_id = pm4py.get_event_attribute_values(el, attribute="subject_id", count_once_per_case=True)
    x = 0
    for id in sub_id:
        if sub_id[id] > 1: x += 1
    print(x, "Subjects were admin more than once")


