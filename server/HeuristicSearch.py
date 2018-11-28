import time
from queue import PriorityQueue


class HeuristicSearch():

    def command(self, mydb, start, goal, algorithm):

        command = { 'HC': self.hc,
                    'BestFS': self.bfs,
                    'A*': self.astar,
                    'GS': self.gs}

        func = command.get(algorithm, lambda: "Invalid command")
        return  func(mydb,start,goal)


    '''
    Hill climbing is a mathematical optimization technique which belongs 
    to the family of local search. It is an iterative algorithm that starts
    with an arbitrary solution to a problem, then attempts to find a better solution by making an incremental change to the solution. If the change produces a better
    solution, another incremental change is made to the new solution, 
    and so on until no further improvements can be found
    '''
    def hc(self, mydb, start, goal):
        #print('------------Algoritmo de Busqueda Gradiente----------')
        #print('%20s%20s' % ("Cola", "Extraer"))
        #print('%20s' % (start))
        start_time = time.time()
        search = {}
        search['$set'] = {'_id': 'HC',
                          'queue': [[start]],
                          'pop': [''],
                          'path': [],
                          'start': start,
                          'goal': goal,
                          'complexity': 0,
                          'temporal':0,
                          'spatial':0}
        promedio = 0
        cont = 0
        queue = [(0,start)]
        path = []
        nodes = mydb['nodes']

        while queue:
            val, current = min(queue)
            path.append(current)
            #print('queue= ',queue)

            queue = []
            hijos = nodes.find_one({"_id": current}, {"_id": 0})
            promedio += len(hijos['hijos'])
            cont += 1
            if current == goal:
                #print('%40s'%(current))
                #return path
                end_time = time.time()
                search['$set']['queue'].append('')
                search['$set']['pop'].append(current)
                search['$set']['path'] = path
                search['$set']['complexity'] = end_time-start_time
                search['$set']['temporal'] = len(path)
                search['$set']['spatial'] = (promedio / cont)
                mydb['search'].update_one({'_id': 'HC'}, search, True)

                return 'Se ha encontrado una solución'
            else:
                for node in hijos['hijos']:
                    value = nodes.find_one({"_id": node},
                                           {"_id": 0, 'Gn':1})
                    queue.append((value['Gn'],node))
            #print('%20s' % ([str(y) + '(' + str(x) + ')' for x, y
            #                 in queue]), end='')
            #print('%20s' % (current))
            search['$set']['queue'].append([str(y) + '(' + str(x) + ')'
                            for x, y in queue])
            search['$set']['pop'].append(current)
        end_time = time.time()
        search['$set']['complexity'] = end_time - start_time
        mydb['search'].update_one({'_id': 'HC'}, search, True)

    '''
    Best-First-Search
    In BFS and DFS, when we are at a node, we can consider any of the 
    adjacent as next node. So both BFS and DFS blindly explore paths 
    without considering any cost function. The idea of Best First Search 
    is to use an evaluation function to decide which adjacent is most 
    promising and then explore.
    '''
    def bfs(self, mydb, start, goal):
        #print('------------Algoritmo Primero el Mejor-----------')
        #print('%20s%20s' % ("Cola", "Extraer"))
        #print('%20s' % (start))
        start_time= time.time()
        search = {}
        search['$set'] = {'_id': 'BestFS',
                          'queue': [[start]],
                          'pop': [''],
                          'path': [],
                          'start': start,
                          'goal': goal,
                          'complexity':0,
                          'temporal':0,
                          'spatial':0}
        promedio = 0
        cont = 0
        queue = PriorityQueue()
        queue.put((0,start,[start]))
        nodes = mydb['nodes']
        visited = set()
        while queue:
            cost, current,path = queue.get()
            visited.add(current)
            hijos = nodes.find_one({'_id':current},{'_id':0})
            promedio += len(hijos['hijos'])
            cont += 1
            if current == goal:
                #print('%40s'%(current))
                #return path
                search['$set']['queue'].append('')
                search['$set']['pop'].append(current)
                search['$set']['path'] = path
                end_time = time.time()
                search['$set']['complexity'] = end_time - start_time
                search['$set']['temporal'] = (promedio / cont)**len(path)
                search['$set']['spatial'] = (promedio / cont)**len(path)
                mydb['search'].update_one({'_id': 'BestFS'}, search, True)

                return 'Se ha encontrado una solución'
            else:
                for node in hijos['hijos']:
                    if node not in visited:
                        visited.add(node)
                        value = nodes.find_one({"_id": node},
                                               {"_id": 0, 'Gn': 1})
                        queue.put((value['Gn'],node,path+[node]))
            #print('%20s' % ([str(y)+'('+str(x)+')'
            #               for x,y,z in queue.queue]), end='')
            #print('%20s' % (current))
            search['$set']['queue'].append([str(y)+'('+str(x)+')'
                           for x,y,z in queue.queue])
            search['$set']['pop'].append(current)
        end_time = time.time()
        search['$set']['complexity'] = end_time - start_time
        mydb['search'].update_one({'_id': 'BestFS'}, search, True)

    '''
    '''
    def astar(self, mydb, start, goal):
        #print('------------Algoritmo A estrella-----------')
        #print('%20s%20s' % ("Cola", "Extraer"))
        #print('%20s' % (start))
        start_time = time.time()
        search = {}
        search['$set'] = {'_id': 'A*',
                          'queue': [[start]],
                          'pop': [''],
                          'path': [],
                          'start': start,
                          'goal': goal,
                          'complexity':0,
                          'temporal':0,
                          'spatial':0}
        #(funcion evaluacion, heuristica, path)
        promedio = 0
        cont = 0
        queue = {start:(0,0,[start])}
        visited = {}
        nodes = mydb['nodes']
        edges = mydb['edges']

        while queue:
            current = min(queue, key=queue.get)
            gn, hn, path = queue.pop(current)
            visited[current] = gn

            hijos = nodes.find_one({'_id': current}, {'_id': 0,'hijos':1})
            promedio += len(hijos['hijos'])
            cont += 1
            if current == goal:
                #print('%40s'%(current))
                #return path
                search['$set']['queue'].append('')
                search['$set']['pop'].append(current)
                search['$set']['path'] = path
                end_time = time.time()
                search['$set']['complexity'] = end_time - start_time
                search['$set']['temporal'] = (promedio / cont)**len(path)
                search['$set']['spatial'] = (promedio / cont)**len(path)
                mydb['search'].update_one({'_id': 'A*'}, search, True)

                return 'Se ha encontrado una solución'
            else:
                for node in hijos['hijos']:
                    value = nodes.find_one({'_id':node},
                                           {'_id':0,'Gn':1})
                    link = edges.find_one({"source": current, "target": node}, {"_id": 0, "value": 1})
                    gn = value['Gn']+hn+link['value']
                    if node in visited and gn < visited[node]:
                        node_sons = nodes.find_one({'_id': node}, {'_id': 0})
                        promedio += len(node_sons['hijos'])
                        cont += 1
                        for sub_node in node_sons['hijos']:
                            if sub_node in queue:
                                sub_node_value = nodes.find_one({'_id': sub_node},
                                                       {'_id': 0, 'Gn': 1})
                                sub_node_edge = edges.find_one({"source": node, "target": sub_node}, {"_id": 0, "value": 1})
                                queue[sub_node] = (sub_node_value['Gn']
                                +hn+sub_node_edge['value'],hn+sub_node_edge['value'],
                                        path+[node]+[sub_node] )
                    else:
                        queue[node] = (gn, hn+link['value'],path+[node])

            aux = [str(x)+'('+str(y[0]-y[1])+'+'+str(y[1])+')' for x,y in queue.items()]
            #print('%20s'%(aux),end='')
            #print('%20s'%(current))
            search['$set']['queue'].append(aux)
            search['$set']['pop'].append(current)
        end_time = time.time()
        search['$set']['complexity'] = end_time - start_time
        mydb['search'].update_one({'_id': 'A*'}, search, True)


    '''
    Greedy-Search
    '''
    def gs(self, mydb, start, goal):
        # print('------------Algoritmo de Busqueda Avara----------')
        # print('%20s%20s' % ("Cola", "Extraer"))
        # print('%20s' % (start))
        start_time = time.time()
        search = {}
        search['$set'] = {'_id': 'GS',
                          'queue': [[start]],
                          'pop': [''],
                          'path': [],
                          'start': start,
                          'goal': goal,
                          'complexity': 0,
                          'temporal':0,
                          'spatial':0}
        promedio = 0
        cont = 0
        queue = [(0, start)]
        path = []
        nodes = mydb['nodes']

        while queue:
            val, current = min(queue)
            path.append(current)
            # print('queue= ',queue)

            queue = []
            hijos = nodes.find_one({"_id": current}, {"_id": 0})
            promedio += len(hijos['hijos'])
            cont += 1
            if current == goal:
                # print('%40s'%(current))
                # return path
                search['$set']['queue'].append('')
                search['$set']['pop'].append(current)
                search['$set']['path'] = path
                end_time = time.time()
                search['$set']['complexity'] = end_time - start_time
                search['$set']['temporal'] = (promedio / cont)**len(path)
                search['$set']['spatial'] = (promedio / cont)**len(path)
                mydb['search'].update_one({'_id': 'GS'}, search, True)

                return 'Se ha encontrado una solución'
            else:
                for node in hijos['hijos']:
                    value = nodes.find_one({"_id": node},
                                           {"_id": 0, 'Gn': 1})
                    queue.append((value['Gn'], node))
            # print('%20s' % ([str(y) + '(' + str(x) + ')' for x, y
            #                 in queue]), end='')
            # print('%20s' % (current))
            search['$set']['queue'].append([str(y) + '(' + str(x) + ')'
                                            for x, y in queue])
            search['$set']['pop'].append(current)
        end_time = time.time()
        search['$set']['complexity'] = end_time - start_time
        mydb['search'].update_one({'_id': 'GS'}, search, True)
