#!/usr/bin/env python
# date: 2016-1-14


class Node:
    key = None
    next = None

    def __init__(self, key=None):
        self.key = key


class LinkList:
    def __init__(self):
        self.head = Node()

    def is_empty(self):
        return self.head.next is None and self.head.key is None

    @staticmethod
    def is_tail(node):
        return node.next is None

    def add(self, key):
        node = self.head
        while not self.is_tail(node):
            node = node.next
        node.next = Node(key)

    def insert(self, key, pos=0):
        node = Node(key)
        if pos == 0:
            if not self.is_empty():
                node.next = self.head
            self.head = node
        else:
            try:
                tmp = self.head
                for i in range(0, pos - 1):
                    tmp = tmp.next
                node.next = tmp.next
                tmp.next = node
            except:
                raise

    def pop(self, pos=0):
        if pos == 0:
            tmp = self.head.key
            self.head = self.head.next
            return tmp
        next_node = self.head
        try:
            for i in range(0, pos - 1):
                next_node = next_node.next
            tmp = next_node.next.key
            next_node.next = next_node.next.next
            return tmp
        except:
            raise

    def print_link(self):
        tmp = self.head
        while not self.is_tail(tmp):
            print tmp.key + ' -> ',
            tmp = tmp.next
        print tmp.key

    def to_array(self):
        array = []
        tmp = self.head
        while not self.is_tail(tmp):
            array.append(tmp.key)
            tmp = tmp.next
        array.append(tmp.key)
        return array

    def revert(self):
        middle = None
        while self.head:
            tail = middle
            middle = self.head
            self.head = self.head.next
            middle.next = tail
        self.head = middle

    def test(self):
        array = ['a', 'b', 'c', 'd', 'e']
        for i in array:
            self.insert(i)
        self.print_link()
        self.revert()
        self.print_link()
        print self.pop(3)
        self.print_link()
        print self.to_array()


if __name__ == "__main__":
    link = LinkList()
    link.test()

