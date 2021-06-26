from .task import Task


class Job:  # 工件类
    def __init__(self, index, name=None):
        """
        初始化工件
        """
        self.index = index
        self.name = name
        self.task = {}  # 工序集合
        self.nd = 0  # 解码用：已加工的工序数量

    def clear(self):  # 解码用：重置
        for i in self.task.keys():
            self.task[i].clear()
        self.nd = 0

    @property
    def nop(self):  # 工序数量
        return len(self.task)

    def add_task(self, machine, duration, name=None, index=None):
        """
        添加加工任务（工序）
        """
        if index is None:
            index = self.nop
        self.task[index] = Task(index, machine, duration, name)

    @property
    def start(self):  # 工件的加工开始时间
        return self.task[0].start

    @property
    def end(self):  # 工件的加工完成时间
        return self.task[self.nop - 1].end

    @property
    def wait(self):  # 工件总的等待时间
        a = self.end - self.start
        b = 0
        for task in self.task.values():
            b += task.duration
        return a - b
