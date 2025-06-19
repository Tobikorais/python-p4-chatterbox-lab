from datetime import datetime
from server.app import create_app
from server.models import db, Message

class TestMessage:
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
