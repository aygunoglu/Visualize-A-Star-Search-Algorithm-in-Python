import pygame
import sys
from collections import deque
from tkinter import messagebox, Tk
import math

size = (width, height) = (800,600)

rows = 30
cols = 40

rectHeight = width//cols
rectWidth = height//rows

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
PURPLE = (102, 0, 102)
YELLOW = (255,255,0)

pygame.init()

wn = pygame.display.set_mode(size)
pygame.display.set_caption("Shortest Path w/ A-Star")

class Node:
    
    def __init__(self, row, col, rectHeight, rectWidth):
        self.row = row
        self.col = col
        #self.f, self.g, self.f = 0,0,0
        self.rectHeight = rectHeight
        self.rectWidth = rectWidth
        self.color = WHITE
        self.prev = []
        self.neighbors = []

    def get_pos(self):
        return self.row, self.col


    def is_visited(self):
        return self.color == GREEN

    def is_obstacle(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == YELLOW

    def is_end(self):
        return self.color == PURPLE

    def make_visited(self):
        self.color = GREEN

    def make_obstacle(self):
        self.color = BLACK

    def make_start(self):
        self.color = RED

    def make_end(self):
        self.color = PURPLE                
    
    def make_queue(self):
        self.color = YELLOW

    def make_path(self):
        self.color = BLUE    

    def draw(self):
        pygame.draw.rect(wn, self.color, (self.row*rectHeight,self.col*rectWidth,self.rectHeight-1,self.rectWidth-1))   

    def add_neighbors(self, grid):
        if self.row > 0 and not grid[self.row-1][self.col].is_obstacle(): # UP
            self.neighbors.append(grid[self.row-1][self.col])

        if self.row < 39 and not grid[self.row+1][self.col].is_obstacle(): # DOWN            
            self.neighbors.append(grid[self.row+1][self.col])

        if self.col < 29 and not grid[self.row][self.col+1].is_obstacle(): # RIGHT            
            self.neighbors.append(grid[self.row][self.col+1])

        if self.col > 0 and not grid[self.row][self.col-1].is_obstacle(): # LEFT          
            self.neighbors.append(grid[self.row][self.col-1])

        if self.row > 0 and self.col > 0 and not grid[self.row-1][self.col-1].is_obstacle(): # UP
            self.neighbors.append(grid[self.row-1][self.col-1])

        if self.row < 39 and self.col < 29 and not grid[self.row+1][self.col+1].is_obstacle(): # DOWN            
            self.neighbors.append(grid[self.row+1][self.col+1])

        if self.col < 29 and self.row > 0 and not grid[self.row-1][self.col+1].is_obstacle(): # RIGHT            
            self.neighbors.append(grid[self.row-1][self.col+1])

        if self.col > 0 and self.row < 39 and not grid[self.row+1][self.col-1].is_obstacle(): # LEFT          
            self.neighbors.append(grid[self.row+1][self.col-1]) 

def make_grid(rows):
    for i in range(cols):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, 20, 20)
            grid[i].append(node)
    return grid        

def draw(startNode, endNode, grid, rows):
    for row in grid:
        for node in row:
            if node is not startNode and node != endNode and node.color != BLUE and node.color != BLACK and node in queue:
                node.make_queue()
                node.draw()
            elif node is not startNode and node != endNode and node.color != BLUE and node.color != BLACK and node in visited:
                node.make_visited()
                node.draw()
            else:
                node.draw()        
    
    pygame.display.update()

def BFS(startNode, endNode):
    
    queue.append(startNode)
    visited.add(startNode)

    g_score = {node: float("inf") for row in grid for node in row}
    g_score[startNode] = 0
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[startNode] = heuristics(startNode, endNode)


    searchFlag = True
    startFlag = True
    while startFlag and queue:




        current = min(f_score,key=f_score.get)

        queue.remove(current)
        del f_score[current]

        if current == endNode:
            back_tracking(current, startNode, endNode)
            Tk().wm_withdraw()
            messagebox.showinfo("Found it","Found it!")
            searchFlag = False 


        if searchFlag:

            for neighbor in current.neighbors:
                if (abs(neighbor.row-current.row) + abs(neighbor.col-current.col)) == 1:
                    tempG = g_score[current] + 1 
                if (abs(neighbor.row-current.row) + abs(neighbor.col-current.col)) == 2:
                    tempG = g_score[current] + 1.414  
                
                if tempG < g_score[neighbor]:
                    if neighbor not in visited:
                        g_score[neighbor] = tempG
                        f_score[neighbor] = tempG + heuristics(neighbor, endNode)   
                        visited.add(neighbor)
                        queue.append(neighbor)
                        neighbor.prev.append(current) 
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        draw(startNode, endNode, grid, rows)

def back_tracking(current, startNode, endNode):
    while current != startNode:       
        current = current.prev[0]
        if current != startNode:
            current.make_path()
        draw(startNode, endNode, grid, rows)
        pygame.time.delay(40)    
       
def click_pos(pos):
    a,b = pos
    a = a//rectHeight
    b = b//rectWidth
    return a,b  

def heuristics(a, b):
    return math.sqrt((a.row - b.row)**2 + abs(a.col - b.col)**2)          
    


grid = []
queue = deque()
visited = set()

make_grid(rows)

startNode = None
endNode = None

def main(startNode, endNode):

    still_going = True
    
    while still_going:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                still_going = False
            
            if pygame.mouse.get_pressed()[0]: 
                pos = pygame.mouse.get_pos()
                a,b = click_pos(pos)
                startNode = grid[a][b]
                startNode.make_start()
            elif pygame.mouse.get_pressed()[2]: 
                pos = pygame.mouse.get_pos()
                a,b = click_pos(pos)
                endNode = grid[a][b]
                endNode.make_end()
            elif pygame.mouse.get_pressed()[1]: 
                pos = pygame.mouse.get_pos()
                a,b = click_pos(pos)
                obstacle = grid[a][b]
                obstacle.make_obstacle()               


            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and startNode and endNode:
                    for row in grid:
                        for node in row:
                            node.add_neighbors(grid)
                    BFS(startNode, endNode)    
        draw(startNode, endNode, grid, rows)    

main(startNode, endNode)    