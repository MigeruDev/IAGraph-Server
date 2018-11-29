import os
import pymongo
import json
from bson.json_util import dumps
from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename

from server.BlindSearch import BlindSearch
from server.GraphGenerator import GraphGenerator
from server.HeuristicSearch import HeuristicSearch

app = Flask(__name__)
CORS(app)
#Create a connection to mongodb
MONGO_URI = os.environ.get('MONGODB_URI') #Heroku & Local

client = pymongo.MongoClient(MONGO_URI)
mydb = client["IAGraph"]                  #IAGraph for Local - iagraph for Heroku
graph = GraphGenerator()
blind_search = BlindSearch()
heuristic_search = HeuristicSearch()

@app.route('/')
def index():
    return ':v'

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
    graph.randomGraph(noNodos,maxHijos,mydb,maxHN,maxGN)
    return dumps({'message' : 'SUCCESS'})

@app.route("/blind_search", methods = ['POST'])
def blindSearch():
    data = json.loads(request.data)
    #data = request.form
    start = data['start']
    goal = data['goal']
    algorithm = data['search']
    blind_search.command(mydb,start,goal,algorithm)
    result = mydb.search.find_one({'_id': algorithm})
    return dumps(result)

@app.route("/heuristic_search", methods = ['POST'])
def heuristicSearch():
    data = json.loads(request.data)
    #data = request.form
    start = data['start']
    goal = data['goal']
    algorithm = data['search']
    heuristic_search.command(mydb,start,goal,algorithm)
    result = mydb.search.find_one({'_id': algorithm})
    return dumps(result)

@app.route("/complexity", methods = ['GET'])
def getComplexity():
    complexity = mydb.complexity.find()
    return dumps(complexity)

@app.route("/upload", methods = ['POST'])
def upload_file():
    print(request.files)
    if request.method =='POST':
        files = request.files.getlist('file')
        print('files',files)
        if files:
            for file in files:
                filename = secure_filename(file.filename)
                print("path= ",os.path)
                file.save(os.path.join(".",filename))
            graph.uploadGraph(mydb)
            return "Succesfuly brooooooooo"
    return "Something went wrong xd"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.debug = True
    app.run(host='127.0.0.1',port=port) #for local
    #app.run(host='0.0.0.0', port=port) #for Heroku
