from extensions import db
from datetime import datetime, timezone

class Users(db.Model):
    """ Modelo de usuario para almacenar en la base de datos """
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"Usuario {self.username}>"
    
class Messages(db.Model):
    """ Modelo de mensaje para almacenar en la base de datos """
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    message = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    

    def __repr__(self):
        return f"Mensaje {self.message}>"