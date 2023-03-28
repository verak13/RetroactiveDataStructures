class Node():
    def __init__(self, prev, next, value=None):
        self.value = value
        self.prev = prev
        self.next = next
        self.is_before_first = False

    def __str__(self):
        return str(self.value)


class Operation():
    def __init__(self, time, node, is_enqueue):
        self.time = time
        self.node = node
        self.is_enqueue = is_enqueue

    def __eq__(self, other):
        if isinstance(other, int):
            return self.time == other
        elif isinstance(other, Operation):
            return self.time == other.time
        return NotImplemented


class PartiallyRetroactiveQueue():
    def __init__(self):
        self.first = None
        self.last = None
        self.operations = []

    def is_initialized(self):
        if self.first is None and self.last is None:
            return False
        return True

    def get_first(self):
        return None if self.first is None else self.first.value

    def get_last(self):
        return None if self.last is None else self.last.value

    def get_max_time(self):

        """
        Find maximum time value. When no time is passed to enqueue or dequeue operation, this value will be incremented by 10.
        """

        return max(self.operations, key=lambda x: x.time).time

    def _find_operation(self, time):

        """
        Find the Operation object with the given time value. If no such object exists, return None.
        """

        operations_at_time = filter(lambda x: x.time == time, self.operations)
        list_operations_at_time = list(operations_at_time)
        if len(list_operations_at_time) == 0:
            return None
        return list_operations_at_time[0]

    def _find_operation_binary_search(self, time):

        """
        Find the Operation object with the given time value using binary search.
        If no such object exists, return None.
        Note that this implementation assumes that self.operations is already sorted in descending order by time.
        """

        if not self.operations:
            return None
        left = 0
        right = len(self.operations) - 1
        while left <= right:
            mid = (left + right) // 2
            if time == self.operations[mid].time:
                return self.operations[mid]
            elif time > self.operations[mid].time:
                right = mid - 1
            else:
                left = mid + 1
        return None

    def _find_operation_after(self, time):

        """
        Filter the list to only keep Operation objects whose time value is greater than passed time value.
        Find the minimum object from the filtered list based on its time value. Otherwise, None is returned.
        """

        operations_after = filter(lambda x: x.time > time, self.operations)
        list_operations_after = list(operations_after)
        if len(list_operations_after) == 0:
            return None
        min_operation_after = min(list_operations_after, key=lambda x: x.time)
        return min_operation_after

    def _find_operation_after_binary_search(self, time):

        """
        Find the smallest time value of Operation object that is larger than the passed time value using binary search.
        Otherwise, None is returned. Note that this implementation assumes that self.operations is already sorted in descending order by time.
        """

        if not self.operations or self.operations[0].time <= time:
            return None
        left = 0
        right = len(self.operations) - 1
        while left <= right:
            mid = (left + right) // 2
            if time < self.operations[mid].time:
                if mid == 0 or time >= self.operations[mid + 1].time:
                    return self.operations[mid]
                else:
                    left = mid + 1
            else:
                right = mid - 1
        return None

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
            if node_after.prev != None:
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
        Insert operation at specific time. If time value does not exists raise ValueError.
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