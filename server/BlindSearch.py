import random
from queue import PriorityQueue


class BlindSearch():

    # Numero de nodos, max hijos, connectionDB, MaxPeso
    def randomGraph(self, N, Nsons, mydb, maxHN:int=100, maxGN:int=100):
        #Drop collections if exist
        mydb["nodes"].drop()
        mydb["edges"].drop()
        mydb['search'].drop()
        #Create collections
        nodes = mydb["nodes"]
        edges = mydb["edges"]

        nodos = set(i for i in range(N))
        #S is an auxiliary nodes set
        S = set(nodos)
        checked = set()
        # Pick a random node, and mark it as visited and the current node
        current_node = random.sample(S, 1).pop()
        S.remove(current_node)
        checked.add(current_node)
        # Create a random connected graph
        while S:
            # Randomly pick the next node from the neighbors of the current node
            # As we are generating a connected graph, we assume a complete graph
            neighbor = random.sample(nodos, 1).pop()
            # If the new node hasn't been visited, add the edge from current to new
            if neighbor not in checked:
                # Consultamos si el nodo actual tiene hijos
                current_node_sons = nodes.find_one({"_id": current_node}, {"_id": 0, "hijos": 1})
                # Verificamos que no sobrepase el limite de hijos que puede tener (Nsons)
                if (current_node_sons==None or len(current_node_sons["hijos"])<Nsons)\
                        and current_node != neighbor:
                    #Se crea un documento que contenga el nodo y sus hijos
                    record = {}
                    record["$set"] = {"_id": current_node,"Gn":random.randint(0, maxGN)}
                    record['$addToSet'] = {"hijos": neighbor}

                    #Se inserta el documento dentro de la collection nodes
                    nodes.update_one({"_id":current_node},record,True)
                    current_node_sons = nodes.find_one({"_id":current_node}, {"_id":0,"hijos":1})
                    #Se agregan hijos aleatorios
                    for i in range(0,Nsons-len(current_node_sons["hijos"]),1):
                        random_node = random.sample(nodos, 1).pop()
                        if random_node != current_node:
                            record = {}
                            record["$set"] = {"_id": current_node,"Gn":random.randint(0, maxGN)}
                            record['$addToSet'] = {"hijos": random_node}
                            nodes.update_one({"_id": current_node}, record, True)
                            record = {}
                            record["$set"] = {"source": current_node, "target": random_node,
                                              "value": random.randint(0, maxHN)}
                            # Se inserta la arista
                            edges.update_one({"source": current_node, "target": random_node}, record, True)

                    record = {}
                    record["$set"] = {"_id": neighbor,"Gn":random.randint(0, maxGN)}
                    record['$setOnInsert'] = {"hijos": []}
                    nodes.update_one({"_id": neighbor}, record, True)

                    record = {}
                    record["$set"] = {"source": current_node,"target":neighbor,
                                      "value":random.randint(0, maxHN)}
                    #Se inserta la arista
                    edges.update_one({"source": current_node,"target":neighbor}, record, True)

                    S.remove(neighbor)
                    checked.add(neighbor)

            # Set the new node as the current node.
            current_node = neighbor
        return ''

    def command(self, mydb, start, end, algorithm):

        command = { 'BFS': self.bfs,
                    'DFS': self.dfs,
                    'IDDFS': self.iddfs,
                    'UCS': self.uniform_cost_search}

        func = command.get(algorithm, lambda: "Invalid command")
        return  func(mydb,start,end)


    '''
    BFS is a traversing algorithm where you should start traversing from a selected node
    (source or starting node) and traverse the graph layerwise thus exploring the neighbour nodes
    (nodes which are directly connected to source node).
    You must then move towards the next-level neighbour nodes.
    '''
    def bfs(self, mydb, start, end):
        #print('------------Algoritmo de búsqueda de amplitud 2------------')
        #print('%20s%20s' % ("Cola", "Extraer"))
        #print('%20s' % (start))
        search = {}
        search['$set'] = {'_id':'BFS',
                  'queue':[[start]],
                  'pop':[''],
                  'path':[],
                  'start':start,
                  'goal':end}
        nodes = mydb['nodes']
        queue = [(start,[start])]
        visited = set()

        while queue:
            vertex, path = queue.pop(0)
            visited.add(vertex)
            hijos = nodes.find_one({"_id": vertex}, {"_id": 0, "hijos": 1})
            hijos['hijos'].sort()
            if vertex == end:
                #print('%40s' % (end))
                search['$set']['queue'].append([''])
                search['$set']['pop'].append(end)
                search['$set']['path'] = path
                mydb['search'].update_one({'_id':'BFS'},search,True)
                return 'Se ha encontrado una solución'
            else:
                for node in hijos['hijos']:
                    if node not in visited:
                        visited.add(node)
                        queue.append((node, path+[node]))
            #print('%20s' % ([x for x, y in queue]), end='')
            #print('%20s' % (vertex))
            search['$set']['queue'].append([x for x, y in queue])
            search['$set']['pop'].append(vertex)
        mydb['search'].update_one({'_id': 'BFS'}, search, True)


    '''
    The DFS algorithm is a recursive algorithm that uses the idea of backtracking.
    It involves exhaustive searches of all the nodes by going ahead, if possible, 
    else by backtracking.
    '''
    def dfs(self, mydb, start, goal):
        #print('------------Algoritmo de búsqueda de profundidad 2----------')
        #print('%20s%20s' % ("Cola", "Extraer"))
        #print('%20s' % (start))
        search = {}
        search['$set'] = {'_id':'DFS',
                         'queue':[[start]],
                         'pop':[''],
                         'path':[],
                         'start':start,
                         'goal':goal}
        nodes = mydb['nodes']
        queue = [(start,[start])]
        visited = set()

        while queue:
            vertex, path = queue.pop(0)
            visited.add(vertex)
            hijos = nodes.find_one({"_id": vertex}, {"_id": 0, "hijos": 1})
            #hijos['hijos'].sort()
            if vertex == goal:
                #print('%40s' % (vertex))
                search['$set']['queue'].append([''])
                search['$set']['pop'].append(goal)
                search['$set']['path'] = path
                mydb['search'].update_one({'_id': 'DFS'}, search, True)
                return 'Se ha encontrado una solución'
            else:
                for next in hijos['hijos']:
                    if next not in visited:
                        visited.add(next)
                        queue.insert(0,(next,path+[next]))

            #print('%20s' % ([x for x, y in queue]), end='')
            #print('%20s' % (vertex))
            search['$set']['queue'].append([x for x, y in queue])
            search['$set']['pop'].append(vertex)
        mydb['search'].update_one({'_id': 'DFS'}, search, True)


    '''
    Iterative deepening depth-first search (IDDFS) is an extension to 
    the ‘vanilla’ depth-first search algorithm, with an added constraint 
    on the total depth explored per iteration.
    '''
    def iddfs(self, mydb,start, goal):
        #print('------------Algoritmo de búsqueda de profundidad 2----------')
        #print('%20s%20s' % ("Cola", "Extraer"))
        #print('%20s' % (start))
        search = {}
        search['$set'] = {'_id': 'IDDFS',
                          'queue': [[start]],
                          'pop': [''],
                          'path': [],
                          'start': start,
                          'goal': goal}
        nodes = mydb['nodes']
        queue = []
        visited = set()
        visited.add(start)
        hijos = nodes.find_one({"_id": start}, {"_id": 0, "hijos": 1})
        hijos['hijos'].sort()
        for node in hijos['hijos']:
            visited.add(node)
            queue.append((node,[start]))
        #print('%20s' % ([x for x, y in queue]), end='')
        #print('%20s' % (start))
        search['$set']['queue'].append([x for x,y in queue])
        search['$set']['pop'].append(start)
        while queue:
            vertex, path = queue.pop(0)
            visited.add(vertex)
            hijos = nodes.find_one({"_id": vertex}, {"_id": 0, "hijos": 1})
            hijos['hijos'].sort()
            aux = [x for x in hijos['hijos'] if x not in visited]
            #print('%20s'%(aux+[x for x,y in queue]),end='')
            #print('%20s'%(vertex))
            search['$set']['queue'].append(aux+[x for x,y in queue])
            search['$set']['pop'].append(vertex)
            if vertex == goal:
                #print('%40s' % (vertex))
                search['$set']['queue'].append([''])
                search['$set']['pop'].append(goal)
                search['$set']['path'] = path + [vertex]
                mydb['search'].update_one({'_id': 'IDDFS'}, search, True)
                #return path + [vertex]
                return 'Se ha encontrado una solución'
            else:
                while queue:
                    node, path2 = queue.pop(0)
                    visited.add(node)
                    if node == goal:
                        #print('%40s' % (node))
                        search['$set']['queue'].append([''])
                        search['$set']['pop'].append(goal)
                        search['$set']['path'] = path + [node]
                        mydb['search'].update_one({'_id': 'IDDFS'}, search, True)
                        #return path + [node]
                        return 'Se ha encontrado una solución'
                    hijos = nodes.find_one({"_id": node}, {"_id": 0, "hijos": 1})
                    hijos['hijos'].sort()
                    aux = aux + [x for x in hijos['hijos']
                                 if x not in aux]

                    #print('%20s' % (aux+[x for x, y in queue]), end='')
                    #print('%20s' % (node))
                    search['$set']['queue'].append(aux + [x for x,y in queue])
                    search['$set']['pop'].append(node)
            for node in aux:
                visited.add(node)
                queue.append((node, path+[node]))
        mydb['search'].update_one({'_id': 'IDDFS'}, search, True)


    '''
    This search strategy is for weighted graphs. Each edge has a weight, and vertices are 
    expanded according to that weight; specifically, cheapest node first. As we move deeper 
    into the graph the cost accumulates. Check out Artificial Intelligence - Uniform Cost Search 
    if you are not familiar with how UCS operates.
    '''
    def uniform_cost_search(self, mydb, start, goal):
        visited = set()
        queue = PriorityQueue()
        queue.put((0, start))

        nodes = mydb["nodes"]
        edges = mydb["edges"]

        #path = [start]

        while queue:
            cost, node = queue.get()
            #path += [node]
            if node not in visited:
                visited.add(node)

                if node == goal:
                    return queue

                hijos = nodes.find_one({"_id": node}, {"_id": 0, "hijos": 1})

                for i in hijos["hijos"]:
                    if i not in visited:
                        peso = edges.find_one({"from": node,"to":i}, {"_id": 0, "weight": 1})
                        total_cost = cost + peso["weight"]
                        queue.put((total_cost, i))
                        #path += [i]