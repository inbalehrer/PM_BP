import pandas as pd
import pm4py

import Conformance
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


if __name__ == '__main__':
    el_adm = csv_to_el("Data/lbp_admission.csv", False)
    el_trans = csv_to_el("Data/el_t_2.csv", False)

    # Filters adm
    # Top 3 Variants, edout start event, shorter than 10 days
    el_adm = pm4py.filter_variants_top_k(el_adm, 3)
    el_adm = pm4py.filter_start_activities(el_adm, ["edout"], retain=False)
    # el_adm = pm4py.filter_trace_attribute_values(el_adm, attribute_key="concept:name", values="edout", retain=False)
    el_adm = pm4py.filter_case_performance(el_adm, 0, 864000)

    el_reg = pm4py.filter_event_attribute_values(el_adm, "concept:name", "edreg", retain=True)
    Discovery.dist_event(el_reg, f"Results/admin_edreg")

    #Filters transfer
    el_trans = pm4py.filter_start_activities(el_trans, ["ED Emergency Department"], retain=True)

    event_logs = {"Admission": el_adm, "Transfer": el_trans}


    for k in event_logs:
        print(f"----------- {k} ----------")
        start_events = pm4py.get_start_activities(event_logs[k])
        end_events = pm4py.get_end_activities(event_logs[k])
        print(f"{k}: Start events:\n {start_events} \n End events:\n {end_events}")
        el_complex, id_complex = Enhancment.sub_had(event_logs[k])

        Enhancment.modal(event_logs[k], k)
        Enhancment.ages(event_logs[k])
        #Enhancment.rework(event_logs[k])
        Enhancment.avg_hospital_time(event_logs[k], f"Results/{k}")

        Discovery.dist_event(event_logs[k], f"Results/{k}")
        n, im, fm = Discovery.discovery_inductive(event_logs[k], f"Results/{k}")

        #Conformance checking
        print(f"--------- CC {k} --------- CC  ")
        if k == "Admission":
            Conformance.footprint(event_logs[k], f"Results/{k}")
        Conformance.token_based(event_logs[k], n, im, fm)
        Conformance.alignment(event_logs[k], n, im, fm)

    # Conformance checking admission
    # Conformance checking Transfer

    # Conformance checking
    el_adm_m = pm4py.filter_event_attribute_values(el_adm, "case:gender", ["M"], retain=True)
    el_adm_f = pm4py.filter_event_attribute_values(el_adm, "case:gender", ["F"], retain=True)