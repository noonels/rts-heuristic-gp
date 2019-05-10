from GP import GP
from Task import Problem, Task

def main():
    gp = GP()
    problems = []
    task_list = [Task(period=0, release=6, deadline=14, exec_time=5, blk_st=2, blk_dur=2),
                 Task(period=0, release=2, deadline=17, exec_time=7, blk_st=2, blk_dur=4),
                 Task(period=0, release=0, deadline=18, exec_time=6, blk_st=1, blk_dur=4)]
    problems.append(Problem(task_list, 20))

    task_list = [Task(period=2, deadline=2, exec_time=1),
                 Task(period=3, deadline=3, exec_time=2),
                 Task(period=7, deadline=7, exec_time=3)]
    problems.append(Problem(task_list, 42))

    task_list = [Task(period=2.5, exec_time=2, deadline=3),
                 Task(period=4,   exec_time=1, deadline=4),
                 Task(period=5,   exec_time=2, deadline=5)]
    problems.append(Problem(task_list, 20))

    task_list = [Task(period=3, exec_time=1, deadline=3),
                 Task(period=4, exec_time=1, deadline=4),
                 Task(period=5, exec_time=1, deadline=5),
                 Task(exec_time=12),
                 Task(exec_time=10)]
    problems.append(Problem(task_list, 60))

    task_list = [Task(period=5, exec_time=6, deadline=5),
                 Task(period=6, exec_time=5, deadline=5),
                 Task(period=9, exec_time=4, deadline=5),
                 Task(exec_time=24),
                 Task(exec_time=7, deadline=12)]
    problems.append(Problem(task_list, 90))
    gp.run(problems)

if __name__ == '__main__':
    main()
