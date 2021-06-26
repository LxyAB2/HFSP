class Objective:
    @staticmethod
    def makespan(info):  # 工期
        return max([machine.end for machine in info.schedule.machine.values()]) / info.schedule.time_unit

    @staticmethod
    def total_makespan(info):  # 工件的完工时间之和
        return sum([job.end for job in info.schedule.job.values()]) / info.schedule.time_unit

    @staticmethod
    def total_flow_time(info):  # 工件的流程时间之和
        return sum([job.end - job.start for job in info.schedule.job.values()]) / info.schedule.time_unit

    @staticmethod
    def total_wait(info):  # 工件的等待时间之和
        return sum([job.wait for job in info.schedule.job.values()]) / info.schedule.time_unit
