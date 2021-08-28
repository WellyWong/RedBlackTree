"""
Reference: Red-Black tree pseudocode from CLRS chapter 13
A red-black tree is a binary search tree with one extra bit of storage per node: its color, which can be either
RED or BLACK. By constraining the node colors on any simple path from the root to a leaf, red-black trees ensure
that no such path is more than twice as long as any other, so that the tree is approximately balanced.
red-black properties:
1. Every node is either red or black.
2. The root is black.
3. Every leaf (NIL) is black.
4. If a node is red, then both its children are black.
5. For each node, all simple paths from the node to descendant leaves contain the same number of black nodes.
"""

class Node:
    def __init__(self, key):
        self.key = key
        self.parent = None
        self.left = None
        self.right = None
        self.color = 1     #1: Red,  0: Black

    def __str__(self):
        col = 'BLACK' if self.color == 0 else 'RED'
        return str("{}({})".format(self.key, col))

"""
As a matter of convenience in dealing with boundary conditions in red-black tree code, we use a single sentinel
to represent NIL (page 238, clrs: A sentinel is a dummy object that allows us to simplify boundary conditions).
For a red-black tree T, the sentinel T.nil is an object with the same attributes as an ordinary node in the tree.
Its color attribute is BLACK.
We use the sentinel so that we can treat a NIL child of a node x as an ordinary node whose parent is x. Although we
instead could add a distinct sentinel node for each NIL in the tree, so that the parent of each NIL is well defined,
that approach would waste space. Instead, we use the one sentinel T.nil to represent all the NILs — all leaves and 
the root’s parent. The values of the attributes p, left, right, and key of the sentinel are immaterial, although we may 
set them during the course of a procedure for our convenience.
"""
import sys

class RedBlackTree:
    def __init__(self):
        self.nil = Node(0)  #see figure 13.1.b: RB tree with all NIL children, root.parent point to sentinel (nil)
        self.nil.color = 0
        self.nil.left = self.nil
        self.nil.right = self.nil
        self.nil.parent = self.nil
        self.root = self.nil

    def get_root(self):
        return self.root

    def minimum(self, node):    #find the node with the minimum key
        while node.left != self.nil:
            node = node.left
        return node

    def maximum(self, node):    #find the node with the maximum key
        while node.right != self.nil:
            node = node.right
        return node

    def successor(self, x):     #find the successor of a given node, x
        if x.right != self.nil:   #if the right subtree is not None, the successor is the leftmost node in the right subtree
            return self.minimum(x.right)
        y = x.parent    #else it is the lowest ancestor of x whose left child is also an ancestor of x
        while y != self.nil and x == y.right:
            x = y
            y = y.parent
        return y

    def predecessor(self, x):
        if x.left != self.nil:
            return self.maximum(x.left)
        y = x.parent
        while y != self.nil and x == y.left:
            x = y
            y = y.parent
        return y

    def left_rotate(self, x):   #left rotate at node x, clrs figure 13.2 (page 313)
        y = x.right         #set y as x's right child
        x.right = y.left    #turn y's left subtree into x's right subtree
        if y.left != self.nil:
            y.left.parent = x

        y.parent = x.parent     #link x's parent to y
        if x.parent == self.nil:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x      #put x on y's left
        x.parent = y

    def right_rotate(self, y):  #right rotate at node y. Inverse operation of left_rotate, the code is symmetric.
        x = y.left         #set x as y's left child
        y.left = x.right   #turn x's right subtree into y's left subtree
        if x.right != self.nil:
            x.right.parent = y

        x.parent = y.parent     ##link y's parent to x
        if y.parent == self.nil:
            self.root = x
        elif y == y.parent.left:
            y.parent.left = x
        else:
            y.parent.right = x
        x.right = y     #put y on x's right
        y.parent = x

    def insert(self, key):  #Ordinary bst insertion, at the end we call insert_fixup to maintain RB properties
        z = Node(key)       #create a new node, z, with the given key argument
        z.parent = self.nil
        z.left = self.nil
        z.right = self.nil
        #z.color is already set to 1 (red) in Node class initialization

        y = self.nil #y will serve as a pointer to previous node (parent of x), x pointer will find position to insert
        x = self.root
        while x != self.nil:
            y = x
            if z.key < x.key:
                x = x.left
            elif z.key > x.key:
                x = x.right
            else:
                print("key {} already exists in the tree".format(key))
                return      # node.key == x.key -->> key already exists in the tree
        z.parent = y
        if y == self.nil:       # an empty tree, make z the root node
            self.root = z
            z.color = 0
            return
        elif z.key < y.key:
            y.left = z
        else:
            y.right = z
        self.insert_fixup(z)


    def insert_fixup(self, z):  #see figure 13.4 CLRS (page 317)
        while z.parent.color == 1:  #we enter this loop iteration only if z.p is red, we know that z.p cannot be
                                    # the root. Hence, z.p.p exists.
            if z.parent == z.parent.parent.left:
                y = z.parent.parent.right    # uncle
                if y.color == 1:           #case 1: z's uncle is red
                    z.parent.color = 0
                    y.color = 0
                    z.parent.parent.color = 1
                    z = z.parent.parent   #The while loop continues with node z’s grandparent z.p.p as the new z
                else:
                    if z == z.parent.right:  #case 2: z's uncle is black and z is a right child
                        z = z.parent         #make z point to z.parent
                        self.left_rotate(z)

                    z.parent.color = 0       #case 3: z's uncle is black and z is a left child
                    z.parent.parent.color = 1
                    self.right_rotate(z.parent.parent) #The while loop does not iterate another time after this, since z.p is now black.
            else:
                y = z.parent.parent.left
                if y.color == 1:
                    y.color = 0
                    z.parent.color = 0
                    z.parent.parent.color = 1
                    z = z.parent.parent
                else:
                    if z == z.parent.left:
                        z = z.parent
                        self.right_rotate(z)

                    z.parent.color = 0
                    z.parent.parent.color = 1
                    self.left_rotate(z.parent.parent)

        self.root.color = 0  #When the loop terminates, it does so because z.parent is black. (If z is the root,
                             #then z.parent is the sentinel TNULL, which is black) Thus, the tree does not violate
                             #property 4 at loop termination. By the loop invariant, the only property that might fail
                             #to hold is property 2. This line of code restores this property,


    # transplant replaces the subtree rooted at node u with the subtree rooted at node v,
    # node u’s parent becomes node v’s parent, and u’s parent ends up having v as its appropriate child.
    def rb_transplant(self, u, v):
        if u.parent == self.nil:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent    #we always assign to v.p even if v points to the sentinel

    def find(self, key):
        if self.root == self.nil:
            return self.nil
        else:
            return self.find_helper(key, self.root)

    def find_helper(self, key, node):
        if node == self.nil or node.key == key:
            return node
        if key < node.key:
            return self.find_helper(key, node.left)
        else:   #key > root.value:
            return self.find_helper(key, node.right)

    def delete_node(self, key):
        z = self.find(key)
        if z == self.nil:
            print("Key is not in the tree")
            return
        self.delete_node_helper(z)

    def delete_node_helper(self, z):    #pseudocode and explanation: clrs chapter 13 (page 324)
        y = z   #maintain node y as the node either removed from the tree or moved within the tree
        y_original_color = y.color
        if z.left == self.nil:
            x = z.right
            self.rb_transplant(z, z.right)
        elif z.right == self.nil:
            x = z.left
            self.rb_transplant(z, z.left)
        else:
            y = self.minimum(z.right)   #when z has 2 children, set y to z's successor
            y_original_color = y.color  #update y's original color
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self.rb_transplant(y, y.right) #Replace y with it's right child, then we can transplant y into z position
                y.right = z.right
                y.right.parent = y

            self.rb_transplant(z, y)      #transplant y (z's succesor) into z position
            y.left = z.left
            y.left.parent = y
            y.color = z.color

        if y_original_color == 0:
            self.fix_delete(x)


    def fix_delete(self, x):
        while x != self.nil and x.color == 0:
            if x == x.parent.left:
                w = x.parent.right      # w : sibling
                if w.color == 1:        # case 1: x's sibling, w, is red
                    w.color = 0
                    x.parent.color = 1
                    self.left_rotate(x.parent)
                    w = x.parent.right      # x now has a new sibling after rotation
                
                if w.left.color == 0 and w.right.color == 0:  #case 2: x's sibling, w, is black and both of w's children are black
                    w.color = 1
                    x = x.parent    # new x
                else:
                    if w.right.color == 0:  #case 3: x's sibling, w, is black, and w's left child is red, w's right child is black
                        w.left.color = 0
                        w.color = 1
                        self.right_rotate(w)
                        w = x.parent.right  # new w

                    w.color = x.parent.color  #case 4: x's sibling, w, is black and w's right child is red
                    x.parent.color = 0
                    w.right.color = 0
                    self.left_rotate(x.parent)
                    x = self.root   #new x = self.root  setting x to be the root causes the while loop to terminate

            else:    # x == x.parent.right
                w = x.parent.left
                if w.color == 1:    # case 1 mirror
                    w.color = 0
                    x.parent.color = 1
                    self.right_rotate(x.parent)
                    w = x.parent.left   # new w

                if w.left.color == 0 and w.right.color == 0:    # case 2 mirror
                    w.color = 1
                    x = x.parent    # new x
                else:
                    if w.left.color == 0:   # case 3 mirror
                        w.right.color = 0
                        w.color = 1
                        self.left_rotate(w)
                        w = x.parent.left   # new w

                    w.color = x.parent.color    # case 4 mirror
                    x.parent.color = 0
                    w.left.color = 0
                    self.right_rotate(x.parent)
                    x = self.root

        x.color = 0


    def print_vertical(self):
        stack = []
        margin_stack = []
        stack.append(self.root)
        margin_stack.append((0, '_'))
        while len(stack) > 0:
            node = stack.pop()
            margin, l_or_r_child = margin_stack.pop()
            for i in range(margin):
                print("     ", end='')
            if margin > 0:
                print(l_or_r_child + "---", end='')
            else:
                print('Root:', end='')

            if node != self.nil:
                if node.left != self.nil or node.right != self.nil:
                    stack.append(node.right)
                    margin_stack.append((margin+1, 'R'))
                    stack.append(node.left)
                    margin_stack.append((margin+1, 'L'))
                print(node)
            else:
                print("[]")

    #We'll need this height method to get max depth of the tree, for printing out a tree diagram horizontally
    def height(self, node):
        if node is self.nil:
            return 0
        else:
            l_height = self.height(node.left)
            r_height = self.height(node.right)

            return max(l_height, r_height) + 1

    def draw_tree(self):
        max_depth = self.height(self.root)
        num_space = pow(2, max_depth) + 4
        print('\n')
        for i in range(max_depth):
            self.print_graph(self.root, num_space, 1, i, 0)
            num_space = num_space // 2
            print('\n')


    def print_graph(self, node, num_space, is_left, expected_level, curr_level):
        if node == self.nil or curr_level > expected_level:
            #for i in range(num_space//2):
                #print('  test', end='')
            return -1
        if expected_level == curr_level:
            for i in range(num_space//2):
                print('   ', end='')
            print(node, end='')
        else:
            self.print_graph(node.left, num_space, 1, expected_level, curr_level+1)
            for i in range(num_space//2):
                print(' ', end='')
            self.print_graph(node.right, num_space, 0, expected_level, curr_level+1)
            return

rbt = RedBlackTree()
rbt.insert(8)
rbt.insert(18)
rbt.insert(5)
rbt.insert(15)
rbt.insert(17)
rbt.insert(25)
rbt.insert(40)
rbt.insert(80)
rbt.print_vertical()
rbt.delete_node(25)
rbt.delete_node(100)
rbt.print_vertical()
rbt.draw_tree()
"""
Output:
Root:17(BLACK)
     L---8(RED)
          L---5(BLACK)
          R---15(BLACK)
     R---25(RED)
          L---18(BLACK)
          R---40(BLACK)
               L---[]
               R---80(RED)
Key is not in the tree
Root:17(BLACK)
     L---8(RED)
          L---5(BLACK)
          R---15(BLACK)
     R---40(RED)
          L---18(BLACK)
          R---80(BLACK)
          
                  17(BLACK)

         8(RED)            40(RED)

   5(BLACK)    15(BLACK)    18(BLACK)    80(BLACK)
"""
