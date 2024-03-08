from flask import Flask, jsonify, request
from level1 import similar_words
from level_2 import Level2
from level_3 import Level3
from level_4 import runLevel
import Level5
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
from functools import wraps
import json
from datetime import datetime, timedelta, timezone
import jwt
from firebase_admin import firestore


cred = credentials.Certificate("admin-sdk.json")
firebase_admin.initialize_app(cred)
app = Flask(__name__)
CORS(app, supports_credentials=True)
JWT_SECRET = 'wsdkOIWrfhnNDMIOPKWFdmSDMFOUbnWS'


def getRemainingTime(iat_timestamp):
    print(iat_timestamp)
    print(type(iat_timestamp))
    # Get the current time
    current_time = datetime.utcnow()

    # Convert `iat` timestamp to a datetime object
    iat_datetime = datetime.utcfromtimestamp(iat_timestamp)

    # Calculate the difference
    time_difference = current_time - iat_datetime

    # Get the difference in minutes and seconds
    minutes_difference = time_difference.total_seconds() // 60
    seconds_difference = time_difference.total_seconds() % 60

    return (f"{int(minutes_difference)} : {int(seconds_difference)} seconds")

# Function to serialize datetime objects to string

def saveLevelPrompts(level,user_id,result):
    try:
        db = firestore.client()
        user_ref = db.collection('users').document(user_id)
        data_ref = db.collection('users').document(user_id).get().to_dict()        
        data_ref[f'level{level}Prompts'] += 1        
        user_ref.set(data_ref)
        return jsonify({"error": False, "message": "Success", "result": result}), 200
    except Exception as e:
        return jsonify({"error": True, "message": str(e), "result": "Error"}), 401
    
def saveLevelCompleted(level,user_id):
    try:
        db = firestore.client()
        user_ref = db.collection('users').document(user_id)
        data_ref = db.collection('users').document(user_id).get().to_dict()
        data_ref[f'level{level}Time'] = getRemainingTime(request.session_data['iat'])
        user_ref.set(data_ref)
        return jsonify({"error": False, "message": "Success", "result": "Level Cleared"}), 200
    except Exception as e:
        return jsonify({"error": True, "message": str(e), "result": "Error"}), 401


def serialize_datetime(dt):
    if isinstance(dt, datetime.datetime):
        return dt.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    return dt

# Authentication decorator


def authenticate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization', '').split('Bearer ')[-1]
        if not token:
            return jsonify({"error": True, "message": "Missing Firebase Token", "result": "Error"}), 401
        try:
            decoded_token = auth.verify_id_token(token)
            request.user_id = decoded_token['uid']
            request.user_email = decoded_token['email']
        except auth.InvalidIdTokenError:
            return jsonify({"error": True, "message": "Invalid Firebase Token", "result": "Error"}), 401
        return func(*args, **kwargs)
    return wrapper

# JWT token verification decorator


def verify_jwt_token(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get('Session', '').split('Bearer ')[-1]
        if not token:
            return jsonify({"error": True, "message": "Missing Session Token", "result": "Error"}), 401
        try:
            decoded_token = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
            request.session_data = decoded_token
        except Exception as e:
            return jsonify({"error": True, "message": str(e), "result": "Error"}), 401
        return func(*args, **kwargs)
    return wrapper


@app.route('/')
def main():
    return jsonify({"error": False, "message": "Success"})


@app.route('/createSession', methods=['POST'])
@authenticate
def create_session_token():
    try:
        db = firestore.client()
        user_ref = db.collection('users').document(request.user_id)

        if not user_ref.get().exists:
            expiration = datetime.now(timezone.utc) + timedelta(hours=30)
            message = {
                'iss': 'https://example.com/',
                'sub': request.user_email,
                'user_id': request.user_id,
                'iat': int(datetime.now(timezone.utc).timestamp()),
                'exp': int(expiration.timestamp()),
            }
            # Create JWT session token
            session_token = jwt.encode(message, JWT_SECRET, algorithm='HS256')
            
            user_ref.set({
                'Email': request.user_email,
                'level1Prompts': 0,
                'level1Time': 'Nan',
                'level2Prompts': 0,
                'level2Time': 'Nan',
                'level3Prompts': 0,
                'level3Time': 'Nan',
                'level4Prompts': 0,
                'level4Time': 'Nan',
                'level5Prompts': 0,
                'level5Time': 'Nan',
                'SessionToken': session_token
            })       
            
            return jsonify({'session_token': session_token}), 200
        else:
            return jsonify({'session_token': user_ref.get().to_dict()["SessionToken"]}), 200
    except Exception as e:
        return jsonify({"error": True, "message": str(e), "result": "Error"}), 401


@app.route('/getLeaderBoard')
def leaderBoard():
    try:
        db = firestore.client()
        users_ref = db.collection('users')
        all_users = [doc.to_dict() for doc in users_ref.stream()]
        return jsonify(all_users), 200
    except Exception as e:
        return jsonify({"error": True, "message": str(e), "result": "Error"}), 401


@app.route('/level1', methods=['POST'])
@verify_jwt_token
def level1():
    try:
        if (request.get_json()["prompt"].lower() != "password"):
            result = similar_words(request.get_json()["prompt"], "password")            
            return saveLevelPrompts(1,request.session_data["user_id"],result)
        else:            
            return saveLevelCompleted(1,request.session_data["user_id"])
    except Exception as e:
        print(e)
        return jsonify({"error": True, "message": "Something Went Wrong", "result": str(e)})


@app.route('/level2', methods=['POST'])
@verify_jwt_token
def level2():
    try:
        if (request.get_json()["prompt"].lower() != "americanprometheus"):
            password = "AmericanPrometheus"
            x = Level2(password)
            result = ""
            """ if password in request.get_json()["prompt"]:
                result = "You cracked the code."
            else:
                result = x.chat(request.get_json()["prompt"]) """
            result = x.chat(request.get_json()["prompt"])
            return saveLevelPrompts(2,request.session_data["user_id"],result)
        else:
            return saveLevelCompleted(2,request.session_data["user_id"])
    except Exception as e:
        print(e)
        return jsonify({"error": True, "message": "Something Went Wrong", "result": None})


@app.route('/level3', methods=['POST'])
@verify_jwt_token
def level3():
    try:
        if (request.get_json()["prompt"].lower() != "dodo"):
            level3Instance = Level3()
            result = level3Instance.runChat(request.get_json()["prompt"])
            return saveLevelPrompts(3,request.session_data["user_id"],result)
        else:
            return saveLevelCompleted(3,request.session_data["user_id"])
    except Exception as e:
        print(e)
        return jsonify({"error": True, "message": "Something Went Wrong", "result": None})


@app.route('/level4', methods=['POST'])
@verify_jwt_token
def level4():
    try:
        if (request.get_json()["prompt"].lower() != "2345jkl"):
            result = runLevel(request.get_json()["prompt"])
            return saveLevelPrompts(4,request.session_data["user_id"],result)
        else:
            return saveLevelCompleted(4,request.session_data["user_id"])
    except Exception as e:
        print(e)
        return jsonify({"error": True, "message": "Something Went Wrong", "result": None})


@app.route('/level5', methods=['POST'])
@verify_jwt_token
def level5():
    try:
        if (request.get_json()["prompt"].lower() != "warrior"):
            l5 = Level5.Level("Warrior")
            result = l5.chat_start(request.get_json()["prompt"])
            return saveLevelPrompts(5,request.session_data["user_id"],result)
        else:
            return saveLevelCompleted(5,request.session_data["user_id"])
    except Exception as e:
        print(e)
        return jsonify({"error": True, "message": "Something Went Wrong", "result": None})


if __name__ == '__main__':
    app.run()
