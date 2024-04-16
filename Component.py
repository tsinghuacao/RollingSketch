"""
-*- coding: utf-8 -*-
@File  : Component.py
@author: XXX
@Time  : 2023/12/19 13:13
"""

import xxhash
import random
import math
from Set_parameter import *


class Node(object):

    def __init__(self, val):
        self.val = val
        self.pre = None
        self.next = None
        self.gap = 0
        self.src = 0

class DoubleLinkedList(object):

    def __init__(self):
        self.head = Node(0)
        self.tail = self.head

    def is_empty(self):
        return self.head.next is None

    def get_length(self):
        cur = self.head.next
        count = 0
        while cur is not None:
            count += 1
            cur = cur.next
        return count

    def add_last(self, node):
        if self.is_empty():
            self.head.next = node
            node.pre = self.head
            self.tail = node
        else:
            cur = self.tail
            cur.next = node
            node.pre = cur
            node.next = None
            self.tail = node

    def shift_node(self, node):
        if node == self.tail:
            a = 0
        else:
            cur = self.tail
            node.pre.next = node.next
            node.next.pre = node.pre
            cur.next = node
            node.pre = cur
            self.tail = node
            node.next = None

    def remove_old_node(self):
        if self.is_empty():
            return False
        else:
            cur = self.head.next
            self.head.next = cur.next
            cur.next.pre = self.head
            cur.pre = None
            cur.next = None

    def traversal(self):
        node_list = []
        cur = self.head.next
        while cur is not None:
            node_list.append(cur)
            cur = cur.next
        return node_list

class CountMin:

    def __init__(self, d, w):
        self.d = d
        self.w = w
        self.CM = []

    def generate_countmin(self):
        for i in range(self.d):
            row = []
            for j in range(self.w):
                row.append(0)
            self.CM.append(row)

    def CM_update(self, pos):
        pos = str(pos)
        global bias
        for i in range(self.d):
            res = xxhash.xxh64_intdigest(pos, seed=2024 + bias[i]) % self.w
            self.CM[i][res] += 1

    def CM_decrease(self, pos):
        pos = str(pos)
        global bias
        D_val = []
        for i in range(self.d):
            res = xxhash.xxh64_intdigest(pos, seed=2024 + bias[i]) % self.w
            self.CM[i][res] -= 1
            D_val.append(self.CM[i][res])
        return D_val

    def get_CM_value(self, pos):
        pos = str(pos)
        global bias
        frequency = []
        for i in range(self.d):
            res = xxhash.xxh64_intdigest(pos, seed=2024 + bias[i]) % self.w
            frequency.append(self.CM[i][res])
        return frequency


