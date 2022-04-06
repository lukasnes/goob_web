from sqlalchemy import func
from goober_database import User, LVL, connect_to_db, db
from goober_web import app

def load_users():
    """Load users from u.user into db"""
    
    User.query.delete()
    
    for row in open("./seed_data/u.user"):
        row = row.rstrip()
        user_id, username, password, full_name, state = row.split('|')
        
        user = User(user_id=user_id,
                    username=username,
                    password=password,
                    full_name=full_name,
                    state=state)
        
        db.session.add(user)
        
    db.session.commit()
    
def load_lvls():
    """Load lvls from u.lvl into db"""
    
    LVL.query.delete()
    
    for row in open('./seed_data/u.lvl'):
        row = row.rstrip()
        lvl_id,lvl_name,user_id,lvl_time,lvl_bacon,lvl_void_egg = row.split('|')
        
        if int(lvl_void_egg):
            lvl_void_egg = True
        else:
            lvl_void_egg = False
        
        lvl = LVL(
                lvl_id=lvl_id,
                lvl_name=lvl_name,
                user_id=user_id,
                lvl_time=lvl_time,
                lvl_bacon=lvl_bacon,
                lvl_void_egg=lvl_void_egg)
        
        db.session.add(lvl)
        
    db.session.commit()
    
def set_val_user_id():
    """Set value for the next user_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(User.user_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('users_user_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()
    
if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    load_users()
    load_lvls()
    set_val_user_id()