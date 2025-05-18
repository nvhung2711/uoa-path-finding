from collections import deque
import heapq
import math
import sys

#getting the input
my_map = sys.argv[1]

with open(my_map, 'r') as f:
    f_cont = f.read()

#separate each line
line_in_file = f_cont.split('\n')

rows, cols = line_in_file[0].split(' ')
begin = [1, 1]
end = [1,1]
begin[0], begin[1] = line_in_file[1].split(' ')
end[0], end[1] = line_in_file[2].split(' ')

#convert to int
rows = int(rows)
cols = int(cols)
begin[0] = int(begin[0])
begin[1] = int(begin[1])
end[0] = int(end[0])
end[1] = int(end[1])

#get inputs for map
map_in_file = line_in_file[3:]
Map = []

for row in map_in_file:
    element = row.split(' ')
    Map.append(element)

#what algorithm do we want to apply to the map
algorithm = sys.argv[2]
if algorithm == 'astar':
    heuristic = sys.argv[3]

##########################################################

#convert to 0-index system
begin[0] -= 1
begin[1] -= 1
end[0] -= 1
end[1] -= 1

#check if the position valid
def validPosition(m, node):
    r = node.pos[0] #row
    c = node.pos[1] #col

    if r < 0 or r >= rows or c < 0 or c >= cols:
        return False
    elif m[r][c] == 'X':
        return False
    return True

#draw the path on map
def draw_path(m, start, path):
    if path != '':
        r = start[0]
        c = start[1]
        m[r][c] = '*'
        for direction in path:
            if direction == 'U':
                r -= 1
            elif direction == 'D':
                r += 1
            elif direction == 'L':
                c -= 1
            elif direction == 'R':
                c += 1
            m[r][c] = '*'
    
    for row in m:
        for point in row:
            print(point, end=' ')
        print()

    return None

########################################################

#breadth first search
def bfs(m, start, goal):
    """
    This function takes two points on the map as the starting point and goal
    OUTPUT:
    The path from start to goal as in U D L R
    """
    ans = []
    #set up the queue and visited set
    fringe = deque([(start[0], start[1], "")])
    visited = set()

    found = False
    #start poping until the list is empty or reach the goal
    while not found and fringe:
        r, c, path = fringe.popleft()

        #if out of bounds or obstacle
        if r < 0 or c < 0 or r >= rows or c >= cols or m[r][c] == 'X':
            continue
        
        #if visited already
        if (r,c) in visited:
            continue
        visited.add((r,c))

        #reach goal
        if [r,c] == goal:
            ans = path
            found = True
            continue

        fringe.append((r - 1, c, path + "U")) #up
        fringe.append((r + 1, c, path + "D")) #down
        fringe.append((r, c - 1, path + "L")) #left
        fringe.append((r, c + 1, path + "R")) #right
 
    return ans


#Uniform cost search
def ucs(m, start, goal):
    """
    This function takes two points on the map as the starting point and goal
    OUTPUT:
    The path from start to goal as in U D L R
    """
    ans = ""
    #set up the min heap
    fringe = [[0, 0, 0, start[0], start[1], ""]] #cost, time, udlr order, row, col, path
    heapq.heapify(fringe)
    visited = set()

    found = False
    #start poping until the list is empty or reach the goal
    while not found and fringe:
        cost, time, udlr, r, c, path = heapq.heappop(fringe)

        #if out of bounds or obstacle
        if r < 0 or c < 0 or r >= rows or c >= cols or m[r][c] == 'X':
            continue
        
        #if visited already
        if (r,c) in visited:
            continue
        visited.add((r,c))

        #reach goal
        if [r,c] == goal:
            ans = path
            found = True
            continue

        if r >= 1 and m[r-1][c] != 'X':
            heapq.heappush(fringe, [cost + max(0, int(m[r-1][c]) - int(m[r][c])) + 1, time + 1, 4, r - 1, c, path + "U"]) #up
        if r < rows - 1 and m[r+1][c] != 'X':
            heapq.heappush(fringe, [cost + max(0, int(m[r+1][c]) - int(m[r][c])) + 1, time + 1, 3, r + 1, c, path + "D"]) #down
        if c >= 1 and m[r][c-1] != 'X':
            heapq.heappush(fringe, [cost + max(0, int(m[r][c-1]) - int(m[r][c])) + 1, time + 1, 2, r, c - 1, path + "L"]) #left
        if c < cols - 1 and m[r][c+1] != 'X':
            heapq.heappush(fringe, [cost + max(0, int(m[r][c+1]) - int(m[r][c])) + 1, time + 1, 1, r, c + 1, path + "R"]) #right

    return ans


def astar_manhattan(m, start, goal):
    """
    This function takes two points on the map as the starting point and goal using a* algo to find shortest part with euclidean heuristic
    OUTPUT:
    The path from start to goal as in U D L R
    """
    ans = ""
    #set up the min heap
    fringe = [[0, 0, 0, start[0], start[1], ""]] #cost, time, udlr order, row, col, path
    heapq.heapify(fringe)
    visited = set()

    found = False
    #start poping until the list is empty or reach the goal
    while not found and fringe:
        cost, time, udlr, r, c, path = heapq.heappop(fringe)

        #if out of bounds or obstacle
        if r < 0 or c < 0 or r >= rows or c >= cols or m[r][c] == 'X':
            continue
        
        #if visited already
        if (r,c) in visited:
            continue
        visited.add((r,c))

        #reach goal
        if [r,c] == goal:
            ans = path
            found = True
            continue

        if r >= 1 and m[r-1][c] != 'X':
            heapq.heappush(fringe, [cost + max(0, int(m[r-1][c]) - int(m[r][c])) + 1 + abs(goal[0] - (r-1)) + abs(goal[1] - c), time + 1, 4, r - 1, c, path + "U"]) #up
        if r < rows - 1 and m[r+1][c] != 'X':
            heapq.heappush(fringe, [cost + max(0, int(m[r+1][c]) - int(m[r][c])) + 1 + abs(goal[0] - (r+1)) + abs(goal[1] - c), time + 1, 3, r + 1, c, path + "D"]) #down
        if c >= 1 and m[r][c-1] != 'X':
            heapq.heappush(fringe, [cost + max(0, int(m[r][c-1]) - int(m[r][c])) + 1 + abs(goal[0] - r) + abs(goal[1] - (c-1)), time + 1, 2, r, c - 1, path + "L"]) #left
        if c < cols - 1 and m[r][c+1] != 'X':
            heapq.heappush(fringe, [cost + max(0, int(m[r][c+1]) - int(m[r][c])) + 1 + abs(goal[0] - r) + abs(goal[1] - (c+1)), time + 1, 1, r, c + 1, path + "R"]) #right

    return ans


def astar_euclidean(m, start, goal):
    """
    This function takes two points on the map as the starting point and goal using a* algo to find shortest part with euclidean heuristic
    OUTPUT:
    The path from start to goal as in U D L R
    """
    ans = ""
    #set up the min heap
    fringe = [[0, 0, 0, start[0], start[1], ""]] #cost, time, udlr order, row, col, path
    heapq.heapify(fringe)
    visited = set()

    found = False
    #start poping until the list is empty or reach the goal
    while not found and fringe:
        cost, time, udlr, r, c, path = heapq.heappop(fringe)

        #if out of bounds or obstacle
        if r < 0 or c < 0 or r >= rows or c >= cols or m[r][c] == 'X':
            continue
        
        #if visited already
        if (r,c) in visited:
            continue
        visited.add((r,c))

        #reach goal
        if [r,c] == goal:
            ans = path
            found = True
            continue

        if r >= 1 and m[r-1][c] != 'X':
            heapq.heappush(fringe, [cost + max(0, int(m[r-1][c]) - int(m[r][c])) + 1 + math.sqrt((goal[0] - (r-1))**2 + (goal[1] - c)**2), time + 1, 4, r - 1, c, path + "U"]) #up
        if r < rows - 1 and m[r+1][c] != 'X':
            heapq.heappush(fringe, [cost + max(0, int(m[r+1][c]) - int(m[r][c])) + 1 + math.sqrt((goal[0] - (r+1))**2 + (goal[1] - c)**2), time + 1, 3, r + 1, c, path + "D"]) #down
        if c >= 1 and m[r][c-1] != 'X':
            heapq.heappush(fringe, [cost + max(0, int(m[r][c-1]) - int(m[r][c])) + 1 + math.sqrt((goal[0] - r)**2 + (goal[1] - (c-1))**2), time + 1, 2, r, c - 1, path + "L"]) #left
        if c < cols - 1 and m[r][c+1] != 'X':
            heapq.heappush(fringe, [cost + max(0, int(m[r][c+1]) - int(m[r][c])) + 1 + math.sqrt((goal[0] - r)**2 + (goal[1] - (c+1))**2), time + 1, 1, r, c + 1, path + "R"]) #right

    return ans

###################################################################
p = ""
if algorithm == 'bfs':
    p = bfs(Map, begin, end)
elif algorithm == 'ucs':
    p = ucs(Map, begin, end)
elif algorithm == 'astar' and heuristic == 'euclidean':
    p = astar_euclidean(Map, begin, end)
elif algorithm == 'astar' and heuristic == 'manhattan':
    p = astar_manhattan(Map, begin, end)


if p == "":
    print("null")
else:
    draw_path(Map, begin, p)