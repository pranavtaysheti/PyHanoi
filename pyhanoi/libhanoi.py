""" Hanoi Library Module """

from __future__ import annotations

from itertools import permutations 
from typing import List, Optional, Tuple, Any
from copy import deepcopy, copy

class InvalidRingOrderError(Exception):
    pass

TowerSet = List[List[int]]
Connection = Tuple["Node", "Delta"]
ConnectionPrototype = Tuple["TowerSet", "Delta"]
Delta = Tuple[int, int]
History = Tuple["Node", List[Delta]]

class Graph():
    """ Graph Class """

    def __init__(self, start: TowerSet, rings: int):
        self.pinned: List[TowerSet] = []
        self.found_nodes: List[Node] = []
        self.rings = rings
        self.current_nodes: List[Node] = [Node(start, self)]
        self.next_nodes: List[Node] = []
        self.all_nodes = lambda : self.current_nodes + self.next_nodes

    def _check_pinned(self, node: Node):
        for term in self.pinned:
            if term == node.data:
                self.found_nodes.append(node)

    def _process_current(self):
        for node in self.current_nodes:
            node.propagate()
            self._check_pinned(node)
        
        self.current_nodes = self.next_nodes
        self.next_nodes = []
    
    def process(self):
        while self.current_nodes:
            self._process_current()
    
    def __repr__(self):
        return repr({
            "pinned": self.pinned,
            "found_nodes": self.found_nodes,
            "rings": self.rings,
            "current_nodes": self.current_nodes,
            "next_nodes": self.next_nodes
        })
    
class NodePrototype():

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

def pop_list(index_list: List[int], item_list: List[Any]):
    index_list.sort()
    index_list.reverse()

    for i in index_list:
        item_list.pop(i)

class Node(NodePrototype):

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
    
    def _copy_history(self, node: Node):
        for log in node.history:
            node, history = log
            new = (node, copy(history))
            self.history.append(new)
    
    def _add_history(self, connection: Connection):
        node, delta = connection
        self._copy_history(node)
        for _, log in self.history:
            log.append(delta)
        self.history.append((node, [delta]))
        
    def _connect_existing(self):
        node_list = self.graph.all_nodes()
        tsl = [node.data for node in node_list]
        rml = []

        if self.mods:
            for i,j in self.mods._get_mod_list(tsl):
                _, delta = self.mods.data[j]
                node_list[i]._connect((self, delta))
                rml.append(j)
        
            pop_list(rml, self.mods.data)
            
    def _connect(self, connection: Connection):
        node, delta = connection

        self.connections.append(node)
        self._add_history(connection)
        node.connections.append(self)
    
    def __repr__(self):
        return repr({
            "data": self.data,
            "connections": [node.data for node in self.connections],
            "mods": self.mods,
        })

    def propagate(self):
        self._generate()
        self._connect_existing()
        if not self.mods:
            return None
        
        while self.mods.data:
            mod = self.mods.data.pop()
            tower_set, delta = mod
            node = Node(tower_set, self.graph)

            node._connect((self, delta))
            self.graph.next_nodes.append(node)

class ModList():

    def __init__(self, node: Node):
        self.data: List[ConnectionPrototype] = []
        self.node = node

    def generate(self):
        """ Generates mods of the self """

        for init, final in permutations(range(len(self.node.data)),2):
            
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
    
    def _get_mod_list(self, tower_sets: List[TowerSet]):
        """ Gets index of item in list matching the arg 
        i: matching index of arg
        j: matching index from self.data
        """

        result: List[Tuple[int,int]] = []

        for i, term in enumerate(tower_sets):
            for j, mod in enumerate(self.data):
                tower_set, _ = mod
                if term == tower_set:
                    result.append((i,j))
        
        return result

    def filter_out(self, tower_sets: List[TowerSet]):
        rml = [index for _, index in self._get_mod_list(tower_sets)]
        pop_list(rml, self.data)
