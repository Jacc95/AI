
import math
import time
import random
import pygame
import numpy
import tkinter as tk
from tkinter import messagebox
 
class cube(object):
    rows = 10
    w = 500
    def __init__(self,start,dirnx=1,dirny=0,color=(255,0,0)):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color
 
       
    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny

        if self.dirnx == -1 and self.pos[0] <= 0: self.pos = (rows-1, self.pos[1])
        elif self.dirnx == 1 and self.pos[0] >= rows-1: self.pos = (0, self.pos[1])
        elif self.dirny == 1 and self.pos[1] >= rows-1: self.pos = (self.pos[0], 0)
        elif self.dirny == -1 and self.pos[1] <= 0: self.pos = (self.pos[0], rows-1)
        else: self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)
 
    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]
 
        pygame.draw.rect(surface, self.color, (i*dis+1,j*dis+1, dis-2, dis-2))
        if eyes:
            centre = dis//2
            radius = 3
            circleMiddle = (i*dis+centre-radius,j*dis+8)
            circleMiddle2 = (i*dis + dis -radius*2, j*dis+8)
            pygame.draw.circle(surface, (0,0,0), circleMiddle, radius)
            pygame.draw.circle(surface, (0,0,0), circleMiddle2, radius)
 
class snake(object):
    body = []
    turns = {}
    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1
 
    def move(self, new, last): 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        if new!=last:
            if new==0:
                self.dirnx = -1
                self.dirny = 0
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

            elif new==1:
                self.dirnx = 1
                self.dirny = 0
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

            elif new==2:
                self.dirnx = 0
                self.dirny = -1
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

            elif new==3:
                self.dirnx = 0
                self.dirny = 1
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        for i, c in enumerate(self.body):        
            p = c.pos[:]
            if p in self.turns: #CHANGE DIRECTION
                #print("este es el IF")
                turn = self.turns[p]
                c.move(turn[0],turn[1])
                if i == len(self.body)-1:
                    self.turns.pop(p)
            else: #CONTINUE IN THE SAME PATH
                #print("este es el ELSE")
                c.move(c.dirnx,c.dirny)
        #print(self.head.pos)
 
    def reset(self, pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1
 
 
    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny
 
        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0]-1,tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0]+1,tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0],tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0],tail.pos[1]+1)))
 
        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy
       
 
    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i ==0:
                c.draw(surface, True)
            else:
                c.draw(surface)

    def getHeadPos(self):
        return self.head.pos
 
 
def drawGrid(w, rows, surface):
    sizeBtwn = w // rows
 
    x = 0
    y = 0
    for l in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn
 
        pygame.draw.line(surface, (255,255,255), (x,0),(x,w))
        pygame.draw.line(surface, (255,255,255), (0,y),(w,y))
       
 
def redrawWindow(surface):
    global rows, width, s, snack
    surface.fill((0,0,0))
    s.draw(surface)
    snack.draw(surface)
    drawGrid(width,rows, surface)
    pygame.display.update()
 
 
def randomSnack(rows, item):
 
    positions = item.body
 
    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:
            continue
        else:
            break
       
    return (x,y)
 
 
def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass

def AS(goal, start, rows, last): #BEST FIRST SEARCH
    #start = (x,y) where the head starts
    #goal  = (x,y) where the apple is
    newRoad = []    #Path to be followed
    queue   = []    #Nodes to be expanded
    visited = []    #Visited nodes

    exp = [] #expanded nodes 

    visited.append(start)
    queue.append(start)

    while True:
        #Initializes flags that registers if a node has already been visited
        flag = [False, False, False, False]

        #Generates the children based on the expanded node
        exp[0] = [queue[0][0], queue[0][1]+1, queue[0]] #Up node
        exp[1] = [queue[0][0], queue[0][1]-1, queue[0]] #Down node
        exp[2] = [queue[0][0]-1, queue[0][1], queue[0]] #Left node
        exp[3] = [queue[0][0]+1, queue[0][1], queue[0]] #Right node

        #Checks if one of the surrounding nodes is goal node, then Kills the While True
        for i in range(len(exp)):
            if (exp[i][0],exp[i][1]) == goal:
                newRoad = [exp[i]]
                #while :
                    
                #newRoad = [,exp[i]]
                break 
        
        #Validates if the children node was already visited
        for i in range(len(exp)):
            for j in range(len(visited)):
                if (exp[i][0],exp[i][1]) == (visited[j][0],visited[j][1]):
                    flag[i] = True
        
        #Depending on the node if it is repeated or not, add it to visited list
        for i in range(len(flag)):
            if flag[i] == False:
                visited.append(exp[i])
                queue.append(exp[i])

        #Updates queue, eliminates the already expanded node from the queue
        queue.pop(0)

        #Parent thing


        #lastMove=move
        #newRoad.append(move)

        #if visited node == goal
            #break
        # #Update coordinates
        # if move==0: #LEFT
        #     x-=1
        # if move==1: #RIGHT
        #     x+=1
        # if move==2: #UP
        #     y-=1
        # if move==3: #DOWN
        #     y+=1 

    return newRoad
 
def main():
    global width, rows, s, snack
    width = 500
    rows = 10
    spawn=(rows//2,rows//2)
    win = pygame.display.set_mode((width, width))
    s = snake((255,0,0), spawn)
    apple=randomSnack(rows, s) #DEFINED TO GET DE COORDINATES OF THE APPLE
    snack = cube(apple, color=(0,255,0))
    flag = True

    lastMove=9
    newMove=0

    road=AS(apple, spawn, rows, lastMove)
    #print(road)
    #print(len(road))

    clock = pygame.time.Clock()
    
    while flag:
        pygame.event.pump()
        pygame.time.delay(50)
        clock.tick(10)
        newMove=road.pop(0)
        s.move(newMove,lastMove)

        lastMove=newMove
        #print(road)
        if s.body[0].pos == snack.pos:
            s.addCube()
            apple = randomSnack(rows, s)
            snack = cube(apple, color=(0,255,0))
            road=AS(apple, s.getHeadPos(), rows, lastMove)
            #print(road)

        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z:z.pos,s.body[x+1:])):
                print('Score: ', len(s.body))
                message_box('You Lost!', 'Play again...')
                s.reset(spawn)
                road=AS(apple, s.getHeadPos(), rows, lastMove)
                pygame.time.delay(100)
                break
 
           
        redrawWindow(win)
 
       
    pass
 
 
 
main()