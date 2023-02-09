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
    el = pm4py.format_dataframe(df, case_id="case:hadm_id", activity_key="concept:name",
                                timestamp_key="time:timestamp")
    el = pm4py.convert_to_event_log(el)
    if x:
        print("export in xes")
        pm4py.write_xes(el, "Data/xes/transfer_in.xes")
    return el


if __name__ == '__main__':
    el_adm = csv_to_el("Data/lbp_admission.csv", False)
    # Filters adm
    # Top 3 Variants, edout start event, shorter than 10 days
    el_adm = pm4py.filter_variants_top_k(el_adm, 3)
    el_adm = pm4py.filter_start_activities(el_adm, ["edout"], retain=False)
    el_adm = pm4py.filter_case_performance(el_adm, 0, 864000)

    # Event log Transfer
    el_trans = csv_to_el("Data/el_t_2.csv", False)
    el_trans = pm4py.filter_start_activities(el_trans, ["ED Emergency Department"], retain=True)

    # Event log Transfer original
    el_trans_n = csv_to_el("Data/lbp_transfer.csv", False)
    el_trans_n = pm4py.filter_start_activities(el_trans_n, ["Emergency Department"], retain=True)
    nt, imt, fmt = Discovery.discovery_inductive(el_trans_n, f"Results/transnormal", 0.3)

    #Event log Transfer Filter to 3.78%
    el_trans_ne = pm4py.read_xes("Data/xes/el_t_2 filtered to 3.78%.xes.xes.gz")
    ntne, imtne, fmtne = Discovery.discovery_inductive(el_trans_n, f"Results/transnormal_new", 0.3)

    el_reg = pm4py.filter_trace_attribute_values(el_adm, "concept:name", "edreg", retain=True)
    Discovery.dist_event(el_reg, f"Results/admin_edreg")

    event_logs = {"Admission": el_adm, "Transfer": el_trans}

    el_complex, id_complex = Enhancment.sub_had(el_adm)
    el_m, el_f = Enhancment.getgenders(el_trans)

    for k in event_logs:
        print(f"----------- {k} ----------")
        # start_events = pm4py.get_start_activities(event_logs[k])
        # end_events = pm4py.get_end_activities(event_logs[k])
        # print(f"{k}: Start events:\n {start_events} \n End events:\n {end_events}")
        # Enhancment.modal(event_logs[k], k)
        # Enhancment.ages(event_logs[k])
        # Enhancment.rework(event_logs[k])
        # Enhancment.avg_hospital_time(event_logs[k], f"Results/{k}")

        # Discovery.dist_event(event_logs[k], f"Results/{k}")
        n, im, fm = Discovery.discovery_inductive(event_logs[k], f"Results/{k}", 0.3)

        # Conformance checking
        if k == "Admission":
            print("----------------------------FOORPRINT-----------------------------")
            Conformance.footprint(event_logs[k], f"Results/{k}")

            print("----------------------------Complex-----------------------------")
            print(len(id_complex))
            Conformance.alignment(el_complex, n, im, fm)
            Conformance.token_based(el_complex, n, im, fm)
            Discovery.discovery_inductive(el_complex, "Results/complex", 0.3)
        else:
            print("----------------------------M-----------------------------")
            print(len(el_m))
            Conformance.alignment(el_m, n, im, fm)
            Conformance.token_based(el_m, n, im, fm)
            Discovery.discovery_inductive(el_m, "Results/complex", 0.3)
            print("----------------------------M - 378 -----------------------------")
            Conformance.alignment(el_m, ntne, imtne, fmtne)
            Conformance.token_based(el_m, ntne, imtne, fmtne)

            print("----------------------------F-----------------------------")
            print(len(el_f))
            Conformance.alignment(el_f, n, im, fm)
            Conformance.token_based(el_f, n, im, fm)
            Discovery.discovery_inductive(el_f, "Results/complex", 0.3)
            print("----------------------------F - 378 -----------------------------")
            Conformance.alignment(el_f, ntne, imtne, fmtne)
            Conformance.token_based(el_f, ntne, imtne, fmtne)


    # Conformance checking admission
    # Conformance checking Transfer

    # Conformance checking
