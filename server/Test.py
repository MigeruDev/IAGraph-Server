import time
from queue import PriorityQueue

import pymongo

from server.BlindSearch import BlindSearch
from server.HeuristicSearch import HeuristicSearch

client = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = client["IAGraph"]
search = BlindSearch()
#search.randomGraph(10,4,mydb,10,10)
start_time = time.time()
#path = search.bs(mydb,0,4)
xd = mydb.complexity.find()
print([x for x in xd])
end_time = time.time()

print("Time elapsed:", 1000.0 * (end_time - start_time), "milliseconds.")