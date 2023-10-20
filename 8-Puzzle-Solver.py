from queue import PriorityQueue
import math
import copy
import time

class Node:
  def __init__(self, board):
    self.board = board
    self.neighbors = []
  def generate_neighbors(self):
    if self.board[0][0] == " ":
      location_open_space = [0, 0]
    elif self.board[0][1] == " ":
      location_open_space = [0, 1]
    elif self.board[0][2] == " ":
      location_open_space = [0, 2]
    elif self.board[1][0] == " ":
      location_open_space = [1, 0]
    elif self.board[1][1] == " ":
      location_open_space = [1, 1]
    elif self.board[1][2] == " ":
      location_open_space = [1, 2]
    elif self.board[2][0] == " ":
      location_open_space = [2, 0]
    elif self.board[2][1] == " ":
      location_open_space = [2, 1]
    elif self.board[2][2] == " ":
      location_open_space = [2, 2]
    
    directions = [(-1, 0), (1, 0), (0, 1), (0, -1)]
    
    for move in directions:
      potential_new_row = location_open_space[0] + move[0]
      potential_new_column = location_open_space[1] + move[1]
      if potential_new_column <= 2 and potential_new_column >= 0 and potential_new_row <= 2 and potential_new_row >= 0:
        temp_board = copy.deepcopy(self.board)
        
        temp_board[location_open_space[0]][location_open_space[1]] = temp_board[potential_new_row][potential_new_column]
        temp_board[potential_new_row][potential_new_column] = " "
        
        new_node = Node(temp_board)
        self.neighbors.append(new_node)
    
    
  def __str__(self):
    return f"{self.board[0][0]} {self.board[0][1]} {self.board[0][2]}\n{self.board[1][0]} {self.board[1][1]} {self.board[1][2]}\n{self.board[2][0]} {self.board[2][1]} {self.board[2][2]}"
  def __lt__(self, other):
    return self.board < other.board
  def __eq__(self, other):
    return self.board == other.board and self.__class__ == other.__class__
  def is_solved(self):
    return self.board == [["1","2","3"], ["4","5","6"], ["7","8"," "]]
    
  def get_heuristic(self):
    if self.is_solved():
      return 0
    
    x = 0
    for row in range(len(self.board)):
      for column in range(len(self.board[row])):
        if self.board[row][column] == "8":
          #print(abs(column - 1) + abs(row - 2))
          x += (abs(column - 1) + abs(row - 2))
        
        elif self.board[row][column] == "7":
          #print(abs(column - 0) + abs(row - 2))
          x += (abs(column - 0) + abs(row - 2))
        
        elif self.board[row][column] == "6":
          #print(abs(column - 2) + abs(row - 1))
          x += (abs(column - 2) + abs(row - 1))
        
        elif self.board[row][column] == "5":
          #print(abs(column - 1) + abs(row - 1))
          x += (abs(column - 1) + abs(row - 1))
        
        elif self.board[row][column] == "4":
          #print(abs(column - 0) + abs(row - 1))
          x += (abs(column - 0) + abs(row - 1))
        
        elif self.board[row][column] == "3":
          #print(abs(column - 2) + abs(row - 0))
          x += (abs(column - 2) + abs(row - 0))
        
        elif self.board[row][column] == "2":
          #print(abs(column - 1) + abs(row - 0))
          x += (abs(column - 1) + abs(row - 0))
        
        elif self.board[row][column] == "1":
          #print((abs(column - 0) + abs(row - 0)))
          x += (abs(column - 0) + abs(row - 0))
        
    
    if x == 0:
      return 1
    else:
      return x 

class Graph:
  def __init__(self, start):
    self.root = start
    self.visited = []
    
  def add_node(self, node):
    self.graph[node.key] = node
  
  def add_edge(self, node1, node2, weight):
    if node1.key in self.graph:
      if node2.key in self.graph:
        node1.add_neighbor(node2, weight)
        node2.add_neighbor(node1, weight)
      else:
        print("Node 1 is in graph, but Node 2 is not")
    else:
      print(node1.key)
      print("node1 not in graph")
  def delete_edge(self, node1, node2):
    if node2 in node1.neighbors:
      if node1 in node2.neighbors:
        node1.remove_neighbor(node2)
        node2.remove_neighbor(node1)
      else:
        print("Node1 is not a neigbor to Node2")
    else: 
      print("Node2 is not a neighbor to Node1")
  def delete_node(self, node):
    if node.key in self.graph:
      del self.graph[node.key]
    for i in self.graph.values():
      if node in i.neighbors:
        i.neighbors.remove(node)
  def __str__(self):
    temp = ""
    for value in self.graph.values():
      temp += str(value) + "\n"
    return(temp)
  
  def bfs(self):
    visited = [self.root]
    queue = [(self.root, [self.root])]
    count = 0
    
    while len(queue) > 0:
      node, path = queue.pop(0)
      count += 1
      if node.is_solved() == True:
        return path, count
      
      node.generate_neighbors()
      
      for neighbor in node.neighbors:
        if neighbor not in visited:
          queue.append((neighbor, path + [neighbor]))
          visited.append(neighbor)

  def greedy_search(self):
    visited = []
    to_visit = PriorityQueue()
    to_visit.put((0, self.root, [self.root]))
    count = 0
    while to_visit.empty() == False:
      
      cost, current_node, path = to_visit.get()
      
      if current_node not in visited:
        count += 1
        visited.append(current_node)
      
        if current_node.is_solved():
          return path, count, visited
        
        current_node.generate_neighbors()
        
        for child in current_node.neighbors:
          #if child not in visited:
          to_visit.put((child.get_heuristic(), child, path + [child]))
        
    return "Error"
    
  def a_star_search(self):
    queue = PriorityQueue()
    g = 0
    count = 0
    queue.put((self.root.get_heuristic() + g, g, self.root, [self.root]))
    #(heuristic, g, node, path)
    visited = []
    
    while queue.empty() == False:
      heuristic, depth, node, path = queue.get()
      if node not in visited:
        
        count += 1
        visited.append(node)
        
        if node.is_solved() == True:
          return path, count, visited
        
        node.generate_neighbors()
        
        for neighbor in node.neighbors:
          
          if neighbor not in visited:
            g = depth + 1
            h = neighbor.get_heuristic()
            queue.put(((h + g, g, neighbor, path + [neighbor])))
      
    return "Error"


test = Node([["3","6","8"], ["1"," ","4"], ["7", "2", "5"]])
#print(test)

#print("\nNeighbors:")
#test.generate_neighbors()
#for i in test.neighbors:
#  print(i)
#  print()

#print("Heuristic:")
#print(test.get_heuristic())

testing = Graph(test)

print("\nBFS:")
start = time.time()
path, count = testing.bfs()
end = time.time()
for node in path:
  print(node)
  print()
print(count)
print(len(path))
print("Time {}".format(str(end - start)))

start = time.time()
path, count, visited = testing.a_star_search()
end = time.time()

for node in path:
  print(node)
  print()
print(count)
print(len(path))
print("Time {}".format(str(end - start)))
