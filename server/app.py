from flask import Flask , request, jsonify ,Response
import json
from bson import json_util
from datetime import datetime

from psutil import users
import pymongo
import certifi
from bson import ObjectId
from flask_cors import CORS
import os

ca = certifi.where()

auth_json_path = os.path.join('..', 'auth.json')

#Collection Feedback
#question string
#answer string
#user_id
#hora time
connection_url=os.environ.get('MONGO_URI')

client = pymongo.MongoClient(connection_url,tlsCAFile=ca)
cliendDb = client['mystica']
col_user = cliendDb['users']
col_feedback = cliendDb['feedbacks']

app=Flask(__name__)
CORS(app)

def load_auth_data():
    with open(auth_json_path, 'r') as file:
        return json.load(file)
    
def save_auth_data(data):
    with open(auth_json_path, 'w') as file:
        json.dump(data, file, indent=4)

def findUserById(users , user_id):
    for user in users:
        if user['_id'] == user_id:
            return user['user']
    return None
## feedback


## users
@app.route('/users',methods=['POST'])
def create_user():
    try:   
        username = request.json['user']
        password = request.json['pass']
        
        existing_user_from_db = col_user.find_one({'user': username})
        if existing_user_from_db:
            return jsonify({'error': 'El usuario ya existe'}), 400
       
        existing_data = load_auth_data()
        existing_data.extend([{"user": username , "pass":password}])
    
        col_user.insert_one({'user':username , 'pass':password})
        save_auth_data(existing_data)
      
        return jsonify({'msg': 'success'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/users',methods=['GET'])
def get_users():
    try:
        users_db = col_user.find()
        users_format = []
        for user in users_db:
            user['_id'] = str(user['_id'])
            users_format.append(user)
        return jsonify(users_format)
    except Exception as e:
        return jsonify({'error':str(e)}),500

@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    user = col_user.find_one({'_id': ObjectId(id)})
    user['_id']=str(user['_id'])
    return jsonify(user)

@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
    try: 
        result = col_user.update_one({'_id':ObjectId(id)},{'$set':request.json})
        if not result.matched_count:
            return {
                "message":"Failed to update. Record is not found"
            }, 404
        users_db=col_user.find()
        users_format = []
        for item in users_db:
            item['pass']=item['pass']
            item['user']=item['user']
            users_format.append({
                'pass':item['pass'],
                'user':item['user']
            })  
        save_auth_data(users_format)
        return {"msg":"Update success"}, 200
    except Exception as e:
        return jsonify({'error':str(e)}),500

@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    col_user.delete_one({'_id': ObjectId(id)})
    users_db = col_user.find()
    users_format = []
    for item in users_db:
        item['pass']=item['pass']
        item['user']=item['user']
        users_format.append({
            'pass':item['pass'],
            'user':item['user']
        })  
    save_auth_data(users_format)
    response = jsonify({'message': 'User' + id + ' Deleted Successfully'})
    response.status_code = 200
    return response

## feedback

@app.route('/feedbacks',methods=['GET'])
def get_feedbacks():
    try:
        feedback_db = col_feedback.find()
        users_db = col_user.find()
        users_format = []
        for user in users_db:
            user['_id'] = str(user['_id'])
            users_format.append(user)

        feedback_format=[]
        for feedback in feedback_db:
            feedback['_id'] = str(feedback['_id'])
            feedback['user_id'] = str(feedback['user_id'])
            feedback['user']=findUserById(users_format,feedback['user_id'])
            feedback_format.append(feedback)
        return jsonify(feedback_format)
    except Exception as e: 
        return jsonify({'error':str(e)}),500

@app.route('/feedback/<id>', methods=['GET'])
def get_feedback(id):

    feedback = col_feedback.find_one({'_id': ObjectId(id)})
    user_id = (feedback['user_id'])
    user_db = col_user.find_one({"_id":(ObjectId(user_id))})

    feedback['_id']=str(feedback['_id'])
    feedback['user_id']=str(feedback['user_id'])
    feedback['user']=user_db['user']
    return jsonify(feedback)

@app.route('/feedbacks',methods=['POST'])
def create_feedback():
    try:

        username = request.json['username']
        answer_one = request.json['answer_one']
        answer_two = request.json['answer_two']
        answer_three= request.json['answer_three']
        hour_time = datetime.now()
        question_one = "What did you think of the Mystica IA?"
        question_two="What features would you like to have in Mystica IA?"
        question_three="What did you like most about Mystica IA?"
        
        user = col_user.find_one({'user': username})

        
        col_feedback.insert_one(
            {
             'question_one':question_one,
             'question_two':question_two,
             'question_three':question_three,
             'answer_one':answer_one , 
             'answer_two':answer_two , 
             'answer_three':answer_three,
             'hour_time':hour_time,
            'user_id':user['_id']
             })

      
        return jsonify({'msg': 'success'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def not_found(error=None):
    message = {
        'message': 'Resource Not Found ' + request.url,
        'status': 404
    }
    response = jsonify(message)
    response.status_code = 404
    return response

if __name__ == "__main__":
    app.run(debug=True, port=5001, host = "0.0.0.0")