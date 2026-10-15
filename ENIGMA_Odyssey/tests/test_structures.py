import unittest
from structures.riddle_circuit import RiddleCircuit


class RiddleCircuitTests(unittest.TestCase):
    def test_empty(self):
        chain = RiddleCircuit()
        self.assertTrue(chain.validate_links())
        self.assertEqual(list(chain), [])
        with self.assertRaises(IndexError): chain.get(0)

    def test_single_circular(self):
        chain = RiddleCircuit()
        chain.append('A')
        self.assertIs(chain.head.next, chain.head)
        self.assertIs(chain.head.prev, chain.head)
        self.assertTrue(chain.validate_links())

    def test_insertion_forward_backward(self):
        chain = RiddleCircuit()
        for x in ['A', 'C']: chain.append(x)
        chain.insert(1, 'B')
        chain.insert(0, 'START')
        self.assertEqual(list(chain), ['START', 'A', 'B', 'C'])
        self.assertEqual(list(chain.reversed_items()), ['C', 'B', 'A', 'START'])
        self.assertEqual(chain.next_index(3), 0)
        self.assertEqual(chain.previous_index(0), 3)
        self.assertTrue(chain.validate_links())

    def test_delete_replace(self):
        chain = RiddleCircuit()
        for x in [1, 2, 3]: chain.append(x)
        self.assertEqual(chain.remove_at(0), 1)
        chain.replace(1, 4)
        self.assertEqual(list(chain), [2, 4])
        self.assertTrue(chain.validate_links())
        chain.remove_at(1)
        chain.remove_at(0)
        self.assertTrue(chain.validate_links())
