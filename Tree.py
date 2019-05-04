from Operations import * # import operation constants (bastardized Sum-Type)
from random import choice, randint
from copy import deepcopy

class Node:
    def __init__(self, left = None, right = None, val = 0, op = CONST):
        self.left = left
        self.right = right
        self.val = val
        self.op = op

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
            self.left.grow(depth_limit - 1)
            self.right = Node()
            self.right.grow(depth_limit - 1)
        if self.op == CONST:
            self.val = randint(0, 255)

    def choose_node(self, graft=False, node=None):
        '''
        Copyright Kool Kids Klub
        '''
        tree_array = []
        def choose_r(tree_array, node, i):
            if node.left != None:
                tree_array += [2 * (i + 1)]
                tree_array = choose_r(tree_array, node.left, 2 * (i + 1))
            if node.right != None:
                tree_array += [2 * (i + 1) + 1]
                tree_array = choose_r(tree_array, node.right, 2 * (i + 1) + 1)
            return tree_array
        tree_array = choose_r(tree_array, self, 0)
        random_node = choice(tree_array)
        parent_list = [random_node]
        while random_node != 0:  # generate lineage
            parent_list += [random_node // 2]
        parent_list.reverse()
        parent_list.pop() # remove self, last element is parent
        current_node = self
        for node_idx in parent_list:
            # follow tree back to chosen node
            current_node = current_node.left if node_idx % 2 == 0 else current_node.right
        if graft:
            if random_node == 0:
                self = deepcopy(node)
            if random_node % 2 == 0: # graft on randomly selected node
                current_node.left = node
            else:
                current_node.right = node
        return current_node

    def recombine(self, other):
        self.choose_node(True, other.choose_node)

    def evaluate(self, task, current_time):
        if self.op == CONST:
            return self.val
        elif self.op == BLK_ST:
            return task.blocking_time.start_time
        elif self.op == BLK_TOT:
            return task.blocking_time.total_time
        elif self.op == OFFSET:
            return task.offset
        elif self.op == PERIOD:
            return task.period
        elif self.op == EXEC:
            return task.exec
        elif self.op == DEADLINE:
            return task.deadline
        elif self.op == PLUS:
            return self.left.evaluate(task, current_time) + self.right.evaluate(task, current_time)
        elif self.op == MINUS:
            return self.left.evaluate(task, current_time) - self.right.evaluate(task, current_time)
        elif self.op == MOD:
            return self.left.evaluate(task, current_time) % self.right.evaluate(task, current_time)
        elif self.op == TIMES:
            return self.left.evaluate(task, current_time) * self.right.evaluate(task, current_time)
        elif self.op == DIVIDED_BY:
            right=self.right.evaluate(task, current_time)
            return 0 if right == 0 else self.left.evaluate(task, current_time) / right
        elif self.op == MAX:
            return max(self.left.evaluate(task, current_time), self.right.evaluate(task, current_time))
        elif self.op == MIN:
            return min(self.left.evaluate(task, current_time), self.right.evaluate(task, current_time))
        elif self.op == CURRENT_TIME:
            return current_time

class Individual:
    def __init__(self):
        self.fitness = 0
        self.root = Node()
        self.size = 0

    def recombine(self, other):
        self.root.recombine(other)

    def evaluate(self, problem):
        '''
        this is where the  p a i n  happens
        '''
        pass
