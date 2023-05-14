from retroactive_data_structures.partially_retroactive_priority_queue.treap import Treap
from retroactive_data_structures.partially_retroactive_priority_queue.zero_prefix_treap import ZeroPrefixTreap


class PartiallyRetroactivePriorityQueue():
    """
    The PartiallyRetroactivePriorityQueue class represents a partially retroactive priority queue, which allows for adding and deleting elements in the past as well as querying the current minimum element.
    """

    def __init__(self):

        """
        Initializes a new PartiallyRetroactivePriorityQueue instance with an empty priority queue and supporting data structures.
        """

        self._queue_now = Treap(lambda x, y: None)
        self._inserts = Treap(min)
        self._deleted_inserts = Treap(max)
        self._bridges = ZeroPrefixTreap()

    def _insert_for_time(self, time):

        """
        Returns the value and time of the earliest insertion operation that happened before or at the given time, or None if there are no earlier insertions.
        """

        bridge = self._bridges.zero_prefix_before(time)
        insert_value, insert_time, insert_data = self._deleted_inserts.aggregate_after(
            bridge, include_eq=True
        )
        return insert_time, insert_value, insert_data

    def _min_for_time(self, time):

        """
        Returns the value and time of the minimum element in the priority queue that was inserted before or at the given time, or None if the priority queue is empty or all elements were inserted after the given time.
        """

        bridge = self._bridges.zero_prefix_after(time)
        if bridge is None:
            raise ValueError
        min_value, min_time, min_data = self._inserts.aggregate_before(
            bridge, include_eq=True
        )
        return min_time, min_value, min_data

    def _promote_to_queue(self, time, value, data):

        """
        Promotes an element with the given value and time to the current priority queue and updates the supporting data structures accordingly.
        """

        self._queue_now.insert(value, data)
        self._inserts[time] = (value, time, data)
        self._deleted_inserts.delete(time)
        self._bridges[time] = 0

    def _delete_from_queue(self, time, value, data):

        """
        Deletes an element with the given value and time from the current priority queue and updates the supporting data structures accordingly.
        """

        self._queue_now.delete(value)
        self._inserts.delete(time)
        self._deleted_inserts[time] = (value, time, data)
        self._bridges[time] = 1

    def _remove_delete_min(self, time):

        """
        Removes the earliest delete-min operation that happened at or after the given time, and promotes the corresponding inserted element to the current priority queue if any.
        """

        insert_time, insert_value, insert_data = self._insert_for_time(time)
        self._bridges.delete(time)
        self._promote_to_queue(insert_time, insert_value, insert_data)

    def _remove_insert_in_queue(self, time):

        """
        Removes the insertion operation with the given time from the partially retroactive priority queue, and updates the supporting data structures accordingly.
        """

        value = self._inserts[time].value[0]
        self._queue_now.delete(value)
        self._inserts.delete(time)
        self._bridges.delete(time)

    def _remove_deleted_insert(self, time):

        """
        Removes the deleted insertion operation with the given time from the partially retroactive priority queue, and promotes the corresponding inserted element to the current priority queue if any.
        """

        delete_time, delete_value, delete_data = self._min_for_time(time)
        self._delete_from_queue(delete_time, delete_value, delete_data)
        self._deleted_inserts.delete(time)
        self._bridges.delete(time)

    def add_insert(self, time, value, data):

        """
        Adds an insertion operation with the given value and time to the partially retroactive priority queue.

        Parameters:
        - time: The time at which the insertion is performed.
        - value: The value to be inserted at time time.

        Raises:
            KeyError: If the queue already contains an operation with time time.
        """

        if time in self._bridges:
            raise KeyError
        self._deleted_inserts[time] = (value, time, data)
        self._bridges[time] = 1
        insert_time, insert_value, insert_data = self._insert_for_time(time)
        self._promote_to_queue(insert_time, insert_value, insert_data)

    def add_delete_min(self, time):

        """
        Adds a delete-min operation at the given time to the partially retroactive priority queue, deleting the minimum element in the current priority queue at that time.

        Parameters:
        - time: The time at which the delete-min is performed.

        Raises:
        - KeyError: If the queue already contains an operation with time time.

        """
        if time in self._bridges:
            raise KeyError
        delete_time, delete_value, delete_data = self._min_for_time(time)
        self._bridges[time] = -1
        self._delete_from_queue(delete_time, delete_value, delete_data)

    def remove(self, time):

        """
        Removes an operation at the given time from the partially retroactive priority queue, either an insertion or a delete-min operation, and updates the supporting data structures accordingly.

        Parameters:
        - time: The time of the operation to be removed.

        Raises:
        - KeyError: If the queue does not contain an operation with time time.
        """

        if time not in self._bridges:
            raise KeyError
        op_type = self._bridges[time]
        if op_type < 0:
            self._remove_delete_min(time)
        elif op_type == 0:
            self._remove_insert_in_queue(time)
        else:
            self._remove_deleted_insert(time)

    def get_min(self):

        """
        Returns the minimum element in the current priority queue, or None if the priority queue is empty.
        """

        try:
            return self.__iter__().__next__()
        except StopIteration:
            return None

    def __iter__(self):

        """
        Returns an iterator over the elements in the current priority queue.
        """

        yield from self._queue_now

    def __len__(self):

        """
        Returns the number of elements in the current priority queue.
        """

        return len(self._queue_now)

    def __contains__(self, value):

        """
        Returns True if the given value is in the current priority queue, False otherwise.
        """

        return value in self._queue_now

    def __str__(self):

        """
        Returns a string representation of the current priority queue, in the format "PriorityQueue = [value1, value2, ...]".
        """

        queue = ", ".join(str(value[0]) for value in self)
        return f"PriorityQueue = [{queue}]"
