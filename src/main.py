"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planet, Person, Favorito
import json
from json import JSONEncoder
from sqlalchemy import or_, and_
#from models import Person

#import JWT for tokenization
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, create_access_token

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# config for jwt
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")
jwt = JWTManager(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route('/planets', methods=['GET'])
def bring_planets():

    allplanets = Planet.query.all()
    allplanets = list(map(lambda x: Planet.serialize(x), allplanets))

    return  jsonify(allplanets), 200

@app.route('/people', methods=['GET'])
def bring_people():

    allpeople = Person.query.all()
    allpeople = list(map(lambda x: Person.serialize(x), allpeople))

    return  jsonify(allpeople), 200

@app.route('/addfavorites', methods=['POST'])
@jwt_required()
def post_favorites():

    current_id = get_jwt_identity()
    user = User.query.get(current_id)
    user_email = user.email

    person_name = request.json.get("person_name")
    planet_name = request.json.get("planet_name")

    new_favorite = Favorito()
    new_favorite.person_name = person_name
    new_favorite.planet_name = planet_name
    new_favorite.user_email = user_email
    # crea registro nuevo favorito
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify({"msg": "Favorite created successfully"}), 200

@app.route('/getfavorites', methods=['GET', 'POST'])
@jwt_required()
def get_favorites():

    current_id = get_jwt_identity()
    user = User.query.get(current_id)
    user_email = user.email

    allfavorites = Favorito.query.filter_by(user_email=user_email)
    allfavorites = list(map(lambda x: Favorito.serialize(x), allfavorites))

    return  jsonify(allfavorites), 200

@app.route('/delfavorites', methods=['DELETE'])
@jwt_required()
def del_favorites():

    current_id = get_jwt_identity()
    user = User.query.get(current_id)
    user_email = user.email

    person_name = request.json.get("person_name")
    planet_name = request.json.get("planet_name")
    
    if person_name is not None:
        delfavorites = Favorito.query.filter_by(user_email=user_email).filter_by(person_name=person_name).first()
        db.session.delete(delfavorites)
        db.session.commit()
        return jsonify({"msg": "Person has been deleted"}), 400
    if planet_name is not None:
        delfavorites = Favorito.query.filter_by(user_email=user_email).filter_by(planet_name=planet_name).first()
        db.session.delete(delfavorites)
        db.session.commit()
        return jsonify({"msg": "Planet has been deleted"}), 400
    if user_email is None:
        return jsonify({"msg": "Email is not valid"}), 400
    #else:
        #return jsonify({"msg": "Person or Planet is not valid"}), 400

@app.route('/register', methods=['POST'])
def register_user():
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    # valida si estan vacios los ingresos
    if email is None:
        return jsonify({"msg": "No email was provided"}), 400
    if password is None:
        return jsonify({"msg": "No password was provided"}), 400
    
    # busca usuario en BBDD
    user = User.query.filter_by(email=email).first()
    if user:
        # the user was not found on the database
        return jsonify({"msg": "User already exists"}), 401
    else:
        # crea usuario nuevo
        new_user = User()
        new_user.email = email
        new_user.password = password
        # crea registro nuevo en BBDD de 
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"msg": "User created successfully"}), 200
    
@app.route('/login', methods=['POST']) 
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    # valida si estan vacios los ingresos
    if email is None:
        return jsonify({"msg": "No email was provided"}), 400
    if password is None:
        return jsonify({"msg": "No password was provided"}), 400

    # para proteger contraseñas usen hashed_password
    # busca usuario en BBDD
    user = User.query.filter_by(email=email, password=password).first()
    if user is None:
        return jsonify({"msg": "Invalid username or password"}), 401
    else:
        # crear token
        my_token = create_access_token(identity=user.id)
        return jsonify({"token": my_token})

@app.route("/protected", methods=['GET', 'POST'])
# protege ruta con esta funcion
@jwt_required()
def protected():

    current_id = get_jwt_identity()
    user = User.query.get(current_id)
    print(user)
    return jsonify({"id": user.id, "email": user.email}), 200
    
# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
