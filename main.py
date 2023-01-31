import pandas as pd
import pm4py

import Discovery
import Enhancment


def csv_to_el(path, x):
    df = pd.read_csv(path)
    if x:
        df["eventtype"] = df["eventtype"] + "/"
        df['event_in'] = df['eventtype'] + df["concept:name"]
    df["time:timestamp"] = pd.to_datetime(df['time:timestamp'])
    print(df.columns)
    el = pm4py.format_dataframe(df, case_id="case:hadm_id", activity_key="concept:name",
                                timestamp_key="time:timestamp")
    el = pm4py.convert_to_event_log(el)
    if x:
        print("export in xes")
        pm4py.write_xes(el, "Data/xes/transfer_in.xes")
    return el


def analysis(el, title):
    print(f"--------------------{title}--------------------")
    start_events = pm4py.get_start_activities(el)
    end_events = pm4py.get_end_activities(el)
    print(f"Start events:\n {start_events} \n End events:\n {end_events}")
    # Filters
    # filtered_start = pm4py.filter_start_activities(el, start_acc)
    # filtered_log = pm4py.filter_end_activities(filtered_start, end_acc)
    # filtered = pm4py.filter_event_attribute_values(el, str(attribute), value, retain=retainit)

    Enhancment.modal(el)
    Enhancment.ages(el)
    Enhancment.rework(el)
    Enhancment.sub_had(el)

    Discovery.dist_event(el, f"Results/{title}")
    Discovery.discovery_inductive(el, f"Results/{title}")
    Discovery.discovery_alpha(el, f"Results/{title}")
    # Enhancment.batch(el_adm)
    # Discovery.social_net(el_trans, "Results/adm")


if __name__ == '__main__':
    el_adm = csv_to_el("Data/lbp_admission.csv", False)
    el_trans = csv_to_el("Data/lbp_transfer.csv", False)

    analysis(el_adm, "admission")
    # Filters adm
    # Variants
    el_adm = pm4py.filter_variants_top_k(el_adm, 3)
    el_adm = pm4py.filter_trace_attribute_values(el_adm, attribute_key="concept:name",  values="edout", retain= False)
    el_adm = pm4py.filter_case_performance(el_adm, 0, 864000)

    Enhancment.modal(el_adm)
    Enhancment.ages(el_adm)
    Enhancment.rework(el_adm)
    Enhancment.sub_had(el_adm)

    Discovery.dist_event(el_adm, f"Results/adm_f_")
    Discovery.discovery_inductive(el_adm, f"Results/adm_f_")
    Discovery.discovery_alpha(el_adm, f"Results/adm_f_")

    #Conformance checking