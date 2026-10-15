"""Implementación enlazada real: no usa list para los enlaces internos."""
from typing import Generic, Iterator, Optional, TypeVar

T = TypeVar('T')


class RiddleStation(Generic[T]):
    def __init__(self, value: T):
        self.value = value
        self.next: 'RiddleStation[T]' = self
        self.prev: 'RiddleStation[T]' = self


class RiddleCircuit(Generic[T]):
    def __init__(self):
        self.head: Optional[RiddleStation[T]] = None
        self.size = 0

    def __len__(self) -> int:
        return self.size

    def node_at(self, index: int) -> RiddleStation[T]:
        if not 0 <= index < self.size:
            raise IndexError('Posición inexistente.')
        assert self.head is not None
        node = self.head
        if index <= self.size // 2:
            for _ in range(index):
                node = node.next
        else:
            for _ in range(self.size - index):
                node = node.prev
        return node

    def insert(self, index: int, value: T) -> None:
        if not 0 <= index <= self.size:
            raise IndexError('Posición inexistente.')
        new = RiddleStation(value)
        if self.head is None:
            self.head = new
        else:
            next_node = self.head if index == self.size else self.node_at(index)
            before = next_node.prev
            before.next = new
            new.prev = before
            new.next = next_node
            next_node.prev = new
            if index == 0:
                self.head = new
        self.size += 1

    def append(self, value: T) -> None:
        self.insert(self.size, value)

    def remove_at(self, index: int) -> T:
        node = self.node_at(index)
        if self.size == 1:
            self.head = None
        else:
            node.prev.next = node.next
            node.next.prev = node.prev
            if node is self.head:
                self.head = node.next
        self.size -= 1
        return node.value

    def replace(self, index: int, value: T) -> None:
        self.node_at(index).value = value

    def get(self, index: int) -> T:
        return self.node_at(index).value

    def next_index(self, index: int) -> int:
        self.node_at(index)
        return (index + 1) % self.size

    def previous_index(self, index: int) -> int:
        self.node_at(index)
        return (index - 1) % self.size

    def __iter__(self) -> Iterator[T]:
        if self.head is None:
            return
        node = self.head
        for _ in range(self.size):
            yield node.value
            node = node.next

    def reversed_items(self) -> Iterator[T]:
        if self.head is None:
            return
        node = self.head.prev
        for _ in range(self.size):
            yield node.value
            node = node.prev

    def validate_links(self) -> bool:
        if self.size == 0:
            return self.head is None
        if self.head is None:
            return False
        seen = set()
        node = self.head
        for _ in range(self.size):
            if id(node) in seen or node.next.prev is not node or node.prev.next is not node:
                return False
            seen.add(id(node))
            node = node.next
        return node is self.head and len(seen) == self.size
