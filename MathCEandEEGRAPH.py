from copy import copy,deepcopy

###
def createAM_G(): #create adjacency matrix for graph g
    V  = int(input('How many vertices do you want in your graph?: '))
    
    graph = [[0] * V for v in range(V)]

    showAM_G(graph)
    
    return graph
####


def showAM_G(graph):  #show adjacency matrix for graph g
    l = []
    print('   ',end='')
    for i in range(len(graph)):
        l.append(i+1)
        print( l[i], ' ', end='')  #might need to add space here
    print()                        # if i use graph = [ f' {x} ' for x in graph ]
                                   # to fix formating issue with two digit numbers
    count = 1                      #also have to add if statement for two digit  index label
    for row in graph:
        print(count,row)
        count = count + 1

    print()

######
def adjList_G(graph):   #adjacency list of G      The index of each element in list is the vertex (rows),
    adjacencyList = []                            #and the list elements are the vertices its connected to (columns)
    for i in range(len(graph)):    
        temp = []
        for j in range(len(graph)):             #do adjacency lists repeat vertices if it has
            if graph[i][j] == 1:                #multiple vertices connecting them? what about 
                temp.append(j+1)                #edges connecting to the same vertex?
            elif graph[i][j] == 2 and j != i:
                temp.append(j+1)
                temp.append(j+1)
            elif graph[i][j] == 2 and j ==i:
                temp.append(j+1)
        adjacencyList.append(temp)
    return adjacencyList
######

def show_adjList(adjList):
    count = 1
    for ls in adjList:
        print(count, ' ', ls)
        count = count + 1
    print()

def fillAM_G(graph): #fill adjacency matrix G

    adjacencyList = []
    for i in range(len(graph)):
        print('What is vertex ', i+1, 'connected to? (enter vertex number separated by space):')
        temp = input()
        list = temp.split()
        adjacencyList.append(list)
    print()
    
    ''' #this code was used to see what was happening
    count = 1
    for ls in adjacencyList:
        print(count, ' ', ls)
        count = count + 1
    print()
    '''
    
    for ls in adjacencyList:     #turns elements into integers
        for i in range(len(ls)):
            ls[i] = int(ls[i])


    for i in range(len(graph)):
        for j in range(len(graph)):
            for x in range(len(adjacencyList[i])):
                if adjacencyList[i][x] == j+1:
                    if i+1 == j+1:
                        graph[i][j] = graph[i][j] + 2
                    else:
                        graph[i][j] = graph[i][j] + 1

####
def vertex_degreeAM(vertex, graph):
    degree = 0
    for i in range(len(graph)):
        degree = degree + graph[vertex-1][i]
    return degree

def add_2DMatrix(A, B):
    C = []
    for i in range(len(A)):
        row = []
        for j in range(len(A[0])):
            row.append(A[i][j] + B[i][j])
        C.append(row)
    return C

def mult_2DMatrix(A,B):
    C = []
    for i in range(len(A)):
        row = []
        for j in range(len(A[0])):
            temp = 0
            for x in range(len(A[i])):
                temp = temp + (A[i][x] * B[x][j])
            row.append(temp)
        C.append(row)
    return C

def connectivity_matrixAM(graph):
    connMatrix = [[0 for i in range(len(graph))] for j in range(len(graph))] 

    A = [[0 for i in range(len(graph))] for j in range(len(graph))] 

    for x in range(len(graph)):
        for y in range(len(graph)):  #creates identity matrix
            if x == y:
                A[x][y] = 1

    for i in range(len(graph)-1):
        for j in range(i):
            A = mult_2DMatrix(A, graph)
            connMatrix = add_2DMatrix(connMatrix, A)
    return connMatrix

def min_degreeAM(graph):
    degree = 500*len(graph) #number much greater than a probable degree of a vertex
    for i in range(len(graph)):
        if degree > vertex_degreeAM(i+1,graph):
            degree = vertex_degreeAM(i+1,graph)
    return degree

def max_degreeAM(graph):
    degree = 0
    for i in range(len(graph)):
        if degree < vertex_degreeAM(i+1,graph):
            degree = vertex_degreeAM(i+1,graph)
    return degree

def is_G_simpleAM(graph):   
    for i in range(len(graph)):
        for j in range(len(graph)):
            if graph[i][j] > 1: #if any element is greater than 1,
                return False    #then its either a loop or repeated edge
    
    return True

def is_G_completeAM(graph):
    simple = is_G_simpleAM(graph)
    connected = True
    for i in range(len(graph)):
        for j in range(len(graph)):
            if i!=j and graph[i][j] == 0:
                connected = False 
    if  connected and simple:
        return True, len(graph)
    else: 
        return False

def is_G_connectedAM(graph): #using connectivity matrix

    cmatrix = connectivity_matrixAM(graph)

    for i in range(len(graph)):
        for j in range(len(graph)):
            if i!=j and cmatrix[i][j] < 1:
                return False
    return True
####

def traversal(matrix, r, c): #marks very element in component 
    matrix[r][c] = 0
    if (r-1 >= 0) and (matrix[r-1][c] != 0): #up 
        traversal(matrix, r-1, c) 
    if (r+1 < len(matrix)) and (matrix[r+1][c] != 0): #down
        traversal(matrix, r+1, c) 
    if (c-1 >= 0) and (matrix[r][c-1] != 0): #left 
        traversal(matrix, r, c-1) 
    if (c+1 < len(matrix)) and (matrix[r][c+1] != 0): #right
        traversal(matrix, r, c+1)

###
def num_of_components(graph): # does not work if you have a lone vertex

    Bg = connectivity_matrixAM(graph)
    loneVertex = False
    count = 0
    for i in range(len(graph)):
        for j in range(len(graph)):
            if i == j and Bg[i][j] != 0:        # for the C3, it shows 2 components, and the diagonal connmatrix is 0s
                traversal(Bg, i, j)
                count = count + 1
            if Bg[i][j] == 0 and Bg[j][i] == 0: #next 4 lines of code check if we have a lone vertex
                loneVertex = True
            
        if loneVertex == True:
            count = count + 1
        loneVertex = False
    

    if count == 0: count = 1
    return count

def is_G_regularAM(graph):
    regular = True
    degree = vertex_degreeAM(1,graph)
    for i in range(len(graph)):
        if vertex_degreeAM(i+1, graph) != degree:
            regular = False
            return regular

    return regular, degree

def edge_subraction(graph, x,y):
    if graph[x][y] == 0 :
        print(x,y,'no edge connecting given vertices')
    elif x == y:
        graph[x][y] = graph[x][y] - 2
    else:
        graph[x][y] = graph[x][y] - 1
        graph[y][x] = graph[y][x] - 1
    
def bridges(graph): # not working
    A = deepcopy(graph)
    n = num_of_components(graph)
    count = 0
    for i in range(len(graph)):
        for j in range(len(graph)):
            edge_subraction(A, i,j)
            showAM_G(connectivity_matrixAM(A))
            print(num_of_components(A))
            if num_of_components(A) > n:
                count = count + 1
            A = deepcopy(graph)
            showAM_G(connectivity_matrixAM(A))
            print(num_of_components(A))
    if count == 0:
        return count, 'Strongly linked'
    if count >= 1:
        return count, 'Weakly linked'
###

'''
***TODO***
-fix briges 
-fix numofcomponents
'''


#def is_G_eularianAM(graph):

#def is_G_hamiltonianAM(graph):

    

graph = createAM_G()
fillAM_G(graph)
print("Adjacency Matrix of graph G:")
showAM_G(graph)
print("Adjacency List:")
show_adjList(adjList_G(graph))
print("Connectivity Matrix:")
showAM_G(connectivity_matrixAM(graph))
print('G is simple: ', is_G_simpleAM(graph))
print('G is regular: ', is_G_regularAM(graph))
print('G is complete: ',is_G_completeAM(graph))
print("G is connected: ",is_G_connectedAM(graph))
print("Number of Components: ", num_of_components(graph))
print(bridges(graph))


# # more topics
    #is null
    #is cylce
    #path graph
    #is bipartite
    #induced subgraph
    #vertex subtraction
    #edge indeced subgraph
    #graph union
    # - walks,trials, paths,
    # - shortest path algorithm
    # - edge connectivity
    # - vertex connectivity
    # - propterty of connectivity (pg 117)
    #diracs theorm
    #ores theorem
    #bipartite graphs
    #laplacian matrix