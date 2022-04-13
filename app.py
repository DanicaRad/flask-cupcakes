"""Flask app for Cupcakes"""
from flask import Flask, request, render_template, redirect, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "Winnie"


connect_db(app)

def serialize_cupcake(cupcake):
    """Serialiaze a cupcake SQLAlchemy obj to dictionary"""

    return {
        'id': cupcake.id,
        'flavor': cupcake.flavor,
        'size': cupcake.size,
        'rating': cupcake.rating,
        'image': cupcake.image
    }

# ************* GET Routes ***************

@app.route('/')
def show_home_page():
    """Shows home page with list of all cupcakes and form to add cupcakes"""

    return render_template('add_cupcake.html')

@app.route('/api/cupcakes')
def list_all_cupcakes():
    """Returns JSON {'cupcakes': [{id, flavor, size, rating, image}... ]} for all cupcakes"""

    cupcakes = Cupcake.query.all()
    serialized = [serialize_cupcake(c) for c in cupcakes]

    return jsonify(cupcakes=serialized)

@app.route('/api/cupcakes/<int:id>')
def list_single_cupcake(id):
    """Returns JSON {'cupcake': [{id, flavor, size, rating, image}]}"""

    cupcake = Cupcake.query.get_or_404(id)
    serialized = serialize_cupcake(cupcake)

    return jsonify(cupcake=serialized)

# ************* POST Routes ***************

@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():
    """Create new cupcake from data and return it.
    
    Returns JSON {'cupcake': [{id, flavor, size, rating, image}]}"""

    new_cupcake = Cupcake(
        flavor = request.json['flavor'],
        size = request.json['size'],
        rating = request.json['rating'],
        image = request.json['image'] or None
    )

    db.session.add(new_cupcake)
    db.session.commit()

    serialized = serialize_cupcake(new_cupcake)

    return (jsonify(cupcake=serialized), 201)

# ************* PATCH Routes ***************

@app.route('/api/cupcakes/<int:id>', methods=['PATCH'])
def update_cupcake(id):
    """Update cupcake from data and return it.
    
    Returns JSON {'cupcake': [{id, flavor, size, rating, image}]}"""

    cupcake = Cupcake.query.get_or_404(id)
    # db.session.query(Cupcake).filter_by(id=id).update(request.json)

    cupcake.flavor = request.json.get('flavor', cupcake.flavor)
    cupcake.size = request.json.get('size', cupcake.size)
    cupcake.rating = request.json.get('rating', cupcake.rating)
    cupcake.image = request.json.get('image', cupcake.image)

    db.session.commit()

    serialized = serialize_cupcake(cupcake)

    return (jsonify(cupcake=serialized), 200)

# ************* DELETE Routes ***************

@app.route('/api/cupcakes/<int:id>', methods=['DELETE'])
def delete_cupcake(id):
    """Delete cupcake from db. 

    Returns JSON {message: 'deleted'}"""

    cupcake = Cupcake.query.get_or_404(id)
    db.session.delete(cupcake)
    db.session.commit()

    return (jsonify(message='Deleted'), 200)