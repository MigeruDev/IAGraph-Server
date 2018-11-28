import time
from queue import PriorityQueue

import pymongo

from server.BlindSearch import BlindSearch
from server.GraphGenerator import GraphGenerator
from server.HeuristicSearch import HeuristicSearch
import csv

client = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = client["IAGraph"]
search = BlindSearch()
#search.randomGraph(10,4,mydb,10,10)
#path = search.bs(mydb,0,4)

graph = GraphGenerator()

#graph.uploadGraph(mydb)

search.bfs(mydb,1,9)
