from __future__ import annotations

import unittest
from typing import TYPE_CHECKING
from copy import deepcopy

from pyhanoi import libhanoi

if TYPE_CHECKING:
    from libhanoi import TowerSet

class TestGraph(unittest.TestCase):
    
    def setUp(self):
        self.node_data: TowerSet = [[1,2,3,4],[],[]]
        self.rings = 4
        self.graph = libhanoi.Graph(self.node_data, self.rings)

    def test_init(self):
        self.assertEqual(self.graph.latest_nodes[0].data, self.node_data)

class TestNodePrototype(unittest.TestCase):

    def setUp(self):
        self.node_data: TowerSet = [[4,3,2,1],[],[]]
        self.node_prototype = libhanoi.NodePrototype(self.node_data)

    def test_patch(self):
        delta = (0,1)
        expected_data = [[4,3,2],[1],[]]
        new = deepcopy(self.node_prototype)
        new.patch(delta)
        self.assertEqual(new.data, expected_data)
    
    def test_check_validity(self):
        self.assertTrue(self.node_prototype.check_validity())
        false_np = libhanoi.NodePrototype([[4,3,1,2],[],[]])
        self.assertFalse(false_np.check_validity())

class TestNode(unittest.TestCase):
    
    def setUp(self):
        self.node_data: TowerSet

if __name__=="__main__":
    unittest.main()