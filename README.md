# Page_Allocator
This is a design exercise to develop a program that simulates memory management on a paging system.

The memory manager will simulate a multiprogramming system, where
several processes can be resident in the simulated physical memory.
The "execution sequence" of these simulated processes will be provided
from a trace tape input file. Each line in the trace tape specifies either
arrival or termination of a process.
* Process arrival
    Encoded as three integers separated by spaces:

    _*pid codesize datasize*_

    Sizes are given in bytes.

* Process termination

    Encoded as two integers separated by a space with the second number
being -1.

    _*pid -1*_
