from retroactive_data_structures.partially_retroactive_priority_queue.treap import Treap


class MinPrefixSumAggregator:
    """
    An aggregator for prefix sum data structure that supports finding the minimum prefix sum and its range.

    Attributes:
    - sum: The sum of all values in the prefix sum data structure.
    - min_key: The minimum key in the prefix sum data structure.
    - max_key: The maximum key in the prefix sum data structure.
    - min_prefix_sum: The minimum prefix sum in the prefix sum data structure.
    - min_prefix_first_key: The first key in the range that results in the minimum prefix sum.
    - min_prefix_last_key: The last key in the range that results in the minimum prefix sum.
    """

    def __init__(self, key, value):

        """
        Initializes a new instance of the MinPrefixSumAggregator class.

        Args:
        - key: The key of the new value to add to the prefix sum data structure.
        - value: The value to add to the prefix sum data structure.
        """

        self.sum = value
        self.min_key = key
        self.max_key = key
        self.min_prefix_sum = value
        self.min_prefix_first_key = key
        self.min_prefix_last_key = key

    def __add__(self, other):

        """
        Returns a new instance of the MinPrefixSumAggregator class that represents the combined prefix sum of this instance
        and another instance.

        Args:
        - other (MinPrefixSumAggregator): The other instance to combine with this instance.

        Returns:
        A new instance of the MinPrefixSumAggregator class that represents the combined prefix sum of this instance and
        another instance.
        """

        result = MinPrefixSumAggregator(None, 0)
        result.sum = self.sum + other.sum
        result.min_key = self.min_key
        result.max_key = other.max_key
        other_min_prefix_sum = self.sum + other.min_prefix_sum
        result.min_prefix_sum = min(self.min_prefix_sum, other_min_prefix_sum)

        if self.min_prefix_sum <= result.min_prefix_sum:
            result.min_prefix_first_key = self.min_prefix_first_key
        else:
            result.min_prefix_first_key = other.min_prefix_first_key
        if other_min_prefix_sum <= result.min_prefix_sum:
            result.min_prefix_last_key = other.min_prefix_last_key
        else:
            result.min_prefix_last_key = self.min_prefix_last_key
        return result

    def __str__(self):

        """
        Returns a string representation of this instance.

        Returns:
        A string representation of this instance.
        """

        return (
            "Ag(sum:{0.sum} min_key:{0.min_key} max_key:{0.max_key}) "
            # + "min_prefix_sum:{0.min_prefix_sum} min_prefix_first_key:{0.min_prefix_first_key} min_prefix_last_key:{0.min_prefix_last_key}"
        ).format(self)


class ZeroPrefixTreap(Treap):
    def __init__(self):

        """
        Initializes a ZeroPrefixTreap object, which is a subclass of the Treap class with a custom aggregation function.

        The aggregation function used is the sum of values associated with the keys in the treap.
        """

        super().__init__(lambda x, y: x + y)

    def zero_prefix_before(self, key):

        """
        Computes the key with the minimum prefix sum of values up to but not including the given key.

        Parameters:
        - key: The key to compute the minimum prefix sum before.

        Returns:
        - The key with the minimum prefix sum of values up to but not including the given key.
        """

        result = self.aggregate_before(key, include_eq=False)
        if result is None:
            return key
        elif result.min_prefix_sum > 0:
            return min(result.min_key, key)
        elif result.sum == 0:
            return max(result.min_prefix_last_key, key)
        else:
            return result.min_prefix_last_key

    def zero_prefix_after(self, key):

        """
        Computes the key with the minimum prefix sum of values after the given key.

        Parameters:
        - key: The key to compute the minimum prefix sum after.

        Returns:
        - The key with the minimum prefix sum of values after the given key, or None if no such key exists.
        """

        result = self.aggregate_after(key, include_eq=False)
        if result is None:
            return key
        before_sum = self.aggregate().sum - result.sum
        min_prefix_in_result = before_sum + result.min_prefix_sum
        if before_sum == 0:
            return key
        elif min_prefix_in_result == 0:
            return result.min_prefix_first_key
        else:
            return None

    def __getitem__(self, key):

        """
        Returns the sum of values associated with the given key in the treap.

        Parameters:
        - key: The key to retrieve the value sum for.

        Returns:
        - The sum of values associated with the given key in the treap.
        """

        return super().__getitem__(key).value.sum

    def __setitem__(self, key, value):

        """
        Sets the value associated with the given key in the treap to a MinPrefixSumAggregator object with the given value.

        Parameters:
        - key: The key to set the value for.
        - value: The value to set.
        """

        super().__setitem__(key, MinPrefixSumAggregator(key, value))

    def __iter__(self):

        """
        Returns an iterator over the keys and sum of values associated with each key in the treap.

        Returns:
        - An iterator over the keys and sum of values associated with each key in the treap.
        """

        for key, value in super().__iter__():
            yield key, value.sum
