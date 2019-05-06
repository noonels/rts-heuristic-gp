from GP import GP
from Task import Problem, Task

def main():
    gp = GP()
    task_list = [Task(0, 6, 14, 5, 2, 2), Task(0, 2, 17, 7, 2, 4), Task(0, 0, 18, 6, 1, 4)]
    problem1 = Problem(task_list, 20)
    # task_list = [Task()]
    task_list = [Task(2, 0, 2, 0.5), Task(3, 0, 3, 1), Task(7, 0, 7, 0.45)]
    problem2 = Problem(task_list, 42)
    # problem3 = Problem()
    # problem4 = Problem()
    problems = [problem1, problem2]
    gp.run(problems)

if __name__ == '__main__':
    main()
