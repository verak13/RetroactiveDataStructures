import unittest
from retroactive_data_structures.partially_retroactive_queue_and_stack.partially_retroactive_stack import PartiallyRetroactiveStack


class PartiallyRetroactiveStackTests(unittest.TestCase):

    def test_insert_push(self):
        prs = PartiallyRetroactiveStack()
        prs.insert_push(value=2, time=10)
        prs.insert_push(value=4, time=20)
        prs.insert_push(value=6, time=30)

        self.assertEqual(str(prs), "Stack = [6, 4, 2]\t\t(Top=6)")

    def test_insert_pop(self):
        prs = PartiallyRetroactiveStack()
        prs.insert_push(value=2, time=10)
        prs.insert_push(value=4, time=20)
        prs.insert_push(value=6, time=30)
        prs.insert_pop(time=28)

        self.assertEqual(str(prs), "Stack = [6, 2]\t\t(Top=6)")

    def test_delete_operation(self):
        prs = PartiallyRetroactiveStack()
        prs.insert_push(value=2, time=10)
        prs.insert_push(value=4, time=20)
        prs.insert_push(value=6, time=30)
        prs.insert_pop(time=28)
        prs.delete_operation(time=20)

        self.assertEqual(str(prs), "Stack = [6]\t\t(Top=6)")

    def test_get_top(self):
        prs = PartiallyRetroactiveStack()
        prs.insert_push(value=2, time=10)
        prs.insert_push(value=4, time=20)
        prs.insert_push(value=6, time=30)

        top_value = prs.get_top()

        self.assertEqual(top_value, 6)