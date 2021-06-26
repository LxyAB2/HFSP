__doc__ = """
工具包
"""

import datetime
import os

import chardet
import numpy as np
from colorama import init, Fore

dt = datetime.datetime
init(autoreset=True)


class Utils:
    @staticmethod
    def create_schedule(shop, n, m, p, tech, proc, best_known=None, time_unit=1):  # 创建一个车间调度对象
        schedule = shop()
        schedule.best_known = best_known  # 已知最优目标值
        schedule.time_unit = time_unit  # 加工时间单位
        for i in range(m):  # 添加机器, 方法add_machine定义在resource包的schedule模块的Schedule类里面
            schedule.add_machine(name=i)
        for i in range(n):  # 添加工件, 方法add_job也定义在resource包的schedule模块的Schedule类里面
            schedule.add_job(name=i)
            for j in range(p[i]):  # 添加工序, p是一个包含n个元素的列表, 对应n个工件的工序数量
                schedule.job[i].add_task(tech[i][j], proc[i][j], name=j)
        return schedule

    @staticmethod
    def calculate_fitness(obj):  # 适应度函数
        return 1 / (1 + obj)

    @staticmethod
    def update_info(old_obj, new_obj):  # 更新个体的条件
        return True if new_obj < old_obj else False

    @staticmethod
    def similarity(a, b):
        return 1 - np.count_nonzero(a - b) / a.shape[0]

    @staticmethod
    def len_tabu(m, n):  # 禁忌搜索表的长度
        a = m * n
        if a < 250:
            return 250
        elif a < 500:
            return 500
        return a

    @staticmethod
    def fore():
        return Fore

    @staticmethod
    def print(msg, fore=Fore.LIGHTCYAN_EX):
        print(fore + msg)

    @staticmethod
    def make_dir(*args, **kw):
        try:
            os.makedirs(*args, **kw)
        except FileExistsError:
            pass

    @staticmethod
    def clear_dir(dir_name):
        try:
            for i in os.listdir(dir_name):
                os.remove("%s/%s" % (dir_name, i))
        except IsADirectoryError:
            pass

    @staticmethod
    def make_dir_save(save, instance, stage2=None):
        Utils.make_dir("./%s" % save)
        Utils.make_dir("./%s/%s" % (save, instance))
        a = ["./%s/%s" % (save, instance), "./%s/%s/Code" % (save, instance), "./%s/%s/GanttChart" % (save, instance),
             "./%s/%s/GanttChartPngHtml" % (save, instance), "./%s/%s/Record" % (save, instance)]
        [Utils.make_dir(i) for i in a]
        try:
            [Utils.clear_dir(i) for i in a]
        except PermissionError:
            pass
        if stage2 is not None:
            b = ["%s2" % i for i in a]
            [Utils.make_dir(i) for i in b]
            try:
                [Utils.clear_dir(i) for i in b]
            except PermissionError:
                pass

    @staticmethod
    def load_text(file_name):
        try:
            with open(file_name, "rb") as f:
                f_read = f.read()
                f_cha_info = chardet.detect(f_read)
                final_data = f_read.decode(f_cha_info['encoding'])
                return final_data
        except FileNotFoundError:
            return None

    @staticmethod
    def string2data_hfsp(string, dtype=int, time_unit=1, minus_one=True):
        try:
            to_data = list(map(dtype, string.split()))
            job, p, tech, prt = 0, [], [], []
            n, m = int(to_data[0]), int(to_data[1])
            index_no, index_nm, index_m, index_t = 2, 3, 4, 5
            while job < n:
                p.append(int(to_data[index_no]))
                tech.append([])
                prt.append([])
                for i in range(p[job]):
                    tech[job].append([])
                    prt[job].append([])
                    int_index_nm = int(to_data[index_nm])
                    for j in range(int_index_nm):
                        int_index_m = int(to_data[index_m])
                        if minus_one is True:
                            tech[job][i].append(int_index_m - 1)
                        else:
                            tech[job][i].append(int_index_m)
                        prt[job][i].append(time_unit * to_data[index_t])
                        index_m += 2
                        index_t += 2
                    index_nm = index_nm + 2 * int_index_nm + 1
                    index_m = index_nm + 1
                    index_t = index_nm + 2
                job += 1
                index_nm = index_nm + 1
                index_m = index_m + 1
                index_t = index_t + 1
                index_no = index_t - 3
            return n, m, p, tech, prt
        except ValueError:
            return None, None, None, None, None

    @staticmethod
    def save_code_to_txt(file, data):
        if not file.endswith(".txt"):
            file = file + ".txt"
        with open(file, "w", encoding="utf-8") as f:
            for i, j in enumerate(str(data)):
                f.writelines(j)
                if (i + 1) % 100 == 0:
                    f.writelines("\n")
            f.writelines("\n")

    @staticmethod
    def save_obj_to_csv(file, data):
        if not file.endswith(".csv"):
            file = file + ".csv"
        with open(file, "w", encoding="utf-8") as f:
            obj, n_iter, direction = [], [], []
            f.writelines("{},{},{}\n".format("Test", "Objective", "IterationReachBest"))
            for k, v in enumerate(data):
                f.writelines("{},{},{}\n".format(k + 1, v[0], v[1]))
                obj.append(v[0])
                n_iter.append(v[1])
            f.writelines("{},{}\n".format("MinObj", min(obj)))
            f.writelines("{},{}\n".format("MaxObj", max(obj)))
            f.writelines("{},{:.2f}\n".format("MeanObj", sum(obj) / len(obj)))
            f.writelines("{},{}\n".format("MinIter", min(n_iter)))
            f.writelines("{},{}\n".format("MaxIter", max(n_iter)))
            f.writelines("{},{:.2f}\n".format("MeanIter", sum(n_iter) / len(n_iter)))

    @staticmethod
    def save_record_to_csv(file, data):
        if not file.endswith(".csv"):
            file = file + ".csv"
        n_row, n_column = len(data[0]), len(data)
        with open(file, "w", encoding="utf-8") as f:
            for i in range(n_row):
                a = ""
                for j in range(n_column):
                    a += "%s," % data[j][i]
                f.writelines(a[:-1] + "\n")

    @staticmethod
    def create_data_hfsp(instance, n, p, m, low, high, dtype=int):
        tech = []
        proc = []
        for i in range(n):
            tech.append([])
            proc.append([])
            for j in range(p):
                tech[i].append(range(sum(m[:j]), sum(m[:j + 1])))
                a = np.random.uniform(low, high, 1).astype(dtype)
                b = []
                for k in range(m[j]):
                    c = np.random.choice([0.9, 0.95, 1, 1.05, 1.1], 1, replace=False)[0]
                    b.append(dtype(a * c))
                proc[i].append(b)
        Utils.make_dir("./src/data/hfsp")
        if not instance.endswith(".txt"):
            instance = instance + ".txt"
        with open("./src/data/hfsp/%s" % instance, "w", encoding="utf-8") as f:
            f.writelines("%s %s\n" % (n, sum(m)))
            for i in range(n):
                d = "%s " % p
                for j in range(p):
                    d += "%s " % m[j]
                    for u, v in zip(tech[i][j], proc[i][j]):
                        d += "%s %s " % (u + 1, v)
                f.writelines("%s\n" % d)
