from ..utils import Utils


def GaTemplate(save, instance, ga, n_exp=10):
    Utils.make_dir_save(save, instance)
    obj_list = []
    for exp in range(1, n_exp + 1):
        ga.do_evolution(exp_no=exp)
        ga.best[0].save_code_to_txt("./%s/%s/Code/%s.txt" % (save, instance, exp))
        ga.best[0].save_gantt_chart_to_csv("./%s/%s/GanttChart/%s.csv" % (save, instance, exp))
        Utils.save_record_to_csv("./%s/%s/Record/%s.csv" % (save, instance, exp), ga.record)
        obj_list.append([ga.best[1], ga.record[2].index(ga.best[1])])
    Utils.save_obj_to_csv("./%s/%s.csv" % (save, instance), obj_list)
