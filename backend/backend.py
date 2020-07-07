import bottle
import useDB
from truckpad.bottle.cors import CorsPlugin, enable_cors

app = bottle.Bottle()


@enable_cors
@app.route("/api/tasks/", method=["GET", "POST"])
def getOrAddTask():
    if bottle.request.method == 'GET':
        bottle.response.content_type = 'application/json'
        return useDB.getAllEntries()
    elif bottle.request.method == "POST":
        desc = bottle.request.json['description']
        is_completed = bottle.request.json['is_completed']
        return useDB.addNewEntry(desc, is_completed)

@enable_cors
@app.route("/api/tasks/desc=:desc&iscompl=:iscompl", method=["DELETE"])
def deleteTask(desc, iscompl):
    return useDB.deleteEntry(desc, iscompl)

@enable_cors
@app.route("/api/tasks/descold=:descold&iscomplold=:iscomplold&desc=:desc&iscompl=:iscompl", method=["PUT"])
def modifyTask(descold, iscomplold, desc, iscompl):
    return useDB.updateEntry(descold, iscomplold, desc, iscompl)

app.install(CorsPlugin(origins=['http://localhost:8080']))


if __name__ == "__main__":
    bottle.run(app, host="localhost", port=5000)