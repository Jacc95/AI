# AI
Snake game controlled by search agents

Best-First Search code (Omar)

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
