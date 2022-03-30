from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """Goober Web Users"""
    
    __tablename__ = "users"
    
    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(64))
    password = db.Column(db.String(64))
    full_name = db.Column(db.String(128), nullable=True)
    state = db.Column(db.String(2), nullable=True)
    
    def __repr__(self):
        return f"<User username={self.username} full_name={self.full_name} state={self.state}"
    
def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://nesit:qqq@localhost/goober_data'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)
    
if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from goober_web import app
    connect_to_db(app)
    print("Connected to DB.")