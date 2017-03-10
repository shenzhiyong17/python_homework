class Node():
    key = None
    value = None
    left = None
    right = None
    parent = None

    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value

    def __cmp__(self, other):
        return cmp(self.key, other.key)

    def __str__(self):
        return '%s' % self.key

    def set_left(self, node):
        self.left = node
        if isinstance(node,Node):
            node.parent = self

    def set_right(self, node):
        self.right = node
        if isinstance(node, Node):
            self.right.parent = self