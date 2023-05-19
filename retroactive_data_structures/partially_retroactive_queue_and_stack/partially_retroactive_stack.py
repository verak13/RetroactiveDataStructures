from retroactive_data_structures.partially_retroactive_queue_and_stack.base import BasePartiallyRetroactive, BaseNode, \
    BaseOperation


class Node(BaseNode):
    def __init__(self, prev, next, value=None):
        super().__init__(prev, next, value)
        self.is_popped = False


class Operation(BaseOperation):
    def __init__(self, time, node, is_push):
        super().__init__(time, node)
        self.is_push = is_push


class PartiallyRetroactiveStack(BasePartiallyRetroactive):
    def __init__(self):
        super().__init__()
        self.top = None

    def is_initialized(self):
        return not self.top is None

    def get_top(self):
        return None if self.top is None else self.top.value

    def _find_operation_after_binary_search(self, time):

        """
        Find the smallest time value of Operation object that is larger than the passed time value using binary search.
        Return the first one that is not popped. Otherwise, None is returned.
        Note that this implementation assumes that self.operations is already sorted in descending order by time.
        """

        if not self.operations or self.operations[0].time <= time:
            return None
        left = 0
        right = len(self.operations) - 1
        while left <= right:
            mid = (left + right) // 2
            if time < self.operations[mid].time:
                if mid == 0 or time >= self.operations[mid + 1].time:
                    while self.operations[mid].node.is_popped:
                        mid -= 1
                    return self.operations[mid]
                else:
                    left = mid + 1
            else:
                right = mid - 1
        return None

    def insert_push(self, value, time=None):

        """
        Inserts a new push operation with the given value and time into the queue.
        Find operation after passed time value and add push operation before it. If there is no operation after passed time value, add push operation at the end.
        """

        if time is None:
            time = self.get_max_time() + 10

        if time in [op.time for op in self.operations]:
            raise ValueError

        if not self.is_initialized():
            node = Node(None, None, value)
            self.top = node
            operation = Operation(time, node, True)
            self.operations.append(operation)
            self.operations.sort(key=lambda x: x.time, reverse=True)
            return operation

        operation_after = self._find_operation_after_binary_search(time)
        if operation_after is None:
            node = Node(self.top, None, value)
            self.top.next = node
            self.top = node
        else:
            node_after = operation_after.node
            node = Node(node_after.prev, node_after, value)
            if node_after.prev is not None:
                node_after.prev.next = node
            node_after.prev = node

        operation = Operation(time, node, True)
        self.operations.append(operation)
        self.operations.sort(key=lambda x: x.time, reverse=True)

    def insert_pop(self, time=None):

        """
        Insert pop operation at specific time. If time value already exists raise ValueError.
        Find operation after passed time value and add pop operation before it. If there is no operation after passed time value, add pop operation at the end.
        """

        if time is None:
            time = self.get_max_time() + 10

        if time in [op.time for op in self.operations]:
            raise ValueError

        if not self.is_initialized():
            return None

        operation_after = self._find_operation_after_binary_search(time)
        if operation_after is None:
            node = self.top
            self.top = node.prev if node is not None else None
        else:
            node_after = operation_after.node
            node_to_pop = node_after.prev
            if node_to_pop is not None:
                if node_to_pop.prev is not None:
                    node_to_pop.prev.next = node_after
                node_after.prev = node_to_pop.prev
            node = node_to_pop
        node.is_popped = True
        operation = Operation(time, node, False)
        self.operations.append(operation)
        self.operations.sort(key=lambda x: x.time, reverse=True)
        return operation

    def delete_operation(self, time):

        """
        Delete operation at specific time. If time value does not exists raise ValueError.
        If operation type is push, remove pushed node.
        if operation type is pop, put back popped node.
        """

        if time not in [op.time for op in self.operations]:
            raise ValueError

        operation = self._find_operation_binary_search(time)
        node, is_push = operation.node, operation.is_push
        if is_push:
            if node.is_popped:
                if node.prev is None:
                    raise ValueError
                node_to_pop = node.prev
                while node_to_pop.is_popped:
                    if node_to_pop.prev is None:
                        raise ValueError
                    node_to_pop = node_to_pop.prev
                node_after = node.next
                while node_after is not None and node_after.is_popped:
                    node_after = node_after.next
                node_to_pop.is_popped = True
                if node_to_pop.prev is not None:
                    node_to_pop.prev.next = node_after
                if node_after is not None:
                    node_after.prev = node_to_pop.prev
            else:
                node.is_popped = True
                if node.prev is not None:
                    node.prev.next = node.next
                if node.next is not None:
                    node.next.prev = node.prev
                else:
                    self.top = node.prev
        else:
            node.is_popped = False
            if node.next is not None:
                next_node = node.next
                while next_node.prev != node.prev:
                    next_node = next_node.prev
                next_node.prev = node
                node.next = next_node
            if node.prev is not None:
                prev_node = node.prev
                while prev_node.next != node.next:
                    prev_node = prev_node.next
                prev_node.next = node
                node.prev = prev_node
            if node.next is not None and node.next.is_popped:
                self.top = node
        self.operations.remove(operation)
        return None

    def __iter__(self):
        node = self.top
        while node is not None:
            yield node
            node = node.prev

    def __str__(self):
        stack = ", ".join(str(val) for val in self)
        return f"Stack = [{stack}]\t\t(Top={self.get_top()})"


if __name__ == '__main__':
    print("PARTIALLY RETROACTIVE STACK:")
    prs = PartiallyRetroactiveStack()
    prs.insert_push(value=2, time=10)
    print(prs)
    prs.insert_push(value=4, time=20)
    print(prs)
    prs.insert_push(value=6, time=30)
    print(prs)
    prs.insert_pop(time=28)
    print(prs)
    prs.insert_push(value=8, time=15)
    print(prs)
    prs.insert_pop(time=16)
    print(prs)
    prs.delete_operation(time=16)
    print(prs)
    prs.delete_operation(time=28)
    print(prs)
    prs.delete_operation(time=30)
    print(prs)
    pop_operation = prs.get_top()
    print("Top value: " + str(pop_operation))
    print(prs)