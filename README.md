Pathfinding is the problem of finding a path between two points on a plane. It is a fundamental task in robotics and AI. Perhaps the most obvious usage of pathfinding is in computer games, when an object is instructed to move from its current position to a goal position, while avoiding obstacles (e.g., walls, enemy fire) along the way.

Pathfinding in commercial games is frequently accomplished using search algorithms1. We consider a simplified version in this assignment. The following shows a 2D map drawn using ASCII characters:

1 1 1 1 1 1 4 7 8 X
1 1 1 1 1 1 1 5 8 8
1 1 1 1 1 1 1 4 6 7
1 1 1 1 1 X 1 1 3 6
1 1 1 1 1 X 1 1 1 1
1 1 1 1 1 1 1 1 1 1
6 1 1 1 1 X 1 1 1 1
7 7 1 X X X 1 1 1 1
8 8 1 1 1 1 1 1 1 1
X 8 7 1 1 1 1 1 1 1
Given a start position and an end position on the map, our aim is to find a path from the start position to the end position. The character 'X' denotes an obstacle that cannot be traversed by a path, while the digits represent the elevation at the respective positions.

Any position is indicated by the coordinates (i, j), where i is the row number (ordered top to bottom) and j is the column number (ordered left to right). For example, the top left position is (1, 1), the bottom right is (10, 10), while the position with elevation 3 is (4, 9). Given start position (1, 1) and end position (10, 10), a possible path is:

* * * 1 1 1 4 7 8 X
1 1 * 1 1 1 1 5 8 8
1 1 * * * * * * * 7
1 1 1 1 1 X 1 1 * 6
1 1 1 1 1 X 1 * * 1
1 1 1 1 1 1 1 * 1 1
6 1 1 1 1 X 1 * * *
7 7 1 X X X 1 1 1 *
8 8 1 1 1 1 1 1 1 *
X 8 7 1 1 1 1 1 1 *
Note that we use 4-connectedness for paths, which means any two points on the path are only connected if they are vertically or horizontally (but not diagonally) adjacent.

Problem Formulation
Following the lecture notes, we formulate the problem as follows:

States: Any obstacle-free position (i, j) on the map.
Initial States: A position (i0, j0) given by the user.
Actions: Since we consider 4-connectedness, only four actions are available: Up, down, left and right (your program must expand each node in this order). Available actions for positions adjacent to the map boundary or obstacles are reduced accordingly.
Transition Model: Moving left moves the current position to the left, etc.
Goal Test: Check if the current state is the end position (i*, j*) given by the user.
Path Cost: Given a map M and a Path P{(i0, j0), (i1, j1), ... (iN, jN)}, the cost of the path is calculated as:

where


and M(a, b) is the elevation at the position (a, b). In words, the cost of a path is the sum of the costs between adjacent points in the path, and the cost between adjacent points is 1 plus the difference between the elevation of the two points if we climb "uphill" or simply 1 if we stay "level" or slide "downhill".

This means shorter paths which avoid climbing cost less. As an example, the cost in the path in the previous page is 25. What is the optimal (i.e., cheapest) path?

Your Tasks
Solve this pathfinding task using three different methods:

Breadth First Search (BFS)
Uniform Cost Search (UCS)
A* Search (A*)
You should base your program on the pseudocode GRAPH-SEARCH see below, and carefully think about the appropriate data structures to use.

function GRAPH-SEARCH (problem, fringe) returns a solution, or failure
    closed <- an empty set
    fringe <- INSERT(MAKE-NODE(INITIAL-STATE[problem]), fringe)
    loop do
        if fringe is empty then return failure
        node <- REMOVE-FRONT(fringe)
        if GOAL-TEST(problem, STATE[node]) then return node
        if STATE[node] is not in closed then
            add STATE[node] to closed
            fringe <- INSERTALL(EXPAND(node, problem), fringe)
    end
 

A* search requires a heuristic. In this assignment, you must implement two such heuristics.

The Euclidean distance between current position and end position.
The Manhattan distance between the current position and end position.
For the map above with start position (1, 1) and end position (10, 10), your program should help you answer these questions:

Are the paths returned by the three methods different?
What about the optimality of the returned paths?
Which method is the most computationally and memory efficient?
Do the two heuristics for A* Search provide different solutions?
Does checking for repeated states matter in this problem?
Deliverables
Write your pathfinding program in Python 3.6.9 in a file called pathfinder.py. Your program must be able to run as follows:

>>> python pathfinder.py [map] [algorithm] [heuristic]

The inputs to the program are as follow:

[map] specifies the path to the map, which is a text file formatted according to this example:
10 10
1 1
10 10
1 1 1 1 1 1 4 7 8 X
1 1 1 1 1 1 1 5 8 8
1 1 1 1 1 1 1 4 6 7
1 1 1 1 1 X 1 1 3 6
1 1 1 1 1 X 1 1 1 1
1 1 1 1 1 1 1 1 1 1
6 1 1 1 1 X 1 1 1 1
7 7 1 X X X 1 1 1 1
8 8 1 1 1 1 1 1 1 1
X 8 7 1 1 1 1 1 1 1
The first line indicates the size of the map (rows, columns), while the second and third line represent the start and end positions respectively. The map then follows where all elevation values are integers from 0 to 9 inclusive.
[algorithm] specifies the search algorithm to use, with the possible values of bfs, ucs, and astar.
[heuristic] specifies the heuristic to use for A* search, with the possible values of euclidean and manhattan. This input is ignored for BFS and UCS.
Your program must then print to standard output the path returned by the search algorithm in the following format:

* * * 1 1 1 4 7 8 X
1 1 * 1 1 1 1 5 8 8
1 1 * * * * * * * 7
1 1 1 1 1 X 1 1 * 6
1 1 1 1 1 X 1 * * 1
1 1 1 1 1 1 1 * 1 1
6 1 1 1 1 X 1 * * *
7 7 1 X X X 1 1 1 *
8 8 1 1 1 1 1 1 1 *
X 8 7 1 1 1 1 1 1 *
where the path is indicated by asterisks *, superimposed on the original map beginning from the start position and leading to the end position. Do not include extraneous spaces or other characters in the output.

If the given map or problem does not have a feasible path, your program must print:

null
