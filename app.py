from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messages.db'
db = SQLAlchemy(app)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(200), nullable=False)
    username = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/messages', methods=['POST'])
def add_message():
    body = request.json.get('body')
    username = request.json.get('username')
    if not body or not username:
        return {'error': 'Body and username are required'}, 400
    new_message = Message(body=body, username=username)
    db.session.add(new_message)
    db.session.commit()
    return {
        'id': new_message.id,
        'body': new_message.body,
        'username': new_message.username,
        'created_at': new_message.created_at.isoformat()
    }, 201

@app.route('/messages', methods=['GET'])
def get_messages():
    messages = Message.query.all()
    return jsonify([
        {
            'id': msg.id,
            'body': msg.body,
            'username': msg.username,
            'created_at': msg.created_at.isoformat()
        } for msg in messages
    ]), 200

@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    message = Message.query.get(id)
    if not message:
        return {'error': 'Message not found'}, 404
    body = request.json.get('body')
    if body:
        message.body = body
    db.session.commit()
    return {
        'id': message.id,
        'body': message.body,
        'username': message.username,
        'created_at': message.created_at.isoformat()
    }, 200

@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = Message.query.get(id)
    if message:
        db.session.delete(message)
        db.session.commit()
        return '', 204
    else:
        return {'error': 'Message not found'}, 404

if __name__ == '__main__':
    app.run(debug=True)