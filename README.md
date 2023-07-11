# PyHanoi

This is a universal tower of hanoi solver, which can "theorotically" solve the
problem for any number of rings and any number of towers.

This doesn't use k-peg or any other algorithm. this program just brute-forces
until it finds smallest solution (that's why this is universal) and other than
normal tower of hanoi problems, it works for a problem going from ANY state A
to state B.

While the solution given should be correct - the time required to solve it
increases exponentially, with more towers and rings.

## Roadmap

- [ ] Show all possible solutions instead of 1
- [ ] Improve main.py
  - [ ] Ability to manually define initial state
- [ ] Optimizations:
  - [ ] Ability to recognize symmetry during problem solving step.

## Installation

soon will write a `setup.py`.

for now just git clone this repo:

``` bash
git clone https://github.com/pranavtaysheti/PyHanoi
cd PyHanoi
python -m pyhanoi
```

## License

GNU General Public License v3.0 or later
