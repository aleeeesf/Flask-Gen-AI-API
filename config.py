import os
from pydantic import BaseModel, Field

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(BaseModel):
    """ Configuración de la aplicación """
    JWT_SECRET_KEY: str = Field(default="alejandro_serrano", title="JWT Secret Key for HASH")
    JWT_ACCESS_TOKEN_EXPIRES: int = Field(default=60 * 60, title="Time Token Expires")
    SQLALCHEMY_DATABASE_URI: str = Field(default='sqlite:///' + os.path.join(basedir, 'db.sqlite3'), title="Database URI")

