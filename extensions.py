from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from transformers import TFGPT2LMHeadModel, GPT2Tokenizer

db = SQLAlchemy() # Base de datos
jwt = JWTManager() # JWT
tokenizer = GPT2Tokenizer.from_pretrained("gpt2") # Tokenizador de gpt2
model = TFGPT2LMHeadModel.from_pretrained("gpt2") # Modelo de gpt2