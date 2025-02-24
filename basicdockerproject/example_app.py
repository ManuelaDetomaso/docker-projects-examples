from flask import Flask, jsonify, request

app = Flask(__name__) #Flask("Hi Flask!")

@app.route("/") #this application is listening on "/"
def hello_world():
    return "Hello World!" #return a string

@app.route("/hithere") #this application is listening on "/hithere"
def hi_there_everyone():
    return "I just hit /hithere!" #return a string

@app.route("/bye") #this application is listening on "/bye"
def bye():
    1/0
    return "Bye!" #return a string

@app.route("/examplejson") #this application is listening on "/bye"
def examplejson():
    computation = 2*3
    retjson = {
        "field_1":1, 
        "field_2":"abc",
        "field_3":None,
        "field_4":True,
        "field_5": ["abc", 1,2,3],
        "field_6": [
            {
                "field_7": computation
            }
        ]
        }
    return jsonify(retjson) #WebServices usually return jsons ({}), while WebApplications usually return pages (index.html)

@app.route("/add_two_nums", methods=["POST", "GET"]) #this application is listening on "/bye"
def add_two_nums():
    try:
        dataDict = request.get_json()
        x = dataDict["x"]
        y = dataDict["y"]
        z=x+y
        retJson = {"z": z}
        return jsonify(retJson), 200
    except Exception:
        return "ERROR", 305

if __name__=="__main__":
    #app.run(host="127.0.0.1", port=80) #app.run() can be empty until deploy
    app.run(debug=True) # ensures to visualise an Internal Server Error in case of errors into APIs



