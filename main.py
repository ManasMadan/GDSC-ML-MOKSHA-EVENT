from flask import Flask,jsonify,request
from level1 import similar_words

app = Flask(__name__)
 
@app.route('/')
def main():
    return jsonify({"error":False,"message":"Success"})

@app.route('/level1',methods=['POST'])
def level1():
    try:
        data = request.get_json()
        prompt = data["prompt"]
        result = similar_words(prompt, "password")
        return jsonify({"error":False,"message":"Success","result":result})
    except Exception as e:
        print(e)
        return jsonify({"error":True,"message":"Something Went Wrong","result":None})

if __name__ == '__main__':
   app.run()