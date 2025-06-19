from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
from server.extensions import db

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

class Message(db.Model, SerializerMixin):
    __tablename__ = 'messages'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
