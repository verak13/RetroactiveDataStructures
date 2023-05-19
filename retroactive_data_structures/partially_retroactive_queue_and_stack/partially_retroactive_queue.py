from retroactive_data_structures.partially_retroactive_queue_and_stack.base import BaseNode, BaseOperation, \
    BasePartiallyRetroactive


class Node(BaseNode):
    def __init__(self, prev, next, value=None):
        super().__init__(prev, next, value)
        self.is_before_first = False


class Operation(BaseOperation):
    def __init__(self, time, node, is_enqueue):
        super().__init__(time, node)
        self.is_enqueue = is_enqueue


class PartiallyRetroactiveQueue(BasePartiallyRetroactive):
    def __init__(self):
        super().__init__()
        self.first = None
        self.last = None

    def is_initialized(self):
        if self.first is None and self.last is None:
            return False
        return True

    def get_first(self):
        return None if self.first is None else self.first.value

    def get_last(self):
        return None if self.last is None else self.last.value

    def insert_enqueue(self, value, time=None):

        """
        Insert enqueue operation at specific time. If time value already exists raise ValueError.
        Find operation after passed time value and add enqueue operation before it. If there is no operation after passed time value, add enqueue operation at the end.
        """

        if time is None:
            time = self.get_max_time() + 10

        if time in self.operations:
            raise ValueError

        if not self.is_initialized():
            node = Node(None, None, value)
            self.last = node
            self.first = node
            node.is_before_first = True
            operation = Operation(time, node, True)
            self.operations.append(operation)
            self.operations.sort(key=lambda x: x.time, reverse=True)
            return operation

        operation_after = self._find_operation_after_binary_search(time)
        if operation_after is None:
            node = Node(self.last, None, value)
            self.last.next = node
            self.last = node
        else:
            node_after = operation_after.node
            node = Node(node_after.prev, node_after, value)
            if node_after.prev is not None:
                node_after.prev.next = node
            node_after.prev = node
            if node_after.is_before_first:
                if self.first is not None:
                    self.first.is_before_first = False
                    self.first = self.first.prev
        operation = Operation(time, node, True)
        self.operations.append(operation)
        self.operations.sort(key=lambda x: x.time, reverse=True)
        return operation

    def insert_dequeue(self, time=None):

        """
        Insert dequeue operation at specific time. If time value already exists raise ValueError.
        Dequeue first node.
        """

        if time is None:
            time = self.get_max_time() + 10

        if time in self.operations:
            raise ValueError

        if not self.is_initialized():
            return None
        node_to_dequeue = self.first
        self.first = self.first.next
        if self.first is not None:
            self.first.is_before_first = True
        else:
            self.last = None
        operation = Operation(time, node_to_dequeue, False)
        self.operations.append(operation)
        self.operations.sort(key=lambda x: x.time, reverse=True)
        return operation

    def delete_operation(self, time):

        """
        Delete operation at specific time. If time value does not exists raise ValueError.
        If operation type is enqueue, remove enqueued node.
        if operation type is dequeue, put back dequeued node.
        """

        if time not in self.operations:
            raise ValueError

        operation = self._find_operation_binary_search(time)
        node, is_enqueue = (operation.node, operation.is_enqueue)
        if is_enqueue:
            if node.next is not None:
                node.next.prev = node.prev
            else:
                self.last = node.prev
            if node.prev is not None:
                node.prev.next = node.next
            if node.is_before_first:
                self.first = self.first.next
                self.first.is_before_first = True
        else:
            self.first.is_before_first = False
            node.next = self.first
            self.first = node
        return None

    def __iter__(self):
        node = self.first
        while node is not None:
            yield node.value
            if node == self.last:
                break
            node = node.next

    def __str__(self):
        queue = ", ".join(str(val) for val in self)
        return f"Queue = [{queue}]\t\t(First={self.get_first()}, Last={self.get_last()})"


if __name__ == '__main__':
    print("PARTIALLY RETROACTIVE QUEUE:")
    prq = PartiallyRetroactiveQueue()
    prq.insert_enqueue(value=2, time=10)
    print(prq)
    prq.insert_enqueue(value=4, time=20)
    print(prq)
    prq.insert_enqueue(value=6, time=30)
    print(prq)
    prq.insert_enqueue(value=10)
    print(prq)
    prq.insert_dequeue(time=28)
    print(prq)
    prq.insert_enqueue(value=8, time=15)
    print(prq)
    prq.insert_dequeue(time=16)
    print(prq)
    prq.delete_operation(time=40)
    print(prq)
    prq.delete_operation(time=28)
    print(prq)
    dequeue_operation = prq.insert_dequeue()
    print("First value: " + str(dequeue_operation.node))
    print(prq)
