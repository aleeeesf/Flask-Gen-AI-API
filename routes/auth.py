from models import Users
from extensions import db
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint("auth", __name__)

def validate_login_data(request_json):
    """Valida los datos de login y registro"""

    username = request_json.get("username")
    password = request_json.get("password")

    if username is None or password is None:
        return jsonify({"msg": "Por favor, ingrese usuario y contraseña"}), 400
    
    if type(username) is not str or type(password) is not str:
        return jsonify({"msg": "Usuario y contraseña deben ser cadenas de texto"}), 400
    
    try:
        # Convertir a string para evitar errores de tipo
        request_json["username"] = str(username)
        request_json["password"] = str(password)

        if len(username) < 4:
            return jsonify({"msg": "El usuario debe tener al menos 4 caracteres"}), 400
    
        if len(username) > 20:
            return jsonify({"msg": "El usuario no puede tener más de 20 caracteres"}), 400
        
        if len(password) < 4:
            return jsonify({"msg": "La contraseña debe tener al menos 4 caracteres"}), 400
        
        if len(password) > 20:
            return jsonify({"msg": "La contraseña no puede tener más de 20 caracteres"}), 400 
           
    except ValueError:
        return jsonify({"msg": "Usuario y contraseña deben ser cadenas de texto"}), 400
          


@auth_bp.route("/register", methods=["POST"])
def register():
    request_json = request.get_json()
    validation = validate_login_data(request_json)
    if validation:
        return validation
    
    username = request_json.get("username")
    password = request_json.get("password")
        
    # Verificar si el usuario ya existe
    if Users.query.filter_by(username=username).first():
        return jsonify({"msg": "El usuario ya existe"}), 400
    
    password = generate_password_hash(password)    
    user = Users(username=username, password=password)
    db.session.add(user)
    db.session.commit()

    return jsonify({"msg": "Usuario creado correctamente"}), 201


@auth_bp.route("/login", methods=["GET"])
def login():
    request_json = request.get_json()   

    # Verificar los datos de entrada
    validation = validate_login_data(request_json)
    if validation:
        return validation    
    
    username = request_json.get("username")
    password = request_json.get("password")
    
    # Verificar si el usuario existe
    db_user = Users.query.filter_by(username=username).first()
    if db_user is None or not check_password_hash(db_user.password, password):
        return jsonify({"msg": "Usuario o contraseña incorrectos"}), 401

    # Crear token JWT
    access_token = create_access_token(identity=username)
    return jsonify({"access_token": access_token}), 200
