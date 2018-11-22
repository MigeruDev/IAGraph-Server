import os
import pymongo
import json
from bson.json_util import dumps
from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin
from server.BlindSearch import BlindSearch

app = Flask(__name__)
CORS(app)
#Create a connection to mongodb
MONGO_URI = os.environ.get('MONGODB_URI')

client = pymongo.MongoClient(MONGO_URI)
mydb = client["iagraph"]
search = BlindSearch()

@app.route('/')
def index():
    return 'FSAFSAFSAFAS HEROKU'

@app.route("/graph", methods = ['GET'])
def getNodes():
    nodes = mydb.nodes.find()
    links = mydb.edges.find({},{'_id':0})
    return dumps({"nodes":nodes, "links":links})


@app.route("/generate_random", methods = ['POST'])
def generateRandom():
    data = json.loads(request.data)
    #data = request.form
    noNodos = data['noNodos']
    maxHijos = data['maxHijos']
    maxHN = data['maxHN']
    maxGN = data['maxGN']
    search.randomGraph(noNodos,maxHijos,mydb,maxHN,maxGN)
    return dumps({'message' : 'SUCCESS'})

@app.route("/blind_search", methods = ['POST'])
def blindSearch():
    data = json.loads(request.data)
    #data = request.form
    start = data['start']
    goal = data['goal']
    algorithm = data['search']
    search.command(mydb,start,goal,algorithm)
    result = mydb.search.find_one({'_id': algorithm})
    return dumps(result)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
