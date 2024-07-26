"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""

import os
from datetime import datetime
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User,Planet,Favorite,Character
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# get all people
@app.route('/character/', methods=['GET'])
def get_all_characters():
    #realizo la consulta para obtener todos los personajes
    result_query=Character.query.all()
     #valido si obtengo los personajes
    if result_query :
        #serializo los personajes obtenidos de la consulta
        characters_serialized= list(map(lambda item: item.serialize(), result_query))
    else:
        return jsonify({'msg ': " no hay personajes...."}),404
    #preparo el mensaje de respuesta y muestro los personajes obtenidos serializados
    response_body = {
        "msg": "character received, ok ",
        "results": characters_serialized
    }
    #muestro la respuesta al usuario con el codigo correspondiente de respuesta.
    return jsonify(response_body), 200

# get one people
@app.route('/character/<int:id>', methods=['GET'])
def get_character(id):
    #consulto por id a mi tabla de personajes, y busco la primera coincidencia
    result_query=Character.query.filter_by(id_character=id).first()  
    
    response_body = {
        "msg": "character received, ok",
        #devuelto el personaje serializado
        "results":result_query.serialize()
    }    
    
    if result_query:
        return jsonify(response_body), 200
    else:
        return jsonify({"error":"No se encontro el personaje"}), 404
# get all planet
@app.route('/planet/', methods=['GET'])
def get_all_planets():

    result_query=Planet.query.all()
    print(result_query)
    
    if result_query :
        planet_serialized= list(map(lambda item: item.serialize(), result_query))
    else:
        return jsonify({'msg ': " no hay planetas...."}),404
    
    response_body = {
        "msg": "planets received, ok ",
        "results": planet_serialized
    }

    return jsonify(response_body), 200

# get one planet
@app.route('/planet/<int:id>', methods=['GET'])
def get_planet(id):

    result_query=Planet.query.filter_by(id_planet=id).first()
    print(result_query)   
    
    response_body = {
        "msg": "planet received, ok",
        "results":result_query.serialize()
    }    
    
    if result_query:
        return jsonify(response_body), 200
    else:
        return jsonify({"error":"No se encontro el planet"}), 404

# get all user
@app.route('/user/', methods=['GET'])
def get_all_users():

    result_query=User.query.all()
    print(result_query)
    
    if result_query :
        users_serialized= list(map(lambda item: item.serialize(), result_query))
    else:
        return jsonify({'msg ': " no hay usuarios...."}),404
    
    response_body = {
        "msg": "user received, ok ",
        "results": users_serialized
    }

    return jsonify(response_body), 200
    
# get all favorites user
@app.route('/users/<int:user_id>/favorites', methods=['GET'])
def get_favorites_user(user_id):
    
    result_query= User.query.get(user_id)
    #verifico si obtengo/encuentro al usuario en mi tabla de favoritos
    if result_query.favorite:
        #si lo obtengo/encuentro traigo los favoritos serializados del usuario...
        user_favorites_serialized= list(map(lambda favorite: favorite.serialize(),result_query.favorite))    
    else:
        return jsonify({'msg': "Usuario no encontrado"}), 404
    
    response_body = {
        "msg": "user received, ok ",
        "results": user_favorites_serialized
    }

    return jsonify(response_body), 200

# post add planet user   
@app.route('/favorite/user/<int:user_id>/planet/<int:planet_id>', methods=['POST'])
def add_planet_user(user_id,planet_id):

    capture_id_user=User.query.get(user_id)
    capture_id_planet=Planet.query.get(planet_id)
    
    if not capture_id_user:
         return jsonify({'msg': "Usuario no encontrado"}), 404
    if not capture_id_planet:
        return jsonify({'msg': "Planeta no encontrado"}), 404
    
    new_favorite_planet= Favorite(user_id=capture_id_user.id_user, planet_id=capture_id_planet.id_planet)   
    
    db.session.add(new_favorite_planet) 
    db.session.commit()

    response_body= {

       "msg": "planet added favorite user,ok",
        "favorite_planet_user": new_favorite_planet.serialize()
    }
    return jsonify(response_body),200

# post add character user   
@app.route('/favorite/user/<int:user_id>/character/<int:character_id>', methods=['POST'])
def add_character_user(user_id,character_id):

    capture_id_user=User.query.get(user_id)
    capture_id_character=Character.query.get(character_id)
    
    if not capture_id_user:
         return jsonify({'msg': "Usuario no encontrado"}), 404
    if not capture_id_character:
        return jsonify({'msg': "Personaje no encontrado"}), 404
    
    new_favorite_character= Favorite(user_id=capture_id_user.id_user, character_id=capture_id_character.id_character)   
    
    db.session.add(new_favorite_character) 
    db.session.commit()

    response_body= {

       "msg": "character added favorite user,ok",
        "favorite_planet_user": new_favorite_character.serialize()
    }
    return jsonify(response_body),200

# delete planet favorite user
@app.route('/favorite/user/<int:user_id>/planet/<int:planet_id>', methods=['DELETE'])
def delete_planet_user(user_id,planet_id):
    
    planet_user= Favorite.query.filter_by(user_id=user_id,planet_id=planet_id).first()
    
    if planet_user == None:
        return jsonify({'msg': "Planeta no eliminado"}), 404
    else:
        db.session.delete(planet_user)
        db.session.commit()
        return jsonify({"msg": "Planeta eliminado de favoritos..."}),200

# delete character favorite user
@app.route('/favorite/user/<int:user_id>/character/<int:character_id>', methods=['DELETE'])
def delete_character_user(user_id,character_id):
    
    character_user= Favorite.query.filter_by(user_id=user_id,character_id=character_id).first()
    
    if character_user == None:
        return jsonify({'msg': "El Personaje nose ha podido eliminar"}), 404
    else:
        db.session.delete(character_user)
        db.session.commit()
        return jsonify({"msg": "Personaje eliminado de favoritos..."}),200
# this only runs if `$ python src/app.py` is executed

# post user, no corresponde a este proyecto, es de prueba....
@app.route('/user/', methods=['POST'])
def post_user():

    data_user=request.get_json()

    if not isinstance(data_user["name"], str):
        return jsonify({"error": "'name' debe contener un valor/o ser una cadena"}), 400
    if not isinstance(data_user["last_name"], str):
        return jsonify({"error": "'last name' debe ser una cadena/no puede quedar vacia"}), 400
    if not isinstance(data_user["email"], str):
        return jsonify({"error": "'email' debe ser una cadena/no puede quedar vacia"}), 400
    if not isinstance(data_user["password"],str):
        return jsonify({"error": "'password' no puede quedar vacia"}), 400
    if not isinstance(data_user["is_active"],bool): 
        return jsonify({"error": "'is_active' no se puede dejar sin seleccion"}), 400   
    if not isinstance(data_user["date_of_suscription"],str):     
        return jsonify({"error": "'date_of_suscription' debe seleccionar la fecha de suscripcion"}), 400
    
    try:
        date_of_suscription = datetime.strptime(data_user['date_of_suscription'], "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"error": "'date_of_suscription' debe estar en formato YYYY-MM-DD"}), 400
    
    new_user= User(
     name= data_user["name"],   
     last_name= data_user["last_name"],
     email= data_user["email"],   
     password= data_user["password"],   
     is_active= data_user["is_active"],
     date_of_suscription= data_user["date_of_suscription"]   
    )
    
    db.session.add(new_user) 
    db.session.commit()

    response_body= {

       "msg": "user created,ok",
        "user": new_user.serialize()
    }
    return jsonify(response_body),200

# get one user, no corresponde a este proyecto, es de prueba.
@app.route('/user/<int:id>', methods=['GET'])
def get_user(id):

    result_query=User.query.filter_by(id_user=id).first()
    print(result_query)   
    
    response_body = {
        "msg": "user received, ok",
        "results":result_query
    }    
    
    if result_query:
        return jsonify(response_body), 200
    else:
        return jsonify({"error":"No se encontro el miembro"}), 400

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
