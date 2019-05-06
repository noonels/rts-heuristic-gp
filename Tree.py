from random import choice, randint, shuffle
from statistics import mean
from copy import deepcopy
from Operations import *  # import operation constants (bastardized Sum-Type)
from Task import Job, Problem


class Node:
    def __init__(self, left=None, right=None, val=0, op=CONST):
        self.left = left
        self.right = right
        self.val = val
        self.op = op

    def size(self):
        return (self.left.size() if self.left != None else 0) + 1 + (self.right.size() if self.right != None else 0)

    def uses_nonstatic(self):
        if self.left == None and self.right == None:
            return self.op in NONSTATIC
        elif self.left == None and self.right != None or self.right == None and self.left != None:
            print('!!!!!!!malformed tree!!!!!!!!!')
        else:
            return True if self.op in NONSTATIC else self.left.uses_nonstatic() or self.right.uses_nonstatic()

    def grow(self, depth_limit):
        '''
        generate tree with max depth depth_limit
        '''
        if depth_limit == 0:
            self.op = choice(LEAVES)
        else:
            self.op = choice(OPSUM)
        if self.op in OPERATORS:
            self.left = Node()
            self.left.grow(depth_limit - 1)
            self.right = Node()
            self.right.grow(depth_limit - 1)
        elif self.op == CONST:
            self.val = randint(0, 255)

    def full(self, depth_limit):
        '''
        generate tree full to passed depth_limt
        '''
        if depth_limit == 0:
            self.op = choice(LEAVES)
        else:
            self.op = choice(OPERATORS)
            self.left = Node()
            self.left.full(depth_limit - 1)
            self.right = Node()
            self.right.full(depth_limit - 1)
        if self.op == CONST:
            self.val = randint(0, 255)

    def choose_node(self, graft=False, node=None):
        '''
        Copyright Kool Kids Klub
        '''

        def choose_r(tree_array, node, i):
            if node.left != None and node.op not in LEAVES:
                next_idx = 2 * i
                tree_array.append(next_idx)
                tree_array = choose_r(tree_array, node.left, next_idx)
            if node.right != None and node.op not in LEAVES:
                next_idx = (2 * i) + 1
                tree_array.append(next_idx)
                tree_array = choose_r(tree_array, node.right, next_idx)
            return tree_array

        tree_array = [1]
        tree_array = choose_r(tree_array, self, 1)
        random_node = 1 if tree_array == [] else choice(tree_array)
        parent_list = []  # Was parent_list = [random_node], but I changed this so the selected node is never moved to
        while random_node != 1:  # generate lineage
            random_node = random_node // 2
            parent_list.append(random_node)  # += [random_node // 2]
        #print(parent_list)
        if parent_list != []: parent_list.pop()  # remove root, last element is parent
        #print(parent_list)
        parent_list.reverse()
        current_node = self
        for node_idx in parent_list:
            # follow tree back to chosen node
            current_node = current_node.left if node_idx % 2 == 0 else current_node.right
        if graft:
            #print('NODE:{}'.format(node))
            spam = False
            if random_node == 1:
                self = deepcopy(node)
            else:
                if current_node.op in LEAVES:
                    print('PANIC!!!!!')
                    print('OP:{}'.format(current_node.op))
                    spam = True
                if random_node % 2 == 0:  # graft on randomly selected node
                    if spam:
                        print('CURRENT:{}'.format(current_node))
                        print('LEFT:{}'.format(current_node.left))
                    current_node.left = deepcopy(node)  # changed to deepcopy
                else:
                    if spam:
                        print('CURRENT:{}'.format(current_node))
                        print('RIGHT:{}'.format(current_node.right))
                    current_node.right = deepcopy(node)  # changed to deepcopy
        return current_node

    def recombine(self, other):
        self.choose_node(True, other.choose_node)

    def evaluate(self, job, current_time):
        if self.op == CONST:
            return self.val
        elif self.op == BLK_ST:
            return job.task.blocking_start
        elif self.op == BLK_TOT:
            return job.task.blocking_duration
        elif self.op == RELEASE:
            return job.task.release
        elif self.op == PERIOD:
            return job.task.period
        elif self.op == EXEC:
            return job.task.exec_time
        elif self.op == DEADLINE:
            return job.task.deadline
        elif self.op == PLUS:
            return self.left.evaluate(job, current_time) + self.right.evaluate(job, current_time)
        elif self.op == MINUS:
            return self.left.evaluate(job, current_time) - self.right.evaluate(job, current_time)
        elif self.op == MOD:
            right = self.right.evaluate(job, current_time)
            left = self.left.evaluate(job, current_time)
            return left if right == 0 else left % right
        elif self.op == TIMES:
            return self.left.evaluate(job, current_time) * self.right.evaluate(job, current_time)
        elif self.op == DIVIDED_BY:
            right = self.right.evaluate(job, current_time)
            return 0 if right == 0 else self.left.evaluate(job, current_time) / right
        elif self.op == MAX:
            return max(self.left.evaluate(job, current_time), self.right.evaluate(job, current_time))
        elif self.op == MIN:
            return min(self.left.evaluate(job, current_time), self.right.evaluate(job, current_time))
        elif self.op == CURRENT_TIME:
            return current_time
        elif self.op == J_DEADLINE:
            return job.deadline
        elif self.op == J_RELEASE:
            return job.release
        else:
            print('HELP')
    
    def string(self):
        if self.op == CONST:
            return repr(self.val)
        elif self.op == BLK_ST:
            return 'BLK_ST'
        elif self.op == BLK_TOT:
            return 'BLK_TOT'
        elif self.op == RELEASE:
            return 'TASK_RELEASE'
        elif self.op == PERIOD:
            return 'TASK_PERIOD'
        elif self.op == EXEC:
            return 'TASK_EXEC'
        elif self.op == DEADLINE:
            return 'TASK_DEADLINE'
        elif self.op == PLUS:
            return '(' + self.left.string() + ' + ' + self.right.string() + ')'
        elif self.op == MINUS:
            return '(' + self.left.string() + ' - ' + self.right.string() + ')'
        elif self.op == MOD:
            return '(' + self.left.string() + ' % ' + self.right.string() + ')'
        elif self.op == TIMES:
            return '(' + self.left.string() + ' * ' + self.right.string() + ')'
        elif self.op == DIVIDED_BY:
            return '(' + self.left.string() + ' / ' + self.right.string() + ')'
        elif self.op == MAX:
            return 'MAX(' + self.left.string() + ', ' + self.right.string() + ')'
        elif self.op == MIN:
            return 'MIN(' + self.left.string() + ', ' + self.right.string() + ')'
        elif self.op == CURRENT_TIME:
            return 'TIME'
        elif self.op == J_DEADLINE:
            return 'JOB_DEADLINE'
        elif self.op == J_RELEASE:
            return 'JOB_DEADLINE'
        else:
            print('HELP')

class Individual:
    def __init__(self, parsimony = 0.5):
        self.fitness = 0
        self.fitnesses = []
        self.stats = []
        self.root = Node()
        self.size = 0
        self.parsimony = parsimony

    def __lt__(self, other):
        self.fitness < other.fitness

    def grow(self, depth):
        self.root.grow(depth)

    def full(self, depth):
        self.root.full(depth)

    def recombine(self, other):
        self.root.recombine(other.root)

    def tree_complexity(self):
        self._size = self.root.size()
        self._use_nonstatic = self.root.uses_nonstatic()
        return 1-1/(self.root.size() * self.parsimony * (2 if self.root.uses_nonstatic() else 1))


    def evaluate(self, problems):
        'this is where the  p a i n  begins'
        fitness_vals = []
        for problem in problems:
            hyper_period = problem.hyper_period
            periodic = False
            sporadic = False
            for task in problem.tasks:
                if task.period != 0:
                    periodic = True
                elif task.deadline != 0:
                    sporadic = True
            total_periodic = 0 if periodic else 1
            total_sporadic = 0 if sporadic else 1
            missed_periodic_deadlines = 0
            missed_sporadic_deadlines = 0
            sum_response_time = 1
            job_queue = []
            just_popped = False
            for time in range(hyper_period+1):
                for task in problem.tasks:
                    if task.release == 0 and time == 0 or (task.period + task.release) == time or (task.period != 0 and (time - task.release) % task.period == 0):
                        job_queue.append(Job(task, time)) # release job
                        if task.period != 0:
                            total_periodic += 1
                        elif task.deadline != 0:
                            total_sporadic += 1
                if just_popped:
                    for job in job_queue:
                        job.priority = self.root.evaluate(job, time)
                    shuffle(job_queue)
                    job_queue.sort()
                if len(job_queue) > 0:
                    if time > job_queue[0].blocking_start and job_queue[0].blocking_duration > 0:
                        job_queue[0].blocking_duration -= 1
                    else:
                        if not just_popped:
                            for job in job_queue:
                                job.priority = self.root.evaluate(job, time)
                            shuffle(job_queue)
                            job_queue.sort()
                        else:
                            just_popped = False
                    job_queue[0].exec_time -= 1
                    job_queue[0].has_run = True
                    if job_queue[0].exec_time <= 0:
                        if job_queue[0].deadline == 0: # aperiodic job
                            sum_response_time += time - job_queue[0].release
                        if len(job_queue) != 1:
                            job_queue[0] = job_queue[1]
                            job_queue[1] = job_queue[-1]
                            job_queue.pop()
                            just_popped = True
                        else:
                            job_queue.pop()
                            just_popped = True
                    for job in job_queue:
                        if job.deadline != 0 and job.deadline < time and job.exec_time > 0:
                            if job.task.period != 0:
                                missed_periodic_deadlines += 1
                            else:
                                missed_sporadic_deadlines += 1
                            job_queue.remove(job)
                fitness_vals.append((1-missed_periodic_deadlines/total_periodic)*2 + (1-missed_sporadic_deadlines/total_sporadic) + (1/sum_response_time))
            self.fitnesses.append( (mean(fitness_vals) - self.tree_complexity()) / 2)
            self.stats.append([1-(missed_periodic_deadlines/total_periodic), 1-(missed_sporadic_deadlines/total_sporadic), 1/sum_response_time if sum_response_time != 1 else None])
        self.fitness = max(self.fitnesses)
