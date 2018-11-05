import networkx as nx
import matplotlib.pyplot as plt
from random import randint
import grinpy as gp
import queue

def RandomNNumbers (n, maxn, AlreadExist):
    nums = set (AlreadExist)

    while ( len(nums) < n):
        nums.add(randint(0, int(maxn) - 1))

    return nums

def GetMinimumConnections(VerticesNum):
    Taken = set([0])
    NotTaken = set(x for x in range(1, VerticesNum))
    Edges = set([])

    while len(NotTaken) > 0:
        randNum1 = randint(min(NotTaken), max(NotTaken))
        if randNum1 in NotTaken:
            randNum2 = randint(min(Taken), max(NotTaken))
            if randNum2 in Taken:
                NotTaken.remove(randNum1)
                Taken.add(randNum1)

                if randNum1 > randNum2:
                    temp = randNum1
                    randNum1 = randNum2
                    randNum2 = temp

                Edges.add((randNum1, randNum2))

    return Edges

def RandomNEdges (EdgesNum, VerticesNum, MakeConnected):
    Edges = set ([])
    Edgesindicies = set([])
    
    maxn = (VerticesNum * VerticesNum - VerticesNum) /2

    if EdgesNum > maxn:
        EdgesNum = maxn

    if MakeConnected:        
        Edges = GetMinimumConnections(VerticesNum)

    iterN = 0
    for i in range(0, VerticesNum) :
        for j in range(i + 1, VerticesNum):
            if (i,j) in Edges:
                Edgesindicies.add(iterN)
            iterN = iterN +1


    Edgesindicies = RandomNNumbers(EdgesNum, maxn, Edgesindicies)
    print(len( Edgesindicies ))
    print(Edgesindicies)

    iterN = 0
    for i in range(0, VerticesNum) :
        for j in range(i + 1, VerticesNum):
            if (iterN in Edgesindicies):
                Edges.add(( i ,j))
            iterN = iterN +1

    return Edges

def RandomNGraph (Order, Size, MakeConnected):

    RandGraph = gp.Graph()
    GNodes = list(x for x in range(Order))
    GEdges = RandomNEdges(Size, Order, MakeConnected)
    RandGraph.add_nodes_from(GNodes)
    RandGraph.add_edges_from(GEdges)

    return RandGraph

#def colorGraphRecursive:
    #basecase 1: 


def ColorGraph(G):
    colors = "bgrcmykw"
    colorsrange = range (0, len(colors))

    #G = nx.Graph()
    hey = G.degree(G.nodes())
    #print(hey)
    maxdegree = max ( y for (x,y) in hey)
    #print(maxdegree)
    targetnodes = [(x,y) for (x,y) in hey if y == maxdegree]
    #print(targetnodes)
    #print(len(targetnodes))
    firstnode = min (x for (x,y) in targetnodes if y == maxdegree)
    #print(firstnode)

    print("Given Problem:\t", hey)
    print("Target Solution:\t", maxdegree, "\t", len(targetnodes), "\t", targetnodes)
    print("Start Point: ", firstnode)

    coloredvertices = dict()
    visitedvertices = set()
    added_as_next_vertice = set()
    nextverticies = queue.Queue()
    for x,y in targetnodes:
        nextverticies.put(x)
        added_as_next_vertice.add(x)

    step = 0
    while nextverticies.qsize() >0 :
        step = step + 1
        currentnode = nextverticies.get()
        #print(currentnode)
        
        if ( currentnode not in visitedvertices):
            visitedvertices.add(currentnode)
            neighbours = list (G.neighbors(currentnode))
            
            for neighbour in neighbours:
                if(neighbour not in added_as_next_vertice):
                    nextverticies.put(neighbour)
                    added_as_next_vertice.add(neighbour)

            neighbourscolors = [color for neighbor, color in coloredvertices.items() if neighbor in neighbours]
            #print(">>>>>>>",neighbourscolors)
            currentcolor = min(x for x in colorsrange if x not in neighbourscolors)
            print(step, ">>> \t",currentnode,"\t", currentcolor, "\t", neighbours)

            coloredvertices[currentnode] = currentcolor
    
    gotcolors = ""
    visitedvertices
    for node in G.nodes():
        gotcolors += colors[coloredvertices[node]];

    print((gotcolors))
    print(coloredvertices)
    print(max (x for n,x in coloredvertices.items() ) + 1 )
    return gotcolors
    

def ColorGraph2(G,add_colors = False ,forcing = True, induction = True):
    colors = "rbgcmykw"
    got_colors = ""

    g_nodes = G.nodes()

    colored_nodes = dict()
    for g_node in G.nodes():
        colored_nodes[g_node] = 0

    max_subgraphs = list(nx.find_cliques(G))
    max_subgraphs.sort(key = len, reverse = True)
    max_subgraph_nodes = list(max_subgraphs[0])
    if (add_colors):
        max_degree = max([len(list (G.neighbors(x))) for x in G.nodes() ])
        max_degree_nodes = [x for x in G.nodes() if  len(list (G.neighbors(x))) == max_degree]
        max_subgraph_nodes = [min(max_degree_nodes)]


    global_colors_neighbors = dict()
    global_colors_partites = dict()
    for max_subgraph_node in max_subgraph_nodes:
        global_colors_neighbors[max_subgraph_node] = set (G.neighbors(max_subgraph_node))
        global_colors_partites[max_subgraph_node] = set ([max_subgraph_node])

    
    colored = len(max_subgraph_nodes)
    print("Start colored\t", colored)
    while colored != 0 :
        
        #mirroring colors
        colored = 0
        current_color = 1
        for max_subgraph_node in max_subgraph_nodes:
            print("\t", max_subgraph_node, "\t")
            colored_nodes[max_subgraph_node] =  current_color

            previous_neighbors_count = len (global_colors_neighbors[max_subgraph_node])
            current_neighbors_increase  = previous_neighbors_count

            while current_neighbors_increase > 0:
                possible_color_nodes = set()
                for color_neighbor in global_colors_neighbors[max_subgraph_node]:
                    for possible_color_node in G.neighbors(color_neighbor):
                        if(possible_color_node not in global_colors_neighbors[max_subgraph_node] ):
                            possible_color_nodes.add(possible_color_node)

                for possible_color_node in possible_color_nodes:
                    if(len([x for x in G.neighbors(possible_color_node) if x in possible_color_nodes]) == 0):
                        neighbour_colors = set([colored_nodes[node] for node in G.neighbors(possible_color_node)])
                        if(current_color not in neighbour_colors):
                            if (colored_nodes[possible_color_node] == 0):
                                colored_nodes[possible_color_node] = current_color
                                global_colors_neighbors[max_subgraph_node].add(possible_color_node)
                                for n in G.neighbors(possible_color_node):
                                    global_colors_neighbors[max_subgraph_node].add(n)
                                print("Choosing\t", possible_color_node, "\t", current_color, "\tneighbours:\t", G.neighbors(possible_color_node), "\tColors\t", neighbour_colors)
                                colored = colored + 1
                current_neighbors_increase = previous_neighbors_count - len(global_colors_neighbors[max_subgraph_node])
                previous_neighbors_count = len(global_colors_neighbors[max_subgraph_node])

            #previous algorithm continues coloring over levels even if a node was not sucessfuly colored
            current_color = current_color + 1

        #Writing Forced Colors
        if forcing:
            if colored == 0:
                for g_node in g_nodes:
                    if (colored_nodes[g_node] == 0):
                        neighbours_colors = set()
                        for x, color in colored_nodes.items():
                            if x in G.neighbors(g_node):
                                if(color != 0):
                                    neighbours_colors.add(color)
                        print("Checking Forcing node:\t", g_node, "\t", G.neighbors(g_node) ,"\t", neighbours_colors)
                        if (len(neighbours_colors) == len(max_subgraph_nodes ) - 1):
                            min_colors  = [x for x in range(0, len (max_subgraph_nodes) + 1) if x not in neighbours_colors or x in [0]]
                            colored_nodes[g_node] = max( min_colors)
                            if (colored_nodes[g_node] != 0):
                                for g_node2 in max_subgraph_nodes:
                                    if (colored_nodes[g_node] == colored_nodes[g_node2]):
                                        global_colors_partites[g_node2].add(g_node)
                                        for eachneighbor in G.neighbors(g_node):
                                            global_colors_neighbors[g_node2].add(eachneighbor)
                                colored = colored + 1
                                print("Forced\t", g_node, "\t", colored_nodes[g_node], "\t\tneighbors_colors\t:", neighbours_colors)
                                print(min_colors)

        #adding colors
        if(add_colors):
            if colored == 0:
                new_color_neighbours = set()
                for max_subgraph_node in max_subgraph_nodes:
                    for neighbor in global_colors_partites[max_subgraph_node]:
                        new_color_neighbours.add(neighbor)
                
                possible_new_color_main_nodes = set([x for x in G.neighbors(neighbor) if neighbor in new_color_neighbours])
                
                possible_new_color_main_nodes_disjoint = set()
                for node in possible_new_color_main_nodes:
                    if (len([x for x in G.nodes(node) if node in possible_new_color_main_nodes]) ==0):
                        possible_new_color_main_nodes_disjoint.add(node)
                
                for possible_new_color_main_node in possible_new_color_main_nodes:
                    if (colored_nodes[possible_new_color_main_node] == 0):
                        neighbours_colors = set()
                        for x, color in colored_nodes.items():
                            if x in G.neighbors(possible_new_color_main_node):
                                if(color != 0):
                                    neighbours_colors.add(color)
                        print("Checking new coloring node:\t", possible_new_color_main_node, "\t", G.neighbors(possible_new_color_main_node) ,"\t", neighbours_colors)
                        if (len(neighbours_colors) == len(max_subgraph_nodes)):
                            colored_nodes[possible_new_color_main_node] = current_color
                            max_subgraph_nodes.append(possible_new_color_main_node)
                            global_colors_partites[possible_new_color_main_node] = set([possible_new_color_main_node])
                            global_colors_neighbors[possible_new_color_main_node] = set([x for x in G.neighbors(possible_new_color_main_node)])
                            colored = colored + 1
                            print("error")
                            print("error")
                            print("error")
                            print("New Colored\t", possible_new_color_main_node, "\t", colored_nodes[possible_new_color_main_node], "\t\tneighbors_colors\t:", neighbours_colors)
                            print("error")
                            print("error")
                            print("error")
                            break

                
        

        #inducing colors
        if induction:
            if colored == 0 and len([colored_nodes[x] for x,y in colored_nodes.items() if y != 0]) < len(g_nodes):
                min_distinct_colors = max([ len(set([colored_nodes[neighbour] for neighbour in G.neighbors(g_node) if colored_nodes[neighbour] != 0 ]))   for g_node in g_nodes if colored_nodes[g_node] == 0])
                print("Max Dinstinct Colors \t", min_distinct_colors)
                for g_node in g_nodes:
                    if (len(set([colored_nodes[neighbour] for neighbour in G.neighbors(g_node) if colored_nodes[neighbour] != 0 ])) == min_distinct_colors) :
                        if (colored_nodes[g_node] == 0):
                            neighbours_colors = set()
                            for x, color in colored_nodes.items():
                                if x in G.neighbors(g_node):
                                    if(color != 0):
                                        neighbours_colors.add(color)
                            print("Checking Inducing node:\t", g_node, "\t", G.neighbors(g_node) ,"\t", neighbours_colors)
                            min_colors  = [x for x in range(0, len (max_subgraph_nodes) + 1) if x not in neighbours_colors or x in [0]]
                            colored_nodes[g_node] = max( min_colors)

                            if (colored_nodes[g_node] !=  0):    
                                for g_node2 in max_subgraph_nodes:
                                    if (colored_nodes[g_node] == colored_nodes[g_node2]):
                                        global_colors_partites[g_node2].add(g_node)
                                        for eachneighbor in G.neighbors(g_node):
                                            global_colors_neighbors[g_node2].add(eachneighbor)

                                colored = colored + 1
                                print("Induced\t", g_node, "\t", colored_nodes[g_node], "\t\tneighbors_colors\t:", neighbours_colors)
                                print(min_colors)
                                break


        print("Now colored\t", colored)

    for g_node in G.nodes():
        got_colors += colors[colored_nodes[g_node]] 

    return got_colors


def GetColorGroundTruth(G):
    GotColors = ""

    return GotColors

def __main__ ():
    GOrder = 15
    GSize = 20
    MakeConnectedGraph = True

    G = RandomNGraph(GOrder, GSize, MakeConnectedGraph)
    GColors = "rrrgggbbbm" + "rrrgggbbbm" + "rrrgg"
    print("\t\t\t##########Test One##########")
    GColors2_Forcing = ColorGraph2(G,add_colors= False, forcing= True, induction=False)
    print("\t\t\t##########Test Two##########")
    GColors2_Induction = ColorGraph2(G,add_colors= False, forcing= True, induction=True)
    print("\t\t\t##########Test Three########")
    
    GColors2_addcolors_Forcing = ColorGraph2(G,add_colors= True, forcing= True, induction=False)
    print("\t\t\t##########Test Four#########")
    GColors2_addcolors_Induction = ColorGraph2(G, add_colors= True, forcing= True, induction= True)


    print(G.order())
    print(G.size())
    planarok, otherg = gp.check_planarity(G);
    print(planarok)

    if (not planarok):
        print("Elhamdullah")

    print(gp.chromatic_number(G))

    
    plt.subplot(221)
    nx.draw(G, node_color = GColors2_Forcing, with_labels  = True)
    plt.subplot(222)
    nx.draw(G, node_color = GColors2_Induction, with_labels  = True)
    plt.subplot(223)
    nx.draw(G, node_color = GColors2_addcolors_Forcing, with_labels  = True)
    plt.subplot(224)
    nx.draw(G, node_color = GColors2_addcolors_Induction, with_labels  = True)
    plt.show()


    return 0

__main__()