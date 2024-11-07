from flask import Flask
from flask_cors import CORS # type: ignore

app = Flask(__name__)
CORS(app, resources={r"/members": {"origins": "http://localhost:3000"}})

@app.route("/members")
def members():
    return { "members" : ["member1", "member2", "member3"]}

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == "__main__":
    app.run(debug=True)
