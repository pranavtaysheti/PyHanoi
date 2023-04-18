# PyHanoi

This is a universal tower of hanoi solver, which can "theorotically" solve the
problem for any number of rings and any number of towers.

This doesn't use k-peg or any other algorithm. this program just brute-forces
until it finds ALL smallest solution (that's why this is universal). If
multiple smallest solution exists, then this shows all the possible solutions.
and other than normal tower of hanoi problems, it works for a problem going
from ANY state A to state B.

While the solution given should be correct - the time required to solve it
increases exponentially, with more towers and rings.

## Installation

If you are using linus simply do:

``` bash
pip install git+https://github.com/pranavtaysheti/PyHanoi.git
pyhanoi
```

## License

GNU General Public License v3.0 or later
