from extensions import db, tokenizer, model
from models import Messages, Users
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

chat_bp = Blueprint("chat", __name__)

def initialize_params(request_json):    
    request_json["message"]         = request_json.get("message")
    request_json["max_length"]      = request_json.get("max_length", 50)
    request_json["temperature"]     = request_json.get("temperature", 0.7)
    request_json["top_k"]           = request_json.get("top_k", 0)
    request_json["top_p"]           = request_json.get("top_p", 1.0)    

    return request_json


def validate_message_params(request_json):
    """Valida los parámetros de entrada y convierte los valores a los tipos correctos"""
    if not request_json["message"]:
        return jsonify({"message": "No se proporcionó un mensaje"}), 400
    
    try:
        request_json["message"] = str(request_json["message"])
        if len(request_json["message"]) < 1 or len(request_json["message"]) > 100:
            return jsonify({"message": "message debe tener entre 1 y 100 caracteres"}), 400
    except ValueError:
        return jsonify({"message": "message debe ser una cadena de texto"}), 400
    
    try:
        request_json["max_length"] = int(request_json["max_length"])
        if request_json["max_length"] < 1 or request_json["max_length"] > 100:
            return jsonify({"message": "max_length debe estar entre 1 y 100"}), 400
    except ValueError:
        return jsonify({"message": "max_length debe ser un entero"}), 400
        
    try:
        temperature = float(request_json["temperature"])
        if temperature < 0.0 or temperature > 1.0:
            return jsonify({"message": "temperature debe estar entre 0 y 1"}), 400
    except ValueError:
        return jsonify({"message": "temperature debe ser un flotante"}), 400
    
    try:
        request_json["top_k"] = int(request_json["top_k"])
        if request_json["top_k"] < 0 or request_json["top_k"] > 100:
            return jsonify({"message": "top_k debe ser un entero positivo"}), 400
    except ValueError:
        return jsonify({"message": "top_k debe ser un entero"}), 400
    
    try:
        request_json["top_p"] = float(request_json["top_p"])
        if request_json["top_p"] < 0.0 or request_json["top_p"] > 1.0:
            return jsonify({"message": "top_p debe estar entre 0 y 1"}), 400
    except ValueError:
        return jsonify({"message": "top_p debe ser un flotante"}), 400
    
    return None



@chat_bp.route("/chat", methods=["GET"])
@jwt_required()  
def chat():
    usuario_actual = get_jwt_identity()

    request_json = initialize_params(request.json)    
    if error := validate_message_params(request_json):
        return error
    
    user_message = request_json["message"]
    max_length = request_json["max_length"]
    temperature = request_json["temperature"]
    top_k = request_json["top_k"]
    top_p = request_json["top_p"]
    
    user_message = str(user_message)
    user_id = Users.query.filter_by(username=usuario_actual).first().id

    tokenizer.pad_token = tokenizer.eos_token
    inputs = tokenizer(user_message, return_tensors="tf", padding=True, truncation=True)
    output = model.generate(inputs["input_ids"], attention_mask=inputs["attention_mask"], pad_token_id=tokenizer.pad_token_id, 
                            max_length=max_length, temperature=temperature, top_k=top_k, top_p=top_p, do_sample=True)
    generated_text = tokenizer.batch_decode(output)[0]

    user_message = Messages(
        message=user_message,
        role="HumanMessage",
        user_id=user_id,
    )
    ai_message = Messages(
        message=generated_text,
        role="AIMessage",
        user_id=user_id,
    )   

    db.session.add(user_message)
    db.session.add(ai_message)
    db.session.commit()
    return jsonify({"generated_text": generated_text})


@chat_bp.route("/history", methods=["GET"])
@jwt_required()  
def historial():
    usuario_actual = get_jwt_identity()
    limit = request.args.get("limit", 10)
    
    # Validar el parámetro limit
    try:
        limit = int(limit)
        if limit < 1 or limit > 100:
            return jsonify({"message": "limit debe estar entre 1 y 100"}), 400
    except ValueError:
        return jsonify({"message": "limit debe ser un entero"}), 400


    user_id = Users.query.filter_by(username=usuario_actual).first().id
    messages = Messages.query.filter_by(user_id=user_id).order_by(Messages.created_at.desc()).limit(limit).all()
    return jsonify([{"role": message.role, "message": message.message} for message in messages])