import math
import pandas as pd
import pm4py
import matplotlib.pyplot as plt


def modal(el, title):
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
    keys = list(gender_attribute_values.keys())
    if title == "Transfer":
        keys[2] = "No Input"
    else:
        keys[1] = "No Input"
    plt.bar(keys, gender_attribute_values.values(), color='maroon', width=0.4)
    plt.xlabel("Gender")
    plt.ylabel("Number of patients")
    plt.title("Gender deviation within lower back pain patients")
    plt.savefig(f"Results/{title}_gender.png")
    print("Number of gender: ", str(n_gender), "Values: ", gender_attribute_values)

    age_attribute_values = pm4py.get_trace_attribute_values(el, attribute="age")
    ages = list(age_attribute_values.keys())
    values = list(age_attribute_values.values())
    plt.bar(ages, values, color='maroon', width=0.4)
    plt.xlabel("Age")
    plt.ylabel("Number of patients")
    plt.title("Age deviation within lower back pain patients")
    plt.savefig(f"Results/{title}_ages.png")
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

def avg_hospital_time(el, path):
    # Collect case:admittime - case:dischtime
    times = {}
    for t in el._list:
        times[t.attributes['hadm_id']] = t.attributes['dischtime'] - t.attributes['admittime']
    time_data = pd.to_timedelta(pd.Series(times.values()))
    time_data = time_data.dropna()
    avg_time = time_data.mean()
    print(f"Avg time in the hospital: {avg_time}")

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
    el_complex = []
    id_complex = []
    x = 0
    for id in sub_id:
        if sub_id[id] > 1:
            x += 1
            id_complex.append(id)
    for t in el._list:
        y = sub_id[t._list[0]._dict['subject_id']]
        if sub_id[t._list[0]._dict['subject_id']] > 1:
            el_complex.append(t)
    print(x, "Subjects were admin more than once")
    el_f_complex = pm4py.filter_event_attribute_values(el, "subject_id", id_complex, retain=True)
    return el_f_complex, id_complex

def getgenders(el):
    m = pm4py.filter_trace_attribute_values(el, "gender", ["M"], retain=True)
    f = pm4py.filter_trace_attribute_values(el, "gender", ["F"], retain=True)
    return m, f
