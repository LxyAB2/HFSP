__doc__ = """
生成数据
"""

import cProfile
import os

from src import *

pr = cProfile.Profile()

LOW, HIGH, DTYPE = 10, 100, int


def do():
    n, p, m = 10, 3, [2, 3, 4]
    pr.enable()
    for no in range(1, 3):
        instance = "n%sm%s-%s" % (n, sum(m), no)
        Utils.create_data_hfsp(instance, n, p, m, LOW, HIGH, dtype=DTYPE)
        Utils.print("Create %s " % instance)
    pr.disable()
    pr.dump_stats("./test_utils_data.prof")
    os.system("pyprof2calltree -i ./test_utils_data.prof -o callgrind.test_utils_data.prof")


if __name__ == "__main__":
    do()
