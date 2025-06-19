from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from flask_migrate import Migrate
from datetime import datetime
from server.extensions import db
from models import Message

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.json.compact = False

    CORS(app)
    db.init_app(app)
    Migrate(app, db)

    # Add to_dict method to Message if not present
    if not hasattr(Message, 'to_dict'):
        def to_dict(self):
            return {
                "id": self.id,
                "body": self.body,
                "username": self.username,
                "created_at": self.created_at.isoformat() if self.created_at else None
            }
        Message.to_dict = to_dict

    @app.route('/messages', methods=['GET'])
    def get_messages():
        messages = Message.query.order_by(Message.created_at.asc()).all()
        return jsonify([m.to_dict() for m in messages]), 200

    @app.route('/messages', methods=['POST'])
    def post_message():
        data = request.get_json()
        try:
            new_message = Message(
                body=data['body'],
                username=data['username']
            )
            db.session.add(new_message)
            db.session.commit()
            return jsonify(new_message.to_dict()), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 400

    @app.route('/messages/<int:id>', methods=['PATCH'])
    def update_message(id):
        message = Message.query.get(id)
        if not message:
            return jsonify({'error': 'Message not found'}), 404

        data = request.get_json()
        message.body = data.get('body', message.body)
        db.session.commit()
        return jsonify(message.to_dict()), 200

    @app.route('/messages/<int:id>', methods=['DELETE'])
    def delete_message(id):
        message = Message.query.get(id)
        if message:
            db.session.delete(message)
            db.session.commit()
            return '', 204
        else:
            return {'error': 'Message not found'}, 404

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(port=5555)
