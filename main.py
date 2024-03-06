from flask import Flask, jsonify, request
from level1 import similar_words
from level_2 import Level2
from level_3 import Level3
from level_4 import runLevel
import Level5 
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/')
def main():
    return jsonify({"error": False, "message": "Success"})


@app.route('/level1', methods=['POST'])
def level1():
    try:       
        result = similar_words(request.get_json()["prompt"], "password")
        return jsonify({"error": False, "message": "Success", "result": result})
    except Exception as e:
        print(e)
        return jsonify({"error": True, "message": "Something Went Wrong", "result": None})
    
@app.route('/level2', methods=['POST'])
def level2():
    try:       
        password="AmericanPrometheus"
        x=Level2("AmericanPrometheus")
        result = ""
        if password in request.get_json()["prompt"]:
            result = "You cracked the code."          
        else :
            result = x.chat(request.get_json()["prompt"])
        return jsonify({"error": False, "message": "Success", "result": result})
    except Exception as e:
        print(e)
        return jsonify({"error": True, "message": "Something Went Wrong", "result": None})

@app.route('/level3', methods=['POST'])
def level3():
    try:
        level3Instance = Level3();    
        result = level3Instance.runChat(request.get_json()["prompt"])   
        return jsonify({"error": False, "message": "Success", "result": result})
    except Exception as e:
        print(e)
        return jsonify({"error": True, "message": "Something Went Wrong", "result": None})

@app.route('/level4', methods=['POST'])
def level4():
    try:       
        result = runLevel(request.get_json()["prompt"])   
        return jsonify({"error": False, "message": "Success", "result": result})
    except Exception as e:
        print(e)
        return jsonify({"error": True, "message": "Something Went Wrong", "result": None})

@app.route('/level5', methods=['POST'])
def level5():
    try: 
        l5 = Level5.Level("Warrior")
        result = l5.chat_start(request.get_json()["prompt"])
        return jsonify({"error": False, "message": "Success", "result": result})
    except Exception as e:
        print(e)
        return jsonify({"error": True, "message": "Something Went Wrong", "result": None})


if __name__ == '__main__':
    app.run()
