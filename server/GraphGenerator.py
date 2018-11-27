import random


class GraphGenerator():
    # Numero de nodos, max hijos, connectionDB, MaxPeso
    def randomGraph(self, N, Nsons, mydb, maxHN: int = 100, maxGN: int = 100):
        # Drop collections if exist
        mydb["nodes"].drop()
        mydb["edges"].drop()
        mydb['search'].drop()
        # Create collections
        nodes = mydb["nodes"]
        edges = mydb["edges"]

        b = Nsons
        d = 0

        nodos = set(i for i in range(N))
        # S is an auxiliary nodes set
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
                if (current_node_sons == None or len(current_node_sons["hijos"]) < Nsons) \
                        and current_node != neighbor:
                    # Se crea un documento que contenga el nodo y sus hijos
                    d += 1
                    record = {}
                    record["$set"] = {"_id": current_node, "Gn": random.randint(0, maxGN)}
                    record['$addToSet'] = {"hijos": neighbor}

                    # Se inserta el documento dentro de la collection nodes
                    nodes.update_one({"_id": current_node}, record, True)
                    current_node_sons = nodes.find_one({"_id": current_node}, {"_id": 0, "hijos": 1})
                    # Se agregan hijos aleatorios
                    for i in range(0, Nsons - len(current_node_sons["hijos"]), 1):
                        random_node = random.sample(nodos, 1).pop()
                        if random_node != current_node:
                            record = {}
                            record["$set"] = {"_id": current_node, "Gn": random.randint(0, maxGN)}
                            record['$addToSet'] = {"hijos": random_node}
                            nodes.update_one({"_id": current_node}, record, True)
                            record = {}
                            record["$set"] = {"source": current_node, "target": random_node,
                                              "value": random.randint(0, maxHN)}
                            # Se inserta la arista
                            edges.update_one({"source": current_node, "target": random_node}, record, True)

                    record = {}
                    record["$set"] = {"_id": neighbor, "Gn": random.randint(0, maxGN)}
                    record['$setOnInsert'] = {"hijos": []}
                    nodes.update_one({"_id": neighbor}, record, True)

                    record = {}
                    record["$set"] = {"source": current_node, "target": neighbor,
                                      "value": random.randint(0, maxHN)}
                    # Se inserta la arista
                    edges.update_one({"source": current_node, "target": neighbor}, record, True)

                    S.remove(neighbor)
                    checked.add(neighbor)

            # Set the new node as the current node.
            current_node = neighbor
        complexity = mydb['complexity']
        aux = {}
        aux["$set"] = {'_id':1,"d": d, 'b': b}

        complexity.update_one({"_id": 1}, aux, True)

        return ''


