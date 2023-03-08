from typing import TYPE_CHECKING, Optional, List

from pyhanoi.libhanoi import Graph, Delta, TowerSet

if TYPE_CHECKING:
    from pyhanoi.libhanoi import TowerSet

WELCOME_MESSAGE = "Welcome to very over-engineered tower of hanoi solver!"
QUES_TOWERS = "Enter the number of towers in hanoi:"
QUES_RINGS = "Enter the number of rings in hanoi:"

def ask(ques: str) -> int:
    result: Optional[int] = None
    
    while not result:
        print (ques)
        inp = input()    
        try:
            result = int(inp)
        except ValueError:
            print ("Enter an integer, ex-3")

    return result

def make_node(towers: int, rings: int, full_tower: int = 0) -> TowerSet:
    result: TowerSet = []
    
    for _ in range(towers):
        result.append([])
    for ring in range(rings, 0, -1):
        result[full_tower].append(ring)
    
    return result

def print_log(log: List[Delta]):
    for block in log:
        init, final = block
        print ("Move Ring from tower", init, "to tower", final)

if __name__ == "__main__":

    print(WELCOME_MESSAGE)
    towers = ask(QUES_TOWERS)
    rings = ask(QUES_RINGS)

    start_tower = make_node(towers, rings)
    graph = Graph(start_tower, rings)
    graph.pinned.append(make_node(towers, rings, towers-1))
    graph.process()

    if graph.found_nodes:
        node = graph.found_nodes[0]
    
        for history in node.history:
            n, log = history
            if n.data == start_tower:
                print_log(log)

        

