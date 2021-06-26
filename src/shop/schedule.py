from ..define import Crossover, Mutation, Selection
from ..resource.job import Job
from ..resource.machine import Machine


class Schedule:  # 调度资源融合类
    def __init__(self):
        self.job = {}  # 工件
        self.machine = {}  # 机器
        self.best_known = None  # 已知下界值
        self.time_unit = 1  # 加工时间单位
        self.ga_operator = {Crossover.name: Crossover.default, Mutation.name: Mutation.default,
                            Selection.name: Selection.default}
        self.para_tabu = False
        self.para_dislocation = False

    def clear(self):  # 解码前要进行清空, 方便快速地进行下一次解码
        for i in self.job.keys():
            self.job[i].clear()
        for i in self.machine.keys():
            self.machine[i].clear()

    @property
    def n(self):  # 工件数量
        return len(self.job)

    @property
    def m(self):  # 机器数量
        return len(self.machine)

    @property
    def makespan(self):  # 工期
        return max([machine.end for machine in self.machine.values()])

    def any_task_not_done(self):  # 解码：判断是否解码结束（基于机器的编码、混合流水车间、考虑作息时间的流水车间）
        return any([any([task.start is None for task in job.task.values()]) for job in self.job.values()])

    def add_machine(self, name=None, index=None):  # 添加机器
        if index is None:
            index = self.m
        self.machine[index] = Machine(index, name)

    def add_job(self, name=None, index=None):  # 添加工件
        if index is None:
            index = self.n
        self.job[index] = Job(index, name)

    def decode_update_machine_idle(self, i, j, k, r, early_start):  # 解码：更新机器空闲时间
        if self.machine[k].idle[1][r] - self.job[i].task[j].end > 0:  # 添加空闲时间段
            self.machine[k].idle[0].insert(r + 1, self.job[i].task[j].end)
            self.machine[k].idle[1].insert(r + 1, self.machine[k].idle[1][r])
        if self.machine[k].idle[0][r] == early_start:  # 删除空闲时间段
            self.machine[k].idle[0].pop(r)
            self.machine[k].idle[1].pop(r)
        else:
            self.machine[k].idle[1][r] = early_start  # 更新空闲时间段
        if self.machine[k].end < self.job[i].task[j].end:  # 更新机器上的最大完工时间
            self.machine[k].end = self.job[i].task[j].end
