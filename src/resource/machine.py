import numpy as np


class Machine:  # 机器类
    def __init__(self, index, name=None):
        """
        初始化机器
        :param index: 机器索引
        :param name: 机器名称
        """
        self.index = index
        self.name = name
        self.end = 0  # 机器上的最大完成时间
        # 机器空闲时间数据类型：字典，0：空闲开始时刻，1：空闲结束时刻
        self.idle = {0: [0, ], 1: [np.inf, ]}

    def clear(self):  # 解码用：重置
        self.end = 0
        self.idle = {0: [0, ], 1: [np.inf, ]}
