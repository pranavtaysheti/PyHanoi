""" Hanoi Library Module """

from __future__ import annotations

from itertools import permutations
from typing import List, Optional, Tuple, Sequence
from copy import deepcopy, copy
from enum import Enum, auto

from pyhanoi.libcommon import pop_list, get_matching_index


class InvalidRingOrderError(Exception):
    pass


TowerSet = List[List[int]]
Connection = Tuple["Node", "Delta"]
ConnectionPrototype = Tuple["TowerSet", "Delta"]
Delta = Tuple[int, int]
History = Tuple["Node", List[Delta]]


class Graph:
    """Graph Class"""

    def __init__(self, start: TowerSet, rings: int):
        self.pinned: List[TowerSet] = []
        self.found_nodes: List[Node] = []
        self.rings = rings
        self.current_nodes: List[Node] = []
        self.next_nodes: List[Node] = []

        self.current_nodes.append(Node(start, self))

    def _check_pinned(self, node: Node):
        for index, term in enumerate(self.pinned):
            if term == node.data:
                self.pinned.pop(index)
    
    def _process_current(self):
        for node in self.current_nodes:
            node.propagate()
            self._check_pinned(node)

        self.current_nodes = self.next_nodes
        self.next_nodes = []

    def process(self):
        while self.current_nodes and self.pinned:
            self._process_current()

    def __repr__(self):
        return repr(
            {
                "pinned": self.pinned,
                "found_nodes": self.found_nodes,
                "rings": self.rings,
                "current_nodes": self.current_nodes,
                "next_nodes": self.next_nodes,
            }
        )


class NodeStage(Enum):
    CURRENT = auto()
    NEXT = auto()
    PROTOTYPE = auto()


class NodePrototype:
    def __init__(self, data: TowerSet):
        self.data = deepcopy(data)
        if not self.check_validity():
            raise InvalidRingOrderError

    def check_validity(self):
        for tower in self.data:
            sorted_tower = deepcopy(tower)
            sorted_tower.sort()
            sorted_tower.reverse()

            if sorted_tower != tower:
                return False

        return True

    def _is_patch_valid(self, delta: Delta):
        init, final = delta
        status = False

        if len(self.data[init]) > 0:
            if len(self.data[final]) == 0:
                status = True
            elif self.data[final][-1] > self.data[init][-1]:
                status = True

        return status

    def __repr__(self):
        return repr(self.data)

    def patch(self, delta: Delta):
        init, final = delta

        if self._is_patch_valid(delta):
            self.data[final].append(self.data[init].pop())
        else:
            raise InvalidRingOrderError


class Node(NodePrototype):
    """Node Class"""

    def __init__(self, data: TowerSet, graph: Graph):
        super().__init__(data)
        self.graph = graph
        self.connections: List[Node] = []
        self.mods: Optional[ModList] = None
        self.history: List[History] = []

    def _generate(self):
        self.mods = ModList(self)
        self.mods.generate()
        self.mods.filter_out([node.data for node in self.connections])

    def add_history(self, connection: Connection):
        node, delta = connection
        for history in node.history:
            node, log = history
            new_log = copy(log)
            new_log.append(delta)
            new_history = (node, new_log)
            self.history.append(new_history)
        self.history.append((node, [delta]))

    def connect(self, connection: Connection, stage: NodeStage):
        node, _ = connection

        self.connections.append(node)
        node.connections.append(self)

        if stage != NodeStage.CURRENT:
            self.add_history(connection)
        if stage == NodeStage.PROTOTYPE:
            self.graph.next_nodes.append(self)

    def __repr__(self):
        return repr(
            {
                "data": self.data,
                "connections": [node.data for node in self.connections],
                "mods": self.mods,
            }
        )

    def propagate(self):
        self._generate()

        if not self.mods:
            return None

        def connect_list(nodes: Sequence[Node], stage: NodeStage):
            if not self.mods:
                return None

            if NodeStage == NodeStage.PROTOTYPE:
                for i, (node, (_tower_set, delta)) in enumerate(
                    zip(nodes, self.mods.data)
                ):
                    node.connect((self, delta), NodeStage.PROTOTYPE)

                self.mods.data = []

            else:
                rml = []
                tsl = [node.data for node in nodes]
                for i, j in get_matching_index(
                    [ts for ts, _delta in self.mods.data], tsl
                ):
                    _tower_set, delta = self.mods.data[i]
                    nodes[j].connect((self, delta), stage)
                    rml.append(i)

                pop_list(rml, self.mods.data)

        connect_list(self.graph.current_nodes, NodeStage.CURRENT)
        connect_list(self.graph.next_nodes, NodeStage.NEXT)
        connect_list(
            [Node(ts, self.graph) for ts, _delta in self.mods.data], NodeStage.PROTOTYPE
        )


class ModList:
    def __init__(self, node: Node):
        self.data: List[ConnectionPrototype] = []
        self.node = node

    def generate(self):
        """Generates mods of the self"""

        for init, final in permutations(range(len(self.node.data)), 2):

            try:
                mod = NodePrototype(self.node.data)
                mod.patch((init, final))

            except InvalidRingOrderError:
                continue

            else:
                self.data.append((mod.data, (init, final)))

    def __iter__(self):
        return iter(self.data)

    def __repr__(self):
        return repr([{"tower_set": t, "delta": d} for t, d in self.data])

    def filter_out(self, tower_sets: List[TowerSet]):
        rml = [
            index_data
            for index_data, _index_tower_sets in get_matching_index(
                [ts for ts, _delta in self.data], tower_sets
            )
        ]
        pop_list(rml, self.data)
