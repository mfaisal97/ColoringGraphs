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
    

def ColorGraph2(G,add_colors = False ,forcing = True, induction = True, max_first = True):
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
        max_degree = 0
        
        if (max_first):
            max_degree = max([len(list (G.neighbors(x))) for x in G.nodes() ])
        else :
            max_degree = min([len(list (G.neighbors(x))) for x in G.nodes() ])

        max_degree_nodes = [x for x in G.nodes() if  len(list (G.neighbors(x))) == max_degree]
        max_subgraph_nodes = [min(max_degree_nodes)]


    global_colors_neighbors = dict()
    global_colors_partites = dict()
    for max_subgraph_node in max_subgraph_nodes:
        global_colors_neighbors[max_subgraph_node] = set (G.neighbors(max_subgraph_node))
        global_colors_partites[max_subgraph_node] = set ([max_subgraph_node])

    
    colored = len(max_subgraph_nodes)
    print("Start colored\t", colored)
    while colored != 0:
        
        #mirroring colors
        colored = 0
        current_color = 1
        for max_subgraph_node in max_subgraph_nodes:
            print("\t", max_subgraph_node, "\t")
            colored_nodes[max_subgraph_node] =  current_color

            previous_neighbors_count = len (global_colors_neighbors[max_subgraph_node])
            current_neighbors_increase  = previous_neighbors_count

            firsttime = True
            while current_neighbors_increase > 0 and (firsttime or current_color == 1 ):
                firsttime = False

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
                            if x in list (G.neighbors(g_node)):
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
                            min_colors  = [x for x in range(0, len (max_subgraph_nodes) + 1) if (x not in neighbours_colors) or (x in [0])]
                            colored_nodes[g_node] = max(min_colors)

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


        #adding colors
        if(add_colors):
            if colored == 0 and current_color < 2:
                new_color_neighbours = set()
                for max_subgraph_node in max_subgraph_nodes:
                    for neighbor in global_colors_partites[max_subgraph_node]:
                        new_color_neighbours.add(neighbor)
                
                possible_new_color_main_nodes = set([x for x in G.neighbors(neighbor) if neighbor in new_color_neighbours])
                
                possible_new_color_main_nodes_disjoint = set()
                for node in possible_new_color_main_nodes:
                    if (len([x for x in G.neighbors(node) if node in possible_new_color_main_nodes]) ==0):
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
                            global_colors_neighbors[possible_new_color_main_node] = set(G.neighbors(possible_new_color_main_node))
                            colored = colored + 1
                            print("error")
                            print("error")
                            print("error")
                            print("New Colored\t", possible_new_color_main_node, "\t", colored_nodes[possible_new_color_main_node], "\t\tneighbors_colors\t:", neighbours_colors)
                            print("error")
                            print("error")
                            print("error")

                            previous_neighbors_count = len (global_colors_neighbors[possible_new_color_main_node])
                            current_neighbors_increase  = previous_neighbors_count

                            firsttime = True
                            while current_neighbors_increase > 0 & firsttime:
                                firsttime = False

                                possible_color_nodes = set()
                                for color_neighbor in global_colors_neighbors[possible_new_color_main_node]:
                                    for possible_color_node in G.neighbors(color_neighbor):
                                        if(possible_color_node not in global_colors_neighbors[possible_new_color_main_node] ):
                                            possible_color_nodes.add(possible_color_node)

                                for possible_color_node in possible_color_nodes:
                                    if(len([x for x in G.neighbors(possible_color_node) if x in possible_color_nodes]) == 0):
                                        neighbour_colors = set([colored_nodes[node] for node in G.neighbors(possible_color_node)])
                                        if(current_color not in neighbour_colors):
                                            if (colored_nodes[possible_color_node] == 0):
                                                colored_nodes[possible_color_node] = current_color
                                                global_colors_neighbors[possible_new_color_main_node].add(possible_color_node)
                                                for n in G.neighbors(possible_color_node):
                                                    global_colors_neighbors[possible_new_color_main_node].add(n)
                                                print("Choosing\t", possible_color_node, "\t", current_color, "\tneighbours:\t", G.neighbors(possible_color_node), "\tColors\t", neighbour_colors)
                                                colored = colored + 1
                                current_neighbors_increase = previous_neighbors_count - len(global_colors_neighbors[possible_new_color_main_node])
                                previous_neighbors_count = len(global_colors_neighbors[possible_new_color_main_node])


                            break

            if forcing:
                for g_node in g_nodes:
                    if (colored_nodes[g_node] == 0):
                        neighbours_colors = set()
                        for x, color in colored_nodes.items():
                            if x in list (G.neighbors(g_node)):
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

        print("Now colored\t", colored)

    for g_node in G.nodes():
        got_colors += colors[colored_nodes[g_node]] 

    return got_colors, len(max_subgraph_nodes), colored_nodes


def ColorGraph3(G,mirror = True, add_colors = False ,forcing = True, induction = True, max_first = True):
    colors = "rbgcmykw"
    got_colors = ""

    hamoone, hamotwo, colored_nodes = ColorGraph2(G, add_colors=add_colors ,forcing=forcing, induction=induction, max_first=max_first)

    g_nodes = G.nodes()

    pivots_neighbors = dict()
    for node,color in colored_nodes.items():
        if color == 1:
            pivots_neighbors[node] = set(G.neighbors(node))


    max_degree = 0
        
    if (max_first):
        max_degree = max([len(list (G.neighbors(x))) for x in G.nodes() ])
    else :
        max_degree = min([len(list (G.neighbors(x))) for x in G.nodes() ])

    max_degree_nodes = [x for x in G.nodes() if  len(list (G.neighbors(x))) == max_degree]
    main_pivot = min(max_degree_nodes)

#    colored_nodes[main_pivot] = 1
#    pivots_neighbors = dict()
#    pivots_neighbors[main_pivot] = set(G.neighbors(main_pivot))

    possible_colors = set([1,2,3,4,5,6,7,8,9])

    #choosing pivots
#    colored = 1
    pivot_class_neighbors = set(G.neighbors(main_pivot))
    previous_neighbors_count = len(pivot_class_neighbors)
    current_neighbors_increase = previous_neighbors_count
    while False:
        possible_pivots = set()
        for pivot_neighbor in pivot_class_neighbors:
            for possible_pivot in G.neighbors(pivot_neighbor):
                if(possible_pivot not in pivot_class_neighbors):
                    possible_pivots.add(possible_pivot)

        print(possible_pivots)
        for possible_pivot in possible_pivots:
            if(len([x for x in G.neighbors(possible_pivot) if x in possible_pivots]) == 0):
                neighbour_colors = set([colored_nodes[node] for node in G.neighbors(possible_pivot)])
                if(1 not in neighbour_colors):
                    if (colored_nodes[possible_pivot] == 0):
                        pivots_neighbors[possible_pivot] = set(G.neighbors(possible_pivot))
                        colored_nodes[possible_pivot] = 1
                        for n in G.neighbors(possible_pivot):
                            pivot_class_neighbors.add(n)
                        print("Initializing\t", possible_pivot, "\t", 1, "\tneighbours:\t", G.neighbors(possible_pivot), "\tColors\t", neighbour_colors)
                        colored = colored + 1
        current_neighbors_increase = previous_neighbors_count - len(pivot_class_neighbors)
        previous_neighbors_count = len(pivot_class_neighbors)


    colored = len(colored_nodes.items())
    print("Start colored\t", colored)
    while colored != 0:        

        #choosing mirrors
        while colored != 0:
            colored = 0
            if mirror:
                for pivot, first_neighbors in pivots_neighbors.items():
                    for first_neighbor in first_neighbors:
                        bad_common_num = 0
                        common  = set()
                        for pvt,neghbrs in pivots_neighbors.items():
                            for x in G.neighbors(first_neighbor):
                                if x in neghbrs and colored_nodes[x] == 0:
                                    common.add(x)
                                    if x in common and x not in list(G.neighbors(first_neighbor)):
                                        bad_common_num = bad_common_num + 1
                        print("Checking fn\t", first_neighbor,"\t",list(G.neighbors(first_neighbor)),"\twith\t", common, "\tbadnum\t", bad_common_num)
                        if bad_common_num == 0 and colored_nodes[first_neighbor] == 0:
                            first_pvt_common_neighbors = set()
                            for cmn in common:
                                for x in G.neighbors(cmn):
                                    first_pvt_common_neighbors.add(x)

                            not_possible_colors_for_common = set(colored_nodes[x] for x in first_pvt_common_neighbors)
                            possible_colors_for_common = set([x for x in possible_colors if x not in not_possible_colors_for_common])

                            not_possible_colors_for_mirror = set(colored_nodes[x] for x in G.neighbors(first_neighbor))
                            possible_colors_for_mirror = set([x for x in possible_colors if x not in not_possible_colors_for_mirror])

                            print("mirror colors:\t", possible_colors_for_mirror, "\tneighbors colors\t", possible_colors_for_common)

                            if (len (set([x for x in possible_colors_for_common or x in possible_colors_for_mirror])) < 2 ):
                                if (len(possible_colors_for_common) < 1 or len(possible_colors_for_mirror) < 1):
                                    break
                            
                            if (True):
                                mirror_color = min(possible_colors_for_mirror)
                                common_color = min([x for x in possible_colors_for_common if x != mirror_color])

                                colored_nodes[first_neighbor] = mirror_color

                                for cmn in common:
                                    colored_nodes[cmn] = common_color
                            else:
                                common_color = min(possible_colors_for_common)
                                mirror_color = min([x for x in possible_colors_for_mirror if x != common_color])

                                colored_nodes[first_neighbor] = mirror_color

                                for cmn in common:
                                    colored_nodes[cmn] = common_color


        current_color = max(possible_colors) + 1

        #Writing Forced Colors
        if False:
            if colored == 0:
                for g_node in g_nodes:
                    if (colored_nodes[g_node] == 0):
                        neighbours_colors = set()
                        for x, color in colored_nodes.items():
                            if x in list (G.neighbors(g_node)):
                                if(color != 0):
                                    neighbours_colors.add(color)
                        print("Checking Forcing node:\t", g_node, "\t", G.neighbors(g_node) ,"\t", neighbours_colors)
                        if (len(neighbours_colors) == len(possible_colors ) - 1):
                            min_colors  = [x for x in range(0, len (possible_colors) + 1) if x not in neighbours_colors or x in [0]]
                            colored_nodes[g_node] = max( min_colors)
                            if (colored_nodes[g_node] != 0):
                                colored = colored + 1
                                print("Forced\t", g_node, "\t", colored_nodes[g_node], "\t\tneighbors_colors\t:", neighbours_colors)
                                print(min_colors)
        

        #inducing colors
        if False:
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
                            min_colors  = [x for x in range(0, len (possible_colors) + 1) if (x not in neighbours_colors) or (x in [0])]
                            colored_nodes[g_node] = max(min_colors)

                            if (colored_nodes[g_node] !=  0):
                                colored = colored + 1
                                print("Induced\t", g_node, "\t", colored_nodes[g_node], "\t\tneighbors_colors\t:", neighbours_colors)
                                print(min_colors)
                                break


        print("Now colored\t", colored)

    for g_node in G.nodes():
        got_colors += colors[colored_nodes[g_node]] 

    return got_colors, len(possible_colors)

def GetColorGroundTruth(G):
    GotColors = ""

    return GotColors

def __main__ ():
    GOrder = 15
    GSize = 30
    MakeConnectedGraph = True

    G = RandomNGraph(GOrder, GSize, MakeConnectedGraph)
    GColors = "rrrgggbbbm" + "rrrgggbbbm" + "rrrgg"
    print("\t\t\t##########Test One##########")
    GColors2_Forcing,num1,hamo1 = ColorGraph2(G,add_colors= False, forcing= True, induction=False)
    print("\t\t\t##########Test Two##########")
    GColors2_Induction, num2,hamo2 = ColorGraph2(G,add_colors= False, forcing= True, induction=True)
    print("\t\t\t##########Test Three########")
    GColors2_addcolors_Forcing,num3,hamo3 = ColorGraph2(G,add_colors= True, forcing= True, induction=False)
    print("\t\t\t##########Test Four#########")
    GColors2_addcolors_Induction,num4,hamo4 = ColorGraph2(G, add_colors= True, forcing= True, induction= True)
    print("\t\t\t##########Test Five########")
    GColors2_addcolors_Forcing_min,num5 = ColorGraph3(G,add_colors= True, forcing= True, induction=False, max_first= True)
    print("\t\t\t##########Test Six#########")
    GColors2_addcolors_Induction_min,num6 = ColorGraph3(G, add_colors= True, forcing= True, induction= True, max_first= True)


    print(G.order())
    print(G.size())
    planarok, otherg = gp.check_planarity(G);
    print(planarok)

    if (not planarok):
        print("Elhamdullah")

    print(gp.chromatic_number(G))
    print(num1,"\t", num2, "\t", num3, "\t",num4, "\t", num5, "\t", num6)
    
    plt.subplot(321)
    nx.draw(G, node_color = GColors2_Forcing, with_labels  = True)
    plt.subplot(322)
    nx.draw(G, node_color = GColors2_Induction, with_labels  = True)
    plt.subplot(323)
    nx.draw(G, node_color = GColors2_addcolors_Forcing, with_labels  = True)
    plt.subplot(324)
    nx.draw(G, node_color = GColors2_addcolors_Induction, with_labels  = True)
    plt.subplot(325)
    nx.draw(G, node_color = GColors2_addcolors_Forcing_min, with_labels  = True)
    plt.subplot(326)
    nx.draw(G, node_color = GColors2_addcolors_Induction_min, with_labels  = True)
    plt.show()

    return 0

__main__()