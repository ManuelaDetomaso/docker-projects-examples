from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt
import numpy as np
import tensorflow as tf
import requests
import subprocess
import json

from keras.applications import InceptionV3
from keras.applications.inception_v3 import preprocess_input
from keras.applications import imagenet_utils
from tensorflow.keras.preprocessing.image import img_to_array
from PIL import Image
from io import BytesIO

app = Flask(__name__)
api = Api(app)

# Load the pretrained model 

pretrained_model = InceptionV3(weights="imagenet")

client = MongoClient("mongodb://db:27017")
db = client.IRG
users = db["Users"]

def UserExist(username):
    # if users.find({"Username":username}).count() == 0:
    if users.count_documents({"Username":username}) == 0:
        return False
    else:
        return True

class Register(Resource):
    def post(self):
        #Step 1 is to get posted data by the user
        postedData = request.get_json()

        #Get the data
        username = postedData["username"]
        password = postedData["password"] #"123xyz"

        # check if the username already exist
        if UserExist(username):
            retJson = {
                'status':301,
                'msg': 'Invalid Username'
            }
            return jsonify(retJson)

        hashed_pw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

        #Store username and pw into the database
        users.insert_one({
            "Username": username,
            "Password": hashed_pw,
            "Tokens":6
        })

        retJson = {
            "status": 200,
            "msg": "You successfully signed up for the API"
        }
        return jsonify(retJson)

def verifyPw(username, password):
    if not UserExist(username):
        return False

    hashed_pw = users.find({
        "Username":username
    })[0]["Password"]

    if bcrypt.hashpw(password.encode('utf8'), hashed_pw) == hashed_pw:
        return True
    else:
        return False

def generateReturnDictionary(status, msg):
    retJson = {
        "status": status,
        "msg": msg
    }
    return retJson

def verifyCredentials(username, password):
    if not UserExist(username):
        return generateReturnDictionary(301, "Invalid Username"), True

    correct_pw = verifyPw(username, password)

    if not correct_pw:
        return generateReturnDictionary(302, "Incorrect Password"), True

    return None, False


class Classify(Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData["username"]
        password = postedData["password"]
        url = postedData["url"]

        retJson, error = verifyCredentials(username, password)
        if error:
            return jsonify(retJson)

        tokens = users.find({
            "Username":username
        })[0]["Tokens"]

        if tokens<=0:
            return jsonify(generateReturnDictionary(303, "Not Enough Tokens"))
        
        if not url:
            return jsonify(({"error": "No url provided"}), 400)
        
        #Load the image from URL
        response = requests.get(url)
        print(response)
        print(response.content)
        # in-memory file of the image
        img = Image.open(BytesIO(response.content))
        # Pre-process the image
        img = img.resize((299, 299)) #resize in pixel size expected by the model
        img_array = img_to_array(img) #convert to numpay array
        img_array = np.expand_dims(img_array, axis=0) #rescale array
        img_array = preprocess_input(img_array)

        # Make the prediction
        prediction = pretrained_model.predict(img_array)
        # take top 5 predictions
        actual_prediction = imagenet_utils.decode_predictions(prediction, top=5)

        # return the classification response
        ret_json = {}
        for pred in actual_prediction[0]:
            # pred[1] = class name, pred[2] = confidence score
            ret_json[pred[1]] = float(pred[2]*100)
        
        # load the image
        # retJson = {}
        # with open('temp.jpg', 'wb') as f:
        #     f.write(response.content)
        #     # preprocess the image
        #     proc = subprocess.Popen('python classify_image.py --model_dir=. --image_file=./temp.jpg', stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        #     ret = proc.communicate()[0]
        #     proc.wait()
        #     with open("text.txt") as f:
        #         retJson = json.load(f)

        users.update({
            "Username": username
        },{
            "$set":{
                "Tokens": tokens-1
            }
        })

        return ret_json


class Refill(Resource):
    def post(self):
        # Get posted data
        postedData = request.get_json()
        # Get credentials
        username = postedData["username"]
        password = postedData["admin_pw"]
        amount = postedData["amount"]

        # check if user exists
        if not UserExist(username):
            return jsonify(generateReturnDictionary(301, "Invalid Username"))
        # check admin password
        correct_pw = "abc123"
        if not password == correct_pw:
            return jsonify(generateReturnDictionary(302, "Incorrect Password"))

        # update the token and respond
        users.update({
            "Username": username
        },{
            "$set":{
                "Tokens": amount
            }
        })
        return jsonify(generateReturnDictionary(200, "Refilled"))


api.add_resource(Register, '/register')
api.add_resource(Classify, '/classify')
api.add_resource(Refill, '/refill')

if __name__=="__main__":
    app.run(host='0.0.0.0')
