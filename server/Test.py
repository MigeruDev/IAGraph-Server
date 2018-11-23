import pymongo

from server.BlindSearch import BlindSearch

client = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = client["IAGraph"]
search = BlindSearch()
#search.randomGraph(10,4,mydb,10,10)
path = search.command(mydb,0,9,'IDDFS')
print(path)