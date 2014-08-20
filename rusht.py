# vim: tabstop=4 shiftwidth=4 softtabstop=4 et
import collections
import gv
import pdb
LEAF, INTER = ("LEAF", "INTER")
class Node:
    def __init__(self, flavor, identity, weight):
        self.flavor = flavor
        self.identity = identity
        self.weight = weight

    def string(self):
        return bin(self.identity)[2:] + ":" + str(self.weight)

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
        #for draw
        self.G = gv.digraph("G")
        gv.setv(self.G, 'nodesep', '0.05')
        gv.setv(self.G, 'rankdir', 'TB')
        N = gv.protonode(self.G)
        E = gv.protoedge(self.G)

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
        print "total objects:%d" %  (self.last + 1)
        while i < self.depth:
            print "depth %d" % (i)
            for j in self.root[i]:
                print "%s" % (j)
            i += 1

    def get_leftchild(self, depth, pos):
        if depth + 1 > self.depth:
            return None
        try:
            self.root[depth][2*pos]
        except:
            return None
        return (depth+1, 2*pos)

    def get_rightchild(self,depth,pos):
        if depth + 1 > self.depth:
            return None
        try:
            #depth + 1 is next depth
            #depth + 1 - 1 is for offset
            self.root[depth][2*pos + 1]
        except:
            return None
        return (depth+1, 2*pos + 1)

    def get_node(self,depth,pos):
        return self.root[depth-1][pos]

    def iterate_LHR(self,depth,pos):
        left_child = self.get_leftchild(depth,pos)
        if left_child:
            for i in self.iterate_LHR(*left_child):
                yield i

        yield self.get_node(depth, pos)

        right_child = self.get_rightchild(depth,pos)
        if right_child:
            for i in self.iterate_LHR(*right_child):
                yield i

    def out_graph(self):
        self.generate_graph(1,0)
        gv.layout(self.G, 'dot')
        #gv.render(self.G, 'xlib')
        gv.write(self.G, "tree.dot")

    def generate_graph(self,depth,pos):
        left_child = self.get_leftchild(depth,pos)
        if left_child:
            self.add_edge(self.get_node(depth,pos).string(), self.get_node(*left_child).string())
            self.generate_graph(*left_child)

        right_child = self.get_rightchild(depth,pos)
        if right_child:
            self.add_edge(self.get_node(depth,pos).string(), self.get_node(*right_child).string())
            self.generate_graph(*right_child)

    def add_edge(self,a,b):
        nodea = gv.node(self.G, a)
        nodeb = gv.node(self.G, b)
        e = gv.edge(nodea, nodeb)
        gv.setv(e, 'side', 'left')



t = RushTree()
t.insert_node()
t.insert_node()
t.insert_node()
t.insert_node()
t.out_graph()
