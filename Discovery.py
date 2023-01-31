import pm4py


def dist_event(el, path):
    '''
    Distribution of all of the events over days of the week and hours.
    :param el: event log
    :param path: path to save figures
    :return: - Saves all graphs in a corresponding path
    '''
    # hours, days_month, months, years
    pm4py.save_vis_events_distribution_graph(el, file_path=f"{path}_days.png", distr_type="days_week")
    pm4py.save_vis_events_distribution_graph(el, file_path=f"{path}_hours.png", distr_type="hours")
    pm4py.save_vis_events_distribution_graph(el, file_path=f"{path}_months.png", distr_type="months")


def discovery_inductive(el, path):
    '''
    generate and save BPMN model, petri net and direct follows graph following the inductive miner
    :param el: event log
    :param path: path to save figures
    :return: petri net marking
    '''
    bpmn_model = pm4py.discover_bpmn_inductive(el)
    pm4py.save_vis_bpmn(bpmn_model, f"{path}_bpmn_inductive.png")

    net, initial_marking, final_marking = pm4py.discover_petri_net_inductive(el)
    pm4py.save_vis_petri_net(net, initial_marking, final_marking, f"{path}_petri_inductive.png")

    dfg, st_acc, end_acc, = pm4py.discover_dfg(el)
    pm4py.save_vis_dfg(dfg, st_acc, end_acc, f"{path}_dgf_inductive.png")

    return net, initial_marking, final_marking


def discovery_alpha(el, path):
    '''
    generate and save petri net and direct follows graph following the alpha miner
    :param el: event log
    :param path: path to save figures
    :return: petri net marking
    '''
    net, initial_marking, final_marking = pm4py.discover_petri_net_alpha(el)
    pm4py.save_vis_petri_net(net, initial_marking, final_marking, f"{path}_petri_alpha.png")

    dfg, st_acc, end_acc, = pm4py.discover_dfg(el)
    pm4py.save_vis_dfg(dfg, st_acc, end_acc, f"{path}_dgf_alpha.png")

    return net, initial_marking, final_marking


def social_net(el, path):
    '''
    Create and view hand over and working together social net works and saves them in a given path
    :param el: event log to analyse social net
    :param path: location to save social net
    :return: - Saves graph in a corresponding path
    '''
    hw_values = pm4py.discover_handover_of_work_network(el)
    pm4py.save_vis_sna(hw_values, f"{path}_ho.html")

    wt_values = pm4py.discover_working_together_network(el)
    pm4py.save_vis_sna(wt_values, f"{path}_wt.html")

def activity_time(el):
    # amount of activity y
    # time (months)
    # color - acitivites
    print("x")