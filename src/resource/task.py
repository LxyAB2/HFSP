class Task:  # 加工任务（工序）类
    def __init__(self, index, machine, duration, name=None):
        self.index = index
        self.machine = machine
        self.duration = duration
        self.name = name
        self.start = None  # 解码用：加工开始时间
        self.end = None  # 解码用：加工完成时间

    def clear(self):  # 解码用：重置
        self.start = None
        self.end = None
