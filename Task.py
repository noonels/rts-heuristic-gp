class Task:
    def __init__(self, period=0, release=0, deadline=0, exec_time=0, blk_st=0, blk_dur=0):
        self.period = period
        self.release = release
        self.deadline = deadline # relative
        self.exec_time = exec_time
        self.blocking_start = blk_st
        self.blocking_duration = blk_dur
        self.priority = None

    def __lt__(self, other):
        return self.priority < other.priority

class Job:
    def __init__(self, task: Task, time):
        self.task = task
        self.exec_time = task.exec_time # remaining execution time
        self.release = time
        self.deadline = self.release + task.deadline if task.deadline != 0 else 0
        self.blocking_start = task.blocking_start + self.release
        self.blocking_duration = task.blocking_duration
        self.priority = None
        self.has_run = False

    def __lt__(self, other):
        if self.priority == other.priority and self.has_run == True and other.has_run == False:
            return True
        else:
            self.priority > other.priority


class Problem:
    def __init__(self, tasks=[], hyper_period=0):
        self.tasks = tasks
        self.hyper_period = hyper_period
