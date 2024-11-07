from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///items.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200))

    def to_dict(self):
        return{
            'id': self.id,
            'name': self.name,
            'description': self.description
        }


with app.app_context():
    # This creates all tables defined in the models if they don't exist
    db.create_all()

    # Sample data to insert
    items = [
        Item(name="Laptop", description="A high-performance laptop for gaming and work"),
        Item(name="Smartphone", description="A smartphone with a great camera and fast processor"),
        Item(name="Headphones", description="Noise-canceling over-ear headphones"),
        Item(name="Monitor", description="4K resolution monitor for professional use"),
        Item(name="Keyboard", description="Mechanical keyboard with RGB lighting"),
    ]

    # Insert data into the database
    for item in items:
        db.session.add(item)
    db.session.commit()

@app.route('/items', methods=['GET'])
def get_item():
    items = Item.query.all()
    return jsonify([item.to_dict() for item in items])

@app.route('/items', methods=['POST'])
def add_item():
    req = request.json
    name = req.get('name')
    desc = req.get('description')
    ite = Item(id, name, desc)
    db.session.add(ite)
    db.session.commit()
    return jsonify(ite.to_dict()), 201


if __name__ == "__main__":
    app.run(debug=True)

    