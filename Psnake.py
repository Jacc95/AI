
import math
import time
import random
import pygame
import numpy
import tkinter as tk
from tkinter import messagebox
 
class cube(object):
    rows = 20
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

def BFS(goal, start, rows, last): #BEST FIRST SEARCH
    newRoad=[]
    direction=[0,0,0,0]
    move=0
    lastMove=last
    r=rows
    x=start[0]
    y=start[1]
    a=goal[0]
    b=goal[1]

    while True:
        direction[0]=x-a
        direction[1]=a-x
        direction[2]=y-b
        direction[3]=b-y

        #print("distancias: ", direction)

        for i in range(len(direction)):
            if direction[i]<=0: #If it is equal, it means that the point reach the coordinates 
                direction[i]+=r #Keeping the numbers positive
            if direction[i]==0:
                direction[i]=r

        if direction[0]==direction[1] and direction[2]==direction[3] and direction[0]==direction[3]:
            break

        move=direction.index(min(direction))

        #print(move, " ", lastMove)
        if (move+lastMove)==1:
            #print("HORIZONTAL")
            if direction[0]==0 and direction[1]==0:
                move=lastMove
            else:
                direction[0]=r
                direction[1]=r
                move=direction.index(min(direction[2], direction[3]))
        elif (move+lastMove)==5:
            #print("VERTICAL")
            move=direction.index(min(direction[0], direction[1]))

        lastMove=move

        newRoad.append(move)

        #Update coordinates
        if move==0: #LEFT
            x-=1
        if move==1: #RIGHT
            x+=1
        if move==2: #UP
            y-=1
        if move==3: #DOWN
            y+=1

    return newRoad
 
def main():
    global width, rows, s, snack
    width = 500
    rows = 20
    spawn=(rows//2,rows//2)
    win = pygame.display.set_mode((width, width))
    s = snake((255,0,0), spawn)
    apple=randomSnack(rows, s) #DEFINED TO GET DE COORDINATES OF THE APPLE
    snack = cube(apple, color=(0,255,0))
    flag = True

    lastMove=9
    newMove=0

    road=BFS(apple, spawn, rows, lastMove)
    #print(road)
    #print(len(road))

    clock = pygame.time.Clock()
    
    while flag:
        pygame.event.pump()
        pygame.time.delay(50)
        clock.tick(10)
        newMove=road.pop(0)
        s.move(newMove,lastMove)

        #s.move(1,0)
        lastMove=newMove
        #print(road)
        if s.body[0].pos == snack.pos:
            s.addCube()
            apple = randomSnack(rows, s)
            snack = cube(apple, color=(0,255,0))
            road=BFS(apple, s.getHeadPos(), rows, lastMove)
            #print(road)

        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z:z.pos,s.body[x+1:])):
                print('Score: ', len(s.body))
                message_box('You Lost!', 'Play again...')
                s.reset(spawn)
                road=BFS(apple, s.getHeadPos(), rows, lastMove)
                pygame.time.delay(100)
                break
 
           
        redrawWindow(win)
 
       
    pass
 
 
 
main()