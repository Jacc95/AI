# AI
Snake game controlled by search agents
Breadth First Search (Juan Alfonso Chan)

def AS(goal, start, rows, last): #BEST FIRST SEARCH
    #start = (x,y) where the head starts
    #goal  = (x,y) where the apple is
    newRoad  = []      #Origin to goal with parent and children relationship
    queue    = []      #Nodes to be expanded
    visited  = []      #Visited nodes
    path     = []      #Path to be followed
    sequence = []      #Sequence of moves
    exp = [0, 0, 0, 0] #Expanded nodes 
    moveh = 0          #Initializes horizontal move variable for the sequence
    movev = 0          #Initializes vertital move variable for the sequence

    visited.append(start)   
    queue.append(start)

    while True:
        #Initializes flags that registers if a node has already been visited
        flag = [False, False, False, False]

        #Generates the children based on the expanded node. North, South, West and East
        exp[0] = [queue[0][0], queue[0][1]+1, queue[0][0], queue[0][1]] #Up node
        exp[1] = [queue[0][0], queue[0][1]-1, queue[0][0], queue[0][1]] #Down node
        exp[2] = [queue[0][0]-1, queue[0][1], queue[0][0], queue[0][1]] #Left node
        exp[3] = [queue[0][0]+1, queue[0][1], queue[0][0], queue[0][1]] #Right node

        #Generates newRoad when the expanded node is goal node.
        for i in range(len(exp)):
            if (exp[i][0],exp[i][1]) == goal:
                newRoad.append(exp[i])                                                      #Adds goal node to the path
                while (newRoad[0][2], newRoad[0][3]) != start:                              #Loop that generates path and stops if it has been fully generated
                    for j in range(len(visited)):              
                        if [newRoad[0][2], newRoad[0][3]] == [visited[j][0],visited[j][1]]: #Add parent of the analyzed node to the path
                            newRoad.insert(0, visited[j])
                break

        #Generates the path sequence and stops the While True
        if len(newRoad) != 0:
            path.append(start)
            for i in range(len(newRoad)):
                path.append((newRoad[i][0],newRoad[i][1]))  #Adds the path steps in tuples
            for j in range(len(path)-1):
                #Updates the moves based on difference between points
                moveh = path[j+1][0] - path[j][0]
                movev = path[j+1][1] - path[j][1]

                #Adds next move to sequence based on vertical diff
                if movev == 1: 
                    sequence.append(0)
                elif movev == -1:
                    sequence.append(1)
                #Adds next move to sequence based on horizontal diff
                if moveh == 1: 
                    sequence.append(3)
                elif moveh == -1:
                    sequence.append(2)

                #Reinitializes move variables
                moveh = 0
                movev = 0

            print(sequence)
            break

        #Validates if the children node was already visited
        for i in range(len(exp)):
            for j in range(len(visited)):
                if (exp[i][0], exp[i][1]) == (visited[j][0], visited[j][1]):
                    flag[i] = True
        
        #Depending on the node if it is repeated or not, add it to visited list
        for i in range(len(flag)):
            if flag[i] == False:
                visited.append(exp[i])
                queue.append(exp[i])

        #Updates queue, eliminates the already expanded node from the queue
        queue.pop(0)
            
        #lastMove=move
        #newRoad.append(move)

    return sequence
