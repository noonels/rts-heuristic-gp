class Block:
    def __init__(self):
        self.start_time = 0
        self.total_time = 0

class Task:
    def __init__(self):
        self.period = 0
        self.deadline = 0
        self.exec_time = 0
        self.blocking_time = Block()
        self.priority = None