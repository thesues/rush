import collections
import pdb
# vim: tabstop=4 shiftwidth=4 softtabstop=4 et
LEAF, INTER = ("LEAF", "INTER")
class Node:
    def __init__(self, flavor, identity, weight):
        self.flavor = flavor
        self.identity = identity
        self.weight = weight

#self.root[0] =>           [node0]
#self.root[1] =>        [node1, node2]
#self.root[2] =>  [node3, node4, node5, node6]

class RushTree:
    def __init__(self):
        self.root = collections.deque()
        self.root.append([Node(LEAF, 1, 1)])
        self.depth = 1
        #point to the last inserted
        self.last = 0

    def insert_node(self):
        #get last line
        if len(self.root[self.depth-1]) < 2 ** (self.depth - 1):
            #use the slot
            #generate intermedia nodes
            pos = self.last + 1
            self.generate_parents_and_increate_weight(pos, self.depth, 1)

            identity = self.calc_identity(pos, self.depth)
            self.root[self.depth-1].append(Node(LEAF, identity, 1))
            self.last += 1
            #let all index node add new weight
        #need new root node
        else:
            left_child_weight = self.root[0][0].weight
            self.root.appendleft([Node(INTER, self.root[0][0].identity << 1 ,left_child_weight)])
            self.depth += 1
            self.insert_node()

    #pos,depth is current node's parameter, its parents would be pos/2, depth-1
    def generate_parents_and_increate_weight(self, pos, depth, weight):
        if depth == 1:
            return
        parent = pos/2
        parent_depth = depth - 1
        if self.is_exist(parent_depth, parent) == True:
            node = self.root[parent_depth-1][parent]
            node.weight += weight
        else:
            #create new parent
            v = self.calc_identity(parent, parent_depth)
            self.root[parent_depth-1].append(Node(INTER, v, weight))

        self.generate_parents_and_increate_weight(parent, parent_depth, weight)


    def calc_identity(self, pos, depth):
        #copy from the left tree and add 1 to left side
        current_value  = self.root[depth -1][pos - (2 ** (depth - 1))/2].identity + (1 << self.depth - 1)
        return current_value

    def is_exist(self, depth, pos):
        try:
            self.root[depth-1][pos]
        except:
            return False
        return True

    def print_me(self):
        i = 0
        print self.last + 1
        while i < self.depth:
            print "depth %d"  % (i + 1)
            for j in self.root[i]:
                print "%s:%d" % (bin(j.identity)[2:] , j.weight)

            i += 1

t = RushTree()
t.insert_node()
t.insert_node()
t.insert_node()
t.insert_node()
t.print_me()
