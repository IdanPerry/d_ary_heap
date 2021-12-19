"""
Implementation of d-ary heap data structure.

D-ary heap is a generalization of the binary heap, where d represents
the number of children. further explanation could be found in Wikipedia:
https://en.wikipedia.org/wiki/D-ary_heap

Most of the methods implementations were relied on the binary heap pseudo-code
routines found in Introduction to Algorithms book by Thomas H. Cormen,
Charles E. Leiserson, Ronald L. Rivest, and Clifford Stein, with d-ary heap adjustments.
"""


class DAryHeap:
    """
    Represents a d-ary heap data structure.

    ...

    Attributes
    ----------
    _heap
        The list which represents the heap data structure.

    _heap_size
        The length of the heap list.

    _children
        The number of children a node should have.

    Methods
    -------
    k_child(k_child: int, parent_index: int)
        Returns the k'th child of the specified index.

    parent(self, child_index: int)
        Returns the parent of the specified node index.

    build_max_heap(self, data: list)
        Construct the heap with the specified data.

    max_heapify(self, heap: list, node: int)
        Given a heap that violates the max-heap property at the
        specified node, max_heapify restores the heap structure.
    """

    def __init__(self, heap_size: int, children: int):
        """
        Parameters
        ----------
        children : int
            The number of children nodes each parent should have.
        """

        if children < 2:
            raise IllegalChildrenError('Illegal children parameter, '
                                       'must be equal to or greater then 2.')

        self._children = children
        self._heap = []
        self._heap_size = heap_size

    def __repr__(self):
        return str(self._heap)

    @staticmethod
    def _swap(array: list, index_a: int, index_b: int) -> None:
        """
        Swaps the list's elements specified by the respective indexes.
        """

        temp = array[index_a]
        array[index_a] = array[index_b]
        array[index_b] = temp

    def k_child(self, k_child: int, parent_index: int) -> int:
        """
        Returns the k'th child of the specified index.

        Parameters
        ----------
        k_child : int
            The k'th child to be returned.

        parent_index : int
            The index of the k'th child's parent.

        Returns
        -------
        The k'th child index.
        """

        return self._children * parent_index + k_child

    def parent(self, child_index: int) -> int:
        """
        Returns the parent of the specified node index.

        Parameters
        ----------
        child_index : int
            The parent's child's index.

        Returns
        -------
        The parent of the specified index.
        """

        return (child_index-1) // self._children

    def _find_max(self, heap: list, parent_index: int) -> int:
        # Returns the value of the specified parent_index if it's
        # greater then any of it's children, otherwise returns the
        # children's maximum value.

        max_value = parent_index

        for k in range(1, self._children + 1):
            child = self.k_child(k, parent_index)

            if child < self._heap_size and heap[child] > heap[max_value]:
                max_value = child

        return max_value

    def build_max_heap(self, data: list) -> None:
        """
        Construct the heap with the specified data.

        Parameters
        ----------
        data : list
            The data to build the heap with.
        """

        self._heap = data

        for i in range(self._heap_size // 2 - 1, -1, -1):
            self.max_heapify(self._heap, i)

    def max_heapify(self, heap: list, node: int) -> None:
        """
        Given a heap that violates the max-heap property at the
        specified node, max_heapify restores the heap structure.

        Parameters
        ----------
        heap : list
            The heap to restore it's structure.

        node : int
            The node index which violates the heap property.
        """

        largest = self._find_max(heap, node)

        if largest != node:
            self._swap(heap, node, largest)
            self.max_heapify(heap, largest)

    def increase_key(self, index: int, key: int) -> None:
        """
        Increases the key of the node at the specified index, to the specified key.

        Parameters
        ----------
        index : int
            The index at which the value should be increased.

        key : int
            The key target to increase to.
        """

        if key <= self._heap[index]:
            raise IllegalKeyError(f'{key}<={self._heap[index]}: Key must be greater'
                                  ' then the value at the specified index.')

        self._heap[index] = key
        while index > 0 and key > self._heap[self.parent(index)]:
            self._swap(self._heap, index, self.parent(index))
            index = self.parent(index)

    def max_heap_insert(self, key: int) -> None:
        """
        Inserts the specified key into the heap.

        Parameters
        ----------
        key : int
            The key to be inserted into the heap.
        """

        self._heap_size += 1
        self._heap.append(key)
        index = self._heap_size - 1

        while index > 0 and key > self._heap[self.parent(index)]:
            self._swap(self._heap, index, self.parent(index))
            index = self.parent(index)

    def delete_key(self, key: int) -> None:
        """
        Deletes the specified key from the heap.

        Parameters
        ----------
        key : int
            The key to be deleted from the heap.
        """

        if key >= self._heap_size or key < 0:
            raise IndexError(f'Key={key} is out of heap range.')

        self._heap[key] = self._heap[self._heap_size - 1]
        self._heap.pop()
        self._heap_size -= 1

        while 1 <= key < self._heap_size and self._heap[self.parent(key)] < self._heap[key]:
            self._swap(self._heap, key, self.parent(key))
            key = self.parent(key)

        self.max_heapify(self._heap, key)

    def extract_max(self) -> int:
        """
        Deletes and returns the maximum key value from the heap.

        Returns
        -------
        The maximum key value from the heap.
        """

        if self._heap_size < 1:
            raise HeapUnderflowError("Can't extract element out of an empty heap.")

        max_value = self._heap[0]
        self._heap[0] = self._heap[self._heap_size - 1]
        self._heap.pop()
        self._heap_size -= 1
        self.max_heapify(self._heap, 0)

        return max_value

    def heap_sort(self, array: list) -> None:
        """
        Sorts the specified list in ascending order.

        Parameters
        ----------
        array : list
            The list to be sorted.
        """

        self._heap_size = len(array)
        temp_size = self._heap_size
        self.build_max_heap(array)

        for i in range(self._heap_size - 1, 0, -1):
            self._swap(array, 0, i)
            self._heap_size -= 1
            self.max_heapify(array, 0)

        self._heap_size = temp_size


class IllegalChildrenError(Exception):
    def __init__(self, message):
        super().__init__(message)


class IllegalKeyError(Exception):
    def __init__(self, message):
        super().__init__(message)


class HeapUnderflowError(Exception):
    def __init__(self, message):
        super().__init__(message)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
