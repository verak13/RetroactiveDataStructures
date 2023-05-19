class BaseNode():
    def __init__(self, prev, next, value=None):
        self.value = value
        self.prev = prev
        self.next = next

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        prev = self.prev.value if self.prev is not None else None
        next = self.next.value if self.next is not None else None
        return str(self.value) + " " + str(prev) + "-" + str(next)


class BaseOperation():
    def __init__(self, time, node):
        self.time = time
        self.node = node

    def __eq__(self, other):
        if isinstance(other, int):
            return self.time == other
        elif isinstance(other, BaseOperation):
            return self.time == other.time
        return NotImplemented


class BasePartiallyRetroactive():
    def __init__(self):
        self.operations = []

    def get_max_time(self):

        """
        Find maximum time value. When no time is passed to operation, this value will be incremented by 10.
        """

        return max(self.operations, key=lambda x: x.time).time

    def is_initialized(self):
        pass

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
