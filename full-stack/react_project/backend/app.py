from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///users.db'
db = SQLAlchemy(app)



class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable= False)
    email = db.Column(db.String(345), nullable= False)
    password = db.Column(db.String())

    def to_user(self):
        return {
            'id' : self.id,
            'name' : self.name,
            'email' : self.email,
            'password' : self.password
        }



with app.app_context():
    db.create_all()

@app.route('/register', methods=['POST'])
def register_user():
    data = request.json
    if 'name' not in data or 'email' not in data or 'password' not in data:
        return jsonify({
            'Message' : 'Missing Information, Please Verify again'
        }), 401
    
    user1 = db.session.query(Users).filter_by(email = data['email']).first()
    if user1:
        return jsonify({
            'Message' : 'User Already Exists'
        }), 403
    
    user = Users(
        name=data['name'],
        email= data['email'],
        password = data['password']
    )
    db.session.add(user)
    db.session.commit()

    return jsonify({
        'Message' : 'User Created Successfuly'
    }), 201

@app.route('/login', methods=['POST'])
def login_user():
    data = request.json
    print("Hello")
    print(data)
    if 'email' not in data or 'password' not in data:
        return jsonify({
            'Message' : 'Missing Information, Please Verify again'
        }), 401
    
    user = db.session.query(Users).filter_by(email=data['email']).first()
    print(user)
    if user and user.password == data['password']:
        return jsonify({
            'Message' : 'User Info Verified'
        }), 200

    else:
        return jsonify({
            'Message' : 'No user found'
        }), 404


if __name__ == '__main__':
    app.run(debug=True)
