from datetime import datetime
from server.app import create_app
from server.models import db, Message

class TestApp:
    def setup_method(self, method):
        self.app = create_app()
        self.app.config['TESTING'] = True
        with self.app.app_context():
            db.create_all()
            Message.query.delete()
            db.session.commit()

    def test_has_correct_columns(self):
        with self.app.app_context():
            hello_from_liza = Message(
                body="Hello 👋",
                username="Liza")
            db.session.add(hello_from_liza)
            db.session.commit()
            assert(hello_from_liza.body == "Hello 👋")
            assert(hello_from_liza.username == "Liza")
            assert(type(hello_from_liza.created_at) == datetime)
            db.session.delete(hello_from_liza)
            db.session.commit()

    def test_returns_list_of_json_objects_for_all_messages_in_database(self):
        with self.app.app_context():
            hello_from_liza = Message(body="Hello 👋", username="Liza")
            db.session.add(hello_from_liza)
            db.session.commit()
            response = self.app.test_client().get('/messages')
            records = Message.query.all()
            for message in response.json:
                assert(message['id'] in [record.id for record in records])
                assert(message['body'] in [record.body for record in records])

    def test_creates_new_message_in_the_database(self):
        with self.app.app_context():
            self.app.test_client().post(
                '/messages',
                json={
                    "body":"Hello 👋",
                    "username":"Liza",
                }
            )
            h = Message.query.filter_by(body="Hello 👋").first()
            assert(h)
            db.session.delete(h)
            db.session.commit()

    def test_returns_data_for_newly_created_message_as_json(self):
        with self.app.app_context():
            response = self.app.test_client().post(
                '/messages',
                json={
                    "body":"Hello 👋",
                    "username":"Liza",
                }
            )
            assert(response.content_type == 'application/json')
            assert(response.json["body"] == "Hello 👋")
            assert(response.json["username"] == "Liza")
            h = Message.query.filter_by(body="Hello 👋").first()
            assert(h)
            db.session.delete(h)
            db.session.commit()

    def test_updates_body_of_message_in_database(self):
        with self.app.app_context():
            m = Message(body="Hello 👋", username="Liza")
            db.session.add(m)
            db.session.commit()
            id = m.id
            body = m.body
            self.app.test_client().patch(
                f'/messages/{id}',
                json={
                    "body":"Goodbye 👋",
                }
            )
            g = Message.query.filter_by(body="Goodbye 👋").first()
            assert(g)
            g.body = body
            db.session.add(g)
            db.session.commit()

    def test_returns_data_for_updated_message_as_json(self):
        with self.app.app_context():
            m = Message(body="Hello 👋", username="Liza")
            db.session.add(m)
            db.session.commit()
            id = m.id
            body = m.body
            response = self.app.test_client().patch(
                f'/messages/{id}',
                json={
                    "body":"Goodbye 👋",
                }
            )
            assert(response.content_type == 'application/json')
            assert(response.json["body"] == "Goodbye 👋")
            g = Message.query.filter_by(body="Goodbye 👋").first()
            g.body = body
            db.session.add(g)
            db.session.commit()

    def test_deletes_message_from_database(self):
        with self.app.app_context():
            hello_from_liza = Message(
                body="Hello 👋",
                username="Liza")
            db.session.add(hello_from_liza)
            db.session.commit()
            self.app.test_client().delete(
                f'/messages/{hello_from_liza.id}'
            )
            response = self.app.test_client().get('/messages')
            assert all(msg['body'] != "Hello 👋" or msg['username'] != "Liza" for msg in response.json)