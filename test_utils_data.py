__doc__ = """
生成数据
"""

from src import *

LOW, HIGH, DTYPE = 10, 100, int


def do():
    n, p, m = 10, 3, [2, 3, 4]
    for no in range(1, 3):
        instance = "n%sm%s-%s" % (n, sum(m), no)
        Utils.create_data_hfsp(instance, n, p, m, LOW, HIGH, dtype=DTYPE)
        Utils.print("Create %s " % instance)


if __name__ == "__main__":
    do()
