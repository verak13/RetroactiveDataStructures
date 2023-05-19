import unittest
from retroactive_data_structures.partially_retroactive_queue_and_stack.partially_retroactive_queue import PartiallyRetroactiveQueue


class PartiallyRetroactiveQueueTests(unittest.TestCase):

    def test_insert_enqueue(self):
        prq = PartiallyRetroactiveQueue()
        prq.insert_enqueue(value=2, time=10)
        prq.insert_enqueue(value=4, time=20)
        prq.insert_enqueue(value=6, time=30)

        self.assertEqual(str(prq), "Queue = [2, 4, 6]\t\t(First=2, Last=6)")

    def test_insert_dequeue(self):
        prq = PartiallyRetroactiveQueue()
        prq.insert_enqueue(value=2, time=10)
        prq.insert_enqueue(value=4, time=20)
        prq.insert_enqueue(value=6, time=30)
        prq.insert_dequeue(time=28)

        self.assertEqual(str(prq), "Queue = [4, 6]\t\t(First=4, Last=6)")

    def test_delete_operation(self):
        prq = PartiallyRetroactiveQueue()
        prq.insert_enqueue(value=2, time=10)
        prq.insert_enqueue(value=4, time=20)
        prq.insert_enqueue(value=6, time=30)
        prq.insert_dequeue(time=28)
        prq.delete_operation(time=20)

        self.assertEqual(str(prq), "Queue = [6]\t\t(First=6, Last=6)")

    def test_get_first(self):
        prq = PartiallyRetroactiveQueue()
        prq.insert_enqueue(value=2, time=10)
        prq.insert_enqueue(value=4, time=20)
        prq.insert_enqueue(value=6, time=30)

        first_value = prq.get_first()

        self.assertEqual(first_value, 2)

    def test_get_last(self):
        prq = PartiallyRetroactiveQueue()
        prq.insert_enqueue(value=2, time=10)
        prq.insert_enqueue(value=4, time=20)
        prq.insert_enqueue(value=6, time=30)

        last_value = prq.get_last()

        self.assertEqual(last_value, 6)

