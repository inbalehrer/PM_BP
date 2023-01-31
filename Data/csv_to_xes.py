import pandas as pd
import pm4py

if __name__ == '__main__':
    df_adm = pd.read_csv("lbp_admission.csv", sep=",")
    df_adm["time:timestamp"] = pd.to_datetime(df_adm['time:timestamp'])
    el_adm = pm4py.format_dataframe(df_adm, case_id="case:hadm_id", activity_key="concept:name", timestamp_key="time:timestamp")
    el_adm = pm4py.convert_to_event_log(el_adm)
    pm4py.write_xes(el_adm, "xes/adm.xes")

    df_poe = pd.read_csv("lbp_poe.csv")
    df_poe["time:timestamp"] = pd.to_datetime(df_poe['time:timestamp'])

    el_poe = pm4py.format_dataframe(df_poe, case_id="case:hadm_id", activity_key="concept:name",
                                    timestamp_key="time:timestamp")
    el_poe = pm4py.convert_to_event_log(el_poe)
    pm4py.write_xes(el_adm, "xes/poe.xes")

    df_transfer = pd.read_csv("lbp_transfer.csv")
    df_transfer["time:timestamp"] = pd.to_datetime(df_transfer['time:timestamp'])

    el_transfer = pm4py.format_dataframe(df_transfer, case_id="case:hadm_id", activity_key="concept:name",
                                    timestamp_key="time:timestamp")
    el_transfer = pm4py.convert_to_event_log(el_transfer)
    pm4py.write_xes(el_adm, "xes/transfer.xes")
