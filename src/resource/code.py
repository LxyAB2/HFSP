import numpy as np


class Code:  # 编码类
    @staticmethod
    def sequence_permutation(length):
        """
        基于排列的编码
        """
        return np.random.permutation(length)
