__doc__ = """
遗传算法
"""

import copy
import time

import numpy as np

from ..define import Selection
from ..resource.code import Code
from ..utils import Utils

deepcopy = copy.deepcopy


class Ga:
    def __init__(self, pop_size, rc, rm, max_generation, objective, schedule, max_stay_generation=None):
        """
        初始化参数。
        pop_size: 种群规模；rc: 交叉概率；rm: 变异概率；max_generation: 最大迭代次数；
        objective: 求解目标值的函数；schedule: 调度对象；max_stay_generation：最大滞留代数
        """
        self.pop_size = pop_size
        self.rc = rc
        self.rm = rm
        self.max_generation = max_generation
        self.objective = objective
        self.schedule = schedule
        self.max_stay_generation = max_stay_generation
        self.best = [None, None, None, []]  # (info, objective, fitness, tabu)
        self.pop = [[], [], []]  # (info, objective, fitness)
        # (start, end, best_objective, best_fitness, worst_fitness, mean_fitness)
        self.record = [[], [], [], [], [], []]
        # (code, mac, tech)
        self.max_tabu = Utils.len_tabu(self.schedule.m, self.schedule.n)
        self.individual = range(self.pop_size)
        self.tabu_list = [[] for _ in self.individual]

    def clear(self):
        self.best = [None, None, None, [[], [], []]]
        self.pop = [[], [], []]
        self.record = [[], [], [], [], [], []]
        self.tabu_list = [[] for _ in self.individual]

    def get_obj_fit(self, info):
        a = self.objective(info)
        b = Utils.calculate_fitness(a)
        return a, b

    def decode(self, code):
        pass

    def update_best(self):
        self.best[2] = max(self.pop[2])
        index = self.pop[2].index(self.best[2])
        self.best[1] = self.pop[1][index]
        self.best[0] = deepcopy(self.pop[0][index])
        self.best[3] = self.tabu_list[index]

    def append_individual(self, info_new):
        obj_new, fit_new = self.get_obj_fit(info_new)
        self.pop[0].append(info_new)
        self.pop[1].append(obj_new)
        self.pop[2].append(fit_new)
        self.tabu_list.append([])

    def replace_individual(self, i, info_new):
        obj_new, fit_new = self.get_obj_fit(info_new)
        if Utils.update_info(self.pop[1][i], obj_new):
            self.pop[0][i] = info_new
            self.pop[1][i] = obj_new
            self.pop[2][i] = fit_new
            self.tabu_list[i] = []

    def show_generation(self, g):
        self.record[2].append(self.best[1])
        self.record[3].append(self.best[2])
        self.record[4].append(min(self.pop[2]))
        self.record[5].append(np.mean(self.pop[2]))
        Utils.print(
            "Generation {:<4} Runtime {:<8.4f} fBest: {:<.8f}, fWorst: {:<.8f}, fMean: {:<.8f}, gBest: {:<.2f} ".format(
                g, self.record[1][g] - self.record[0][g], self.record[3][g], self.record[4][g], self.record[5][g],
                self.record[2][g]))

    def selection_roulette(self):
        a = np.array(self.pop[2]) / sum(self.pop[2])
        b = np.array([])
        for i in range(a.shape[0]):
            b = np.append(b, sum(a[:i + 1]))
        pop = deepcopy(self.pop)
        tabu_list = deepcopy(self.tabu_list)
        self.pop = [[], [], []]
        self.tabu_list = [[] for _ in self.individual]
        c = np.random.random(self.pop_size)
        for i in range(self.pop_size):
            j = np.argwhere(b > c[i])[0, 0]  # 轮盘赌选择
            self.pop[0].append(pop[0][j])
            self.pop[1].append(pop[1][j])
            self.pop[2].append(pop[2][j])
            self.tabu_list[i] = tabu_list[j]

    def selection_champion2(self):
        pop = deepcopy(self.pop)
        tabu_list = deepcopy(self.tabu_list)
        self.pop = [[], [], []]
        self.tabu_list = [[] for _ in self.individual]
        for i in range(self.pop_size):
            a = np.random.choice(range(self.pop_size), 2, replace=False)
            j = a[0] if pop[2][a[0]] > pop[2][a[1]] else a[1]
            self.pop[0].append(pop[0][j])
            self.pop[1].append(pop[1][j])
            self.pop[2].append(pop[2][j])
            self.tabu_list[i] = tabu_list[j]

    def save_best(self):
        self.pop[0][0] = self.best[0]
        self.pop[1][0] = self.best[1]
        self.pop[2][0] = self.best[2]
        self.tabu_list[0] = self.best[3]

    def do_selection(self):
        func_dict = {
            Selection.default: self.selection_roulette,
            Selection.roulette: self.selection_roulette,
            Selection.champion2: self.selection_champion2,
        }
        func = func_dict[self.schedule.ga_operator[Selection.name]]
        self.update_best()
        func()
        self.save_best()

    def do_init(self, pop=None):
        pass

    def do_crossover(self, i, j, p):
        pass

    def do_mutation(self, i, q):
        pass

    def do_tabu_search(self, i):
        pass

    def do_key_block_move(self, i):
        pass

    def reach_max_stay_generation(self, g):
        if self.max_stay_generation is not None and g > self.max_stay_generation and self.record[2][g - 1] == \
                self.record[2][g - self.max_stay_generation]:
            return True
        return False

    def reach_best_known_solution(self):
        if self.schedule.best_known is not None and self.best[1] <= self.schedule.best_known:
            return True
        return False

    def do_evolution(self, pop=None, exp_no=None):
        exp_no = "" if exp_no is None else exp_no
        Utils.print("{}Evolution {}  start{}".format("=" * 48, exp_no, "=" * 48), fore=Utils.fore().LIGHTYELLOW_EX)
        self.clear()
        self.do_init(pop)
        self.do_selection()
        for g in range(1, self.max_generation + 1):
            if self.reach_best_known_solution():
                break
            if self.reach_max_stay_generation(g):
                break
            self.record[0].append(time.perf_counter())
            p, q = np.random.random(self.pop_size), np.random.random(self.pop_size)
            for i in range(self.pop_size):
                if self.reach_best_known_solution():
                    break
                if self.schedule.para_tabu:
                    self.do_tabu_search(i)
                j = np.random.choice(np.delete(np.arange(self.pop_size), i), 1, replace=False)[0]
                self.do_crossover(i, j, p[i])
                self.do_mutation(i, q[i])
            self.do_selection()
            self.record[1].append(time.perf_counter())
            self.show_generation(g)
        Utils.print("{}Evolution {} finish{}".format("=" * 48, exp_no, "=" * 48), fore=Utils.fore().LIGHTRED_EX)


class GaHfsp(Ga):
    def __init__(self, pop_size, rc, rm, max_generation, objective, schedule, max_stay_generation=None):
        Ga.__init__(self, pop_size, rc, rm, max_generation, objective, schedule, max_stay_generation)

    def decode(self, code):
        return self.schedule.decode(code)

    def do_init(self, pop=None):
        self.record[0].append(time.perf_counter())
        for i in range(self.pop_size):
            if pop is None:
                code = Code.sequence_permutation(self.schedule.n)
            else:
                code = pop[0][i].code
            info = self.decode(code)
            obj, fit = self.get_obj_fit(info)
            self.pop[0].append(info)
            self.pop[1].append(obj)
            self.pop[2].append(fit)
        self.update_best()
        self.record[1].append(time.perf_counter())
        self.show_generation(0)

    def do_crossover(self, i, j, p):
        if p < self.rc:
            code1, code2 = self.pop[0][i].ga_crossover_sequence_permutation(self.pop[0][j])
            self.append_individual(self.decode(code1))
            self.append_individual(self.decode(code2))

    def do_mutation(self, i, q):
        if q < self.rm:
            code1 = self.pop[0][i].ga_mutation_sequence_permutation()
            self.append_individual(self.decode(code1))

    def do_tabu_search(self, i):
        code1 = self.pop[0][i].ts_sequence_permutation_based(self.tabu_list[i], self.max_tabu)
        self.replace_individual(i, self.decode(code1))
        if len(self.tabu_list[i]) >= self.max_tabu:
            self.tabu_list[i] = []
