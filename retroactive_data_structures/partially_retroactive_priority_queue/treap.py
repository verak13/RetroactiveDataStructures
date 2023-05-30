import random

random.seed(1)


class TreapNode:
    def __init__(self, key, value, aggregate_func):

        """
        Initialize a new instance of TreapNode.

        Parameters:
        - key: The key of the node.
        - value: The value of the node.
        - aggregate_func: A function used to aggregate the values of nodes.
        """

        self.key = key
        self.value = value
        self.priority = random.random()
        self.aggregate_func = aggregate_func
        self.aggregate_value = value
        self.left = None
        self.right = None

    def left_rotate(self):

        """
        Perform a left rotation on the node.

        Returns:
        - The new root of the rotated subtree.
        """

        first_node = self
        second_node = first_node.right
        first_node.right = second_node.left
        second_node.left = first_node
        first_node = second_node
        second_node = first_node.left
        first_node.update_aggregate_value()
        second_node.update_aggregate_value()
        return first_node

    def right_rotate(self):

        """
        Perform a right rotation on the node.

        Returns:
        - The new root of the rotated subtree.
        """

        first_node = self
        second_node = first_node.left
        first_node.left = second_node.right
        second_node.right = first_node
        first_node = second_node
        second_node = first_node.right
        first_node.update_aggregate_value()
        second_node.update_aggregate_value()
        return first_node

    def split(self, key, eq_left=False):

        """
        Split the subtree rooted at this node by a key.

        Parameters:
        - key: The key to split the tree by.
        - eq_left: A flag indicating if nodes with keys equal to `key` should be placed in the left subtree.

        Returns:
        - A tuple of two TreapNodes representing the split subtrees.
        """

        root = self
        if root.key < key or (root.key == key and eq_left):
            split_left, split_right = (None, None) if root.right is None else root.right.split(key, eq_left)
            root.right = split_left
            root.update_aggregate_value()
            return root, split_right
        else:
            split_left, split_right = (None, None) if root.left is None else self.left.split(key, eq_left)
            root.left = split_right
            root.update_aggregate_value()
            return split_left, root

    def merge(self, right_tree):

        """
        Merge this node with another node.

        Parameters:
        - right_tree: The node to merge with.

        Returns:
        - The new root of the merged subtree.
        """

        if right_tree is None:
            return self
        elif self is None:
            return right_tree
        elif self.priority < right_tree.priority:
            self.right = right_tree if self.right is None else self.right.merge(right_tree)
            self.update_aggregate_value()
            return self
        else:
            right_tree.left = self.merge(right_tree.left)
            right_tree.update_aggregate_value()
            return right_tree

    def update_aggregate_value(self):

        """
        Update the aggregate value of this node and its children.
        """

        self.aggregate_value = self.value
        result = None
        for node in [self.left, self, self.right]:
            if node is None:
                continue
            elif result is None:
                result = node.aggregate_value
            else:
                result = self.aggregate_func(result, node.aggregate_value)
        self.aggregate_value = result

    def __iter__(self):

        """
        Perform an inorder traversal of the subtree rooted at this node.

        Yield:
        - A tuple containing the key and value of each node visited.
        """

        if self.left is not None:
            yield from self.left
        yield self.key, self.value
        if self.right is not None:
            yield from self.right

    def __str__(self, prefix=""):

        """
        Generate a string representation of the subtree rooted at this node.

        Parameters:
        - prefix: A prefix string used to format the output string.

        Returns:
        - A string representation of the subtree rooted at this node.
        """

        res = prefix + "|- Node k:{0.key} v:{0.value} p:{0.priority} agg:{0.aggregate_value}\n".format(self)
        if self.left is not None:
            res += self.left.__str__(prefix + "|  ")
        else:
            res += prefix + "|  |- None\n"
        if self.right is not None:
            res += self.right.__str__(prefix + "|  ")
        else:
            res += prefix + "|  |- None\n"
        return res


class Treap:
    def __init__(self, aggregate_func):

        """
        Initialize a new instance of Treap.

        Parameters:
        - aggregate_func: A function used to aggregate the values of nodes.
        """

        self._aggregate_func = aggregate_func
        self._root = None
        self._len = 0

    def _insert(self, node, key, value=None):

        """
        Insert a new node with a key and value into the subtree rooted at `node`.

        Parameters:
        - node: The root of the subtree to insert into.
        - key: The key of the node to insert.
        - value: The value of the node to insert.

        Returns:
        - The new node of the modified subtree.
        """

        if node is None:
            node = TreapNode(key, value, self._aggregate_func)
            self._len += 1
            return node
        if key < node.key:
            node.left = self._insert(node.left, key, value)
            if node.left.priority > node.priority:
                node = node.right_rotate()
        elif key > node.key:
            node.right = self._insert(node.right, key, value)
            if node.right.priority < node.priority:
                node = node.left_rotate()
        else:
            node.value = value
        return node

    def insert(self, key, value=None):

        """
        Insert a new node with a key and value into the Treap.

        Parameters:
        - key: The key of the node to insert.
        - value: The value of the node to insert.
        """

        self._root = self._insert(self._root, key, value)

    def _delete(self, node, key):

        """
        Delete the node with a given key from the subtree rooted at `node`.

        Parameters:
        - node: The root of the subtree to delete from.
        - key: The key of the node to delete.
        """

        if node is None:
            return False
        if node.key == key:
            if node.left is None and node.right is None:
                self._len -= 1
                return None
            elif node.left is None:
                self._len -= 1
                return node.right
            elif node.right is None:
                self._len -= 1
                return node.left
            else:
                if node.left.priority < node.right.priority:
                    node = node.right_rotate()
                    node.right = self._delete(node.right, key)
                else:
                    node = node.left_rotate()
                    node.left = self._delete(node.left, key)
        elif key < node.key:
            node.left = self._delete(node.left, key)
        else:
            node.right = self._delete(node.right, key)
        return node

    def delete(self, key):

        """
        Delete the node with a given key from the Treap.

        Parameters:
        - key: The key of the node to delete.

        Returns:
        - A boolean indicating whether or not the node was deleted.
        """

        if self.find(key) is None: return False
        self._root = self._delete(self._root, key)
        return True

    def _find(self, node, key):

        """
        Recursively searches the tree rooted at the given node to find a node with the specified key.

        Parameters:
        - node: The root node of the tree to search.
        - key: The key to search for in the tree.

        Returns:
        - The node with the specified key if found, or `None` otherwise.

        Raises:
        - KeyError if the key is not found in the Treap.
        """

        if node == None:
            return None
        if node.key == key:
            return node
        if key < node.key:
            return self._find(node.left, key)
        else:
            return self._find(node.right, key)

    def find(self, key):

        """
        Finds and returns the value associated with the given key.

        Parameters:
        - key: the key to search for

        Returns:
        - The value associated with the given key.

        Raises:
        - KeyError if the key is not found in the Treap.
        """

        return self._find(self._root, key)

    def aggregate_before(self, key, include_eq=False):

        """
        Aggregates the values of all nodes with keys less than or equal to the given key.

        Parameters:
        - key: the key to aggregate before
        - include_eq: whether or not to include nodes with keys equal to the given key

        Returns:
        - The aggregated value of all nodes with keys less than or equal to the given key.

        """

        before, after = (None, None) if self._root is None else self._root.split(key, eq_left=include_eq)
        result = before.aggregate_value if before is not None else None
        self._root = after if before is None else before.merge(after)
        return result

    def aggregate_after(self, key, include_eq=False):

        """
        Aggregates the values of all nodes with keys greater than or equal to the given key.

        Parameters:
        - key: the key to aggregate after
        - include_eq: whether or not to include nodes with keys equal to the given key

        Returns:
        - The aggregated value of all nodes with keys greater than or equal to the given key.

        """

        before, after = (None, None) if self._root is None else self._root.split(key, eq_left=not include_eq)
        result = after.aggregate_value if after is not None else None
        self._root = after if before is None else before.merge(after)
        return result

    def aggregate(self):

        """
        Aggregates the values of all nodes in the Treap.

        Returns:
        - The aggregated value of all nodes in the Treap.
        """

        return self._root.aggregate_value if self._root else None

    def __getitem__(self, key):

        """
        Returns the value associated with the given key.

        Parameters:
        - key: the key to search for

        Returns:
        - The value associated with the given key.

        Raises:
        - KeyError if the key is not found in the Treap.
        """

        return self.find(key)

    def __contains__(self, key):

        """
        Checks if the given key is in the Treap.

        Parameters:
        - key: the key to search for

        Returns:
        - True if the key is in the Treap, False otherwise.
        """

        try:
            self.__getitem__(key)
            return True
        except KeyError:
            return False
        except AttributeError:
            return False

    def __setitem__(self, key, value):

        """
        Inserts or updates a node with the given key and value.

        Parameters:
        - key: the key to insert or update
        - value: the value to associate with the given key

        """

        self._root = self._insert(self._root, key, value)

    def __len__(self):

        """
        Returns the number of nodes in the Treap.
        """

        return self._len

    def __iter__(self):

        """
        Returns an iterator over the keys of the treap in ascending order.
        """

        if self._root is not None:
            yield from self._root

    def __str__(self):

        """
        Returns a string representation of the treap root.
        """

        return self._root.__str__()
