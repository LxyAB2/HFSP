__doc__ = """
绘制甘特图
"""

from src import *

# save, instance, exp = "GA_HFSP", "real1", "1"
save, instance, exp = "GA-TS_HFSP", "real1", "4"
file_dir = "./%s/%s/GanttChart" % (save, instance)  # 甘特图数据文件所在目录
save_dir = "./%s/%s/GanttChartPngHtml" % (save, instance)  # 生成的甘特图保存目录
file = "%s.csv" % exp  # 甘特图数据文件
file_save = "%s/%s" % (save_dir, file[:-4])  # 保存的甘特图名称
"""===================================================================================="""
a = GanttChart("%s/%s" % (file_dir, file))  # 调用甘特图生成类
a.gantt_chart_png(filename=file_save, fig_width=9, fig_height=5, random_colors=False, lang=0, dpi=200,
                  height=0.8, scale_more=12, x_step=a.schedule.makespan // 10, text_rotation=0,
                  with_operation=True, with_start_end=False, jobs_label=True, show=False)  # 绘制png格式的甘特图
a.gantt_chart_html(filename=file_save, date="2021 06 26", lang=0, show=False)  # 绘制html格式的甘特图
