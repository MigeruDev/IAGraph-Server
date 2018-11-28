import random
import threading
import time
from queue import PriorityQueue


class BlindSearch():

    def command(self, mydb, start, end, algorithm):

        command = { 'BFS': self.bfs,
                    'DFS': self.dfs,
                    'IDDFS': self.iddfs,
                    'UCS': self.ucs}

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
        start_time = time.time()
        search = {}
        search['$set'] = {'_id':'BFS',
                  'queue':[[start]],
                  'pop':[''],
                  'path':[],
                  'start':start,
                  'goal':end,
                  'complexity':0,
                  'temporal':0,
                  'spatial':0}
        promedio = 0
        cont = 0
        nodes = mydb['nodes']
        queue = [(start,[start])]
        visited = set()

        while queue:
            vertex, path = queue.pop(0)
            visited.add(vertex)
            hijos = nodes.find_one({"_id": vertex}, {"_id": 0, "hijos": 1})
            hijos['hijos'].sort()
            promedio += len(hijos['hijos'])
            cont += 1
            if vertex == end:
                #print('%40s' % (end))
                search['$set']['queue'].append([''])
                search['$set']['pop'].append(end)
                search['$set']['path'] = path
                end_time = time.time()
                search['$set']['complexity'] = end_time - start_time
                search['$set']['temporal'] = (promedio / cont) ** len(path)
                search['$set']['spatial'] = (promedio / cont) * len(path)
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
        end_time = time.time()
        search['$set']['complexity'] = end_time - start_time
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
        start_time = time.time()
        search = {}
        search['$set'] = {'_id':'DFS',
                         'queue':[[start]],
                         'pop':[''],
                         'path':[],
                         'start':start,
                         'goal':goal,
                          'complexity':0,
                          'temporal':0,
                          'spatial':0}
        promedio = 0
        cont = 0
        nodes = mydb['nodes']
        queue = [(start,[start])]
        visited = set()

        while queue:
            vertex, path = queue.pop(0)
            visited.add(vertex)
            hijos = nodes.find_one({"_id": vertex}, {"_id": 0, "hijos": 1})
            #hijos['hijos'].sort()
            promedio += len(hijos['hijos'])
            cont += 1
            if vertex == goal:
                #print('%40s' % (vertex))
                search['$set']['queue'].append([''])
                search['$set']['pop'].append(goal)
                search['$set']['path'] = path
                end_time = time.time()
                search['$set']['complexity'] = end_time - start_time
                search['$set']['temporal'] = (promedio / cont) ** len(path)
                search['$set']['spatial'] = (promedio / cont) * len(path)
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
        end_time = time.time()
        search['$set']['complexity'] = end_time - start_time
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
        start_time = time.time()
        search = {}
        search['$set'] = {'_id': 'IDDFS',
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
            promedio += len(hijos['hijos'])
            cont += 1
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
                end_time = time.time()
                search['$set']['complexity'] = end_time - start_time
                search['$set']['temporal'] = (promedio / cont) ** len(path)
                search['$set']['spatial'] = (promedio / cont)
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
                        end_time = time.time()
                        search['$set']['complexity'] = end_time - start_time
                        search['$set']['temporal'] = (promedio / cont) ** len(path)
                        search['$set']['spatial'] = (promedio / cont)
                        mydb['search'].update_one({'_id': 'IDDFS'}, search, True)
                        #return path + [node]
                        return 'Se ha encontrado una solución'
                    hijos = nodes.find_one({"_id": node}, {"_id": 0, "hijos": 1})
                    hijos['hijos'].sort()
                    promedio += len(hijos['hijos'])
                    cont += 1
                    aux = aux + [x for x in hijos['hijos']
                                 if x not in aux]

                    #print('%20s' % (aux+[x for x, y in queue]), end='')
                    #print('%20s' % (node))
                    search['$set']['queue'].append(aux + [x for x,y in queue])
                    search['$set']['pop'].append(node)
            for node in aux:
                visited.add(node)
                queue.append((node, path+[node]))
        end_time = time.time()
        search['$set']['complexity'] = end_time - start_time
        mydb['search'].update_one({'_id': 'IDDFS'}, search, True)


    '''
    This search strategy is for weighted graphs. Each edge has a weight, and vertices are 
    expanded according to that weight; specifically, cheapest node first. As we move deeper 
    into the graph the cost accumulates. Check out Artificial Intelligence - Uniform Cost Search 
    if you are not familiar with how UCS operates.
    '''
    def ucs(self, mydb, start, goal):
        #print('------------Algoritmo de costo uniforme----------')
        #print('%20s%20s' % ("Cola", "Extraer"))
        #print('%20s' % (start))
        start_time = time.time()
        search = {}
        search['$set'] = {'_id': 'UCS',
                          'queue': [[start]],
                          'pop': [''],
                          'total_cost':[''],
                          'path': [],
                          'start': start,
                          'goal': goal,
                          'complexity':0,
                          'temporal':0,
                          'spatial':0}
        promedio = 0
        cont = 0
        visited = set()
        queue = PriorityQueue()
        queue.put((0, start,[start]))

        nodes = mydb["nodes"]
        edges = mydb["edges"]

        while queue:
            cost, node,path = queue.get()

            if node not in visited:
                visited.add(node)

                if node == goal:
                    #print('%20s' % (path ), end='')
                    #print('%20s' % (node), end='')
                    #print('%20s' % (cost))
                    #return path
                    search['$set']['queue'].append(path)
                    search['$set']['pop'].append(node)
                    search['$set']['total_cost'].append(cost)
                    search['$set']['path'] = path
                    end_time = time.time()
                    search['$set']['complexity'] = end_time - start_time
                    search['$set']['temporal'] = (promedio / cont) ** len(path)
                    search['$set']['spatial'] = (promedio / cont) * len(path)
                    mydb['search'].update_one({'_id': 'UCS'}, search, True)

                    return 'Se ha encontrado una solución'

                hijos = nodes.find_one({"_id": node}, {"_id": 0, "hijos": 1})
                promedio += len(hijos['hijos'])
                cont += 1
                for i in hijos["hijos"]:
                    if i not in visited:
                        peso = edges.find_one({"source": node,"target":i}, {"_id": 0, "value": 1})
                        total_cost = cost + peso["value"]
                        queue.put((total_cost, i,path+[i]))

                        aux = str(i)+"("+str(peso['value'])+")"
                        #print('%20s'%(path+[i]),end='')
                        #print('%20s'%(aux),end='')
                        #print('%20s'%(total_cost))
                        search['$set']['queue'].append(path+[i])
                        search['$set']['pop'].append(aux)
                        search['$set']['total_cost'].append(total_cost)
        end_time = time.time()
        search['$set']['complexity'] = end_time - start_time
        mydb['search'].update_one({'_id': 'UCS'}, search, True)


    '''
    Bidirectional-Search
    '''

    def hilo1(self, mydb, start, goal, out_init, out_end):
        if len(self.getParents(mydb,goal[0])) == 0:
            return None
        cola = [start]
        nodes = mydb['nodes']
        while cola and goal:
            print("colaH1= ",cola)
            evalue_node = cola[0]
            print("enH1=", evalue_node)
            hijos = nodes.find_one({"_id": evalue_node}, {"_id": 0, "hijos": 1})
            for node_son in hijos['hijos'].__reversed__():
                if not node_son in cola and not node_son in out_init:
                    cola = [node_son] + cola
            if evalue_node in goal:
                goal.remove(evalue_node)
            if evalue_node in out_end:
                break
            out_init.append(evalue_node)

            cola.remove(evalue_node)

        if len(goal):
            return None

    def hilo2(self, mydb, start, goal, out_init, out_end):
        nodes = mydb['nodes']
        hijos = nodes.find_one({"_id": start[0]}, {"_id": 0, "hijos": 1})

        if len(hijos['hijos']) == 0:
            return None

        cola = [goal]
        while cola and start:
            print("colaH2= ",cola)
            evalue_node = cola[0]
            print("enH2= ", evalue_node)
            for node_son in self.getParents(mydb,evalue_node).__reversed__():
                if not node_son in cola and not node_son in out_end:
                    cola = [node_son] + cola
            if evalue_node in start:
                start.remove(evalue_node)
            if evalue_node in out_init:
                break
            out_end.insert(0, evalue_node)
            cola.remove(evalue_node)

        if len(start):
            return None

    def getParents(self,mydb,node):
        edges = mydb['edges']
        link = edges.find({'target':node})
        parents = []
        for i in link:
            parents.append(i['source'])
        return parents


    # busqueda bidireccional.
    def bs(self, mydb, start, goal):
        start_time = time.time()
        search = {}
        search['$set'] = {'_id': 'BS',
                          'queue': [[start]],
                          'pop': [''],
                          'path': [],
                          'start': start,
                          'goal': goal,
                          'complexity': 0,
                          'temporal':0,
                          'spatial':0}
        out_init = []
        out_end = []

        t1 = threading.Thread( self.hilo1(mydb, start, [goal], out_init, out_end))
        t2 = threading.Thread( self.hilo2(mydb, [start], goal, out_init, out_end))

        t1.start()
        t2.start()

        t1.join()
        t2.join()
        end_time = time.time()
        search['$set']['complexity'] = end_time - start_time
        search['$set']['queue'] = out_init
        mydb['search'].update_one({'_id': 'BS'}, search, True)
        return out_init + out_end
