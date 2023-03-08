from typing import TYPE_CHECKING, Optional

from pyhanoi.libhanoi import Graph

if TYPE_CHECKING:
    from pyhanoi.libhanoi import TowerSet

WELCOME_MESSAGE = "Welcome to quite bad tower of hanoi solver!"
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

def make_start_node(towers: int, rings: int) -> TowerSet:
    result: TowerSet = []
    
    for _ in range(towers):
        result.append([])
    for ring in range(rings, 0, -1):
        result[0].append(ring)
    
    return result

if __name__ == "__main__":

    print(WELCOME_MESSAGE)
    towers = ask(QUES_TOWERS)
    rings = ask(QUES_RINGS)

    graph = Graph(make_start_node(towers, rings), rings)

