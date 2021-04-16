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

@app.route('/getfavorites', methods=['GET'])
def get_favorites():

    #person_id = request.json.get("person_id", None)
    #person_id_list = Favorites.query.filter_by(person_id=person_id).all()
    #allfavorite = list(map(lambda x: Favorito.serialize(x), allfavorite))

    return  jsonify(allpeople), 200


@app.route('/postfavorites', methods=['POST'])
def post_favorites():
    person_id = request.json.get("person_id")
    planet_id = request.json.get("planet_id")
    user_id = request.json.get("user_id")

    new_favorite = Favorito()
    new_favorite.person_id = person_id
    new_favorite.planet_id = planet_id
    new_favorite.user_id = user_id
    # crea registro nuevo en BBDD de 
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify({"msg": "Favorite created successfully"}), 200

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

    print(user)
    return jsonify({"id": user.id, "email": user.email}), 200
    
# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
