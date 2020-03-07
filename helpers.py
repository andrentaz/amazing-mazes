# -*- encoding: utf-8 -*-
"""
This module contains all the auxiliar data structures and functions required to
implement Dijkstra's algorithm.

:author: Andre Filliettaz
:email: andrentaz@gmail.com
:github: https://github.com/andrentaz
"""
from __future__ import absolute_import, unicode_literals

from collections import deque


class BinaryMinHeap(object):
    """A simple implementation of a BinaryMinHeap"""
    def __init__(self):
        super(BinaryMinHeap, self).__init__()
        self.heap = []
        self.unheaped = True

    def __repr__(self):
        return (
            'BinaryMinHeap(size={}, '
            'min={}, '
            'heap={})'
        ).format(len(self.heap), self.heap[0], self.heap)

    def min_heapify(self, idx):
        """Heapify a portion of the array"""
        # total array size
        length = len(self.heap) - 1

        # indexes
        left = 2 * idx + 1
        right = 2 * idx + 2
        smallest = idx

        if left <= length and self.heap[idx] > self.heap[left]:
            smallest = left

        if right <= length and self.heap[smallest] > self.heap[right]:
            smallest = right

        if smallest != idx:
            self.heap[idx], self.heap[smallest] = self.heap[smallest], self.heap[idx]
            self.min_heapify(smallest)

    def build_min_heap(self):
        """Create a heap from the object's array heap"""
        array = self.heap
        for i in reversed(range(len(array)//2)):
            self.min_heapify(i)

        self.unheaped = False

    def extract_min(self):
        """Get minimum element preserving the heap property"""
        # change the first and last elements
        if self.unheaped:
            self.build_min_heap()

        self.heap[0], self.heap[-1] = self.heap[-1], self.heap[0]
        minimum = self.heap.pop()

        self.unheaped = True

        # return the minimum
        return minimum

    def add_to_heap(self, node):
        """Add node to heap, preserving the heap property"""
        idx = len(self.heap)
        self.heap.append(node)


class Queue(object):
    """Simple FIFO data structure"""
    def __init__(self, queue):
        super(Queue, self).__init__()
        self.queue = deque(queue)

    def add(self, e):
        """Add element to the last position in the FIFO"""
        self.queue.append(e)

    def pop(self):
        """Pop the first element in the FIFO"""
        return self.queue.popleft()

    def __len__(self):
        return len(self.queue)
