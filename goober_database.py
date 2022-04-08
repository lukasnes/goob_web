from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

class User(db.Model):
    """Goober Web Users"""
    
    __tablename__ = "users"
    
    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(64))
    password = db.Column(db.String(255))
    full_name = db.Column(db.String(128), nullable=True)
    state = db.Column(db.String(2), nullable=True)
    
    def __repr__(self):
        return f"<User user_id={self.user_id} username={self.username} full_name={self.full_name} state={self.state}>"

class LVL(db.Model):
    """Super Goober World Goober Data"""
    
    __tablename__ = 'lvl'
    
    lvl_data_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    lvl_id = db.Column(db.Integer)
    lvl_name = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    lvl_time = db.Column(db.Integer)
    lvl_bacon = db.Column(db.Integer)
    lvl_void_egg = db.Column(db.Boolean)
    
    user = db.relationship("User",
                           backref=db.backref("lvl",
                                              order_by=lvl_id))
    
    def __repr__(self):
        return f"<Data lvl_id={self.lvl_id} user_id={self.user_id} lvl_time={self.lvl_time}>"
    
def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DB_URL']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)
    
if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from goober_web import app
    connect_to_db(app)
    print("Connected to DB.")