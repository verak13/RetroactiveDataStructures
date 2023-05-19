import unittest
from retroactive_data_structures.partially_retroactive_priority_queue.partially_retroactive_priority_queue import PartiallyRetroactivePriorityQueue


class PartiallyRetroactivePriorityQueueTests(unittest.TestCase):

    def test_add_insert(self):
        prpq = PartiallyRetroactivePriorityQueue()
        prpq.add_insert(10, 2, "2")
        prpq.add_insert(20, 6, "6")
        prpq.add_insert(30, 4, "4")
        prpq.add_insert(40, 10, "10")

        self.assertEqual(str(prpq), "PriorityQueue = [2, 4, 6, 10]")

    def test_add_delete_min(self):
        prpq = PartiallyRetroactivePriorityQueue()
        prpq.add_insert(10, 2, "2")
        prpq.add_insert(20, 6, "6")
        prpq.add_insert(30, 4, "4")
        prpq.add_insert(40, 10, "10")
        prpq.add_delete_min(29)

        self.assertEqual(str(prpq), "PriorityQueue = [4, 6, 10]")

    def test_get_min(self):
        prpq = PartiallyRetroactivePriorityQueue()
        prpq.add_insert(10, 2, "2")
        prpq.add_insert(20, 6, "6")
        prpq.add_insert(30, 4, "4")
        prpq.add_insert(40, 10, "10")

        min_value = prpq.get_min()

        self.assertEqual(min_value, (2, '2'))

    def test_remove_insert(self):
        prpq = PartiallyRetroactivePriorityQueue()
        prpq.add_insert(10, 2, "2")
        prpq.add_insert(20, 6, "6")
        prpq.add_insert(30, 4, "4")
        prpq.add_insert(40, 10, "10")
        prpq.remove(20)

        self.assertEqual(str(prpq), "PriorityQueue = [2, 4, 10]")

    def test_remove_delete_min(self):
        prpq = PartiallyRetroactivePriorityQueue()
        prpq.add_insert(10, 2, "2")
        prpq.add_insert(20, 6, "6")
        prpq.add_insert(30, 4, "4")
        prpq.add_insert(40, 10, "10")
        prpq.add_delete_min(29)
        prpq.add_delete_min(28)
        prpq.remove(28)

        self.assertEqual(str(prpq), "PriorityQueue = [4, 6, 10]")

    def test_len(self):
        prpq = PartiallyRetroactivePriorityQueue()
        prpq.add_insert(10, 2, "2")
        prpq.add_insert(20, 6, "6")
        prpq.add_insert(30, 4, "4")
        prpq.add_insert(40, 10, "10")

        length = len(prpq)

        self.assertEqual(length, 4)
