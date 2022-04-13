"""Models for Cupcake app."""

from filecmp import DEFAULT_IGNORES
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)


DEFAULT_IMG_URL = 'https://tinyurl.com/demo-cupcake'

class Cupcake(db.Model):
    """Cupcake model"""

    __tablename__ = 'cupcakes'

    def __repr__(self):
        c = self
        return f"<id={c.id} flavor={c.flavor} size={c.size} rating={c.rating} image={c.image}>"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    flavor = db.Column(db.Text, nullable=False)

    size = db.Column(db.Text, nullable=False)

    rating = db.Column(db.Float, nullable=False)

    image = db.Column(db.Text, nullable=False, default=DEFAULT_IMG_URL)