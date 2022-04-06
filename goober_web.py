from distutils.log import debug
from flask import Flask, request, render_template, session, flash, redirect, url_for
from sqlalchemy import asc, desc
from goober_database import connect_to_db, db, User, LVL
from support import create_time, deconstruct_time
import os

app = Flask(__name__)

app.secret_key = os.environ['PASS']

@app.route('/')
def goober_home():
    return render_template("goober_web_home.html")

@app.route('/home')
def return_home():
    return render_template("goober_web_home.html")

@app.route('/login')
def login_form():
    """Show login form"""
    
    return render_template('goober_login.html')

@app.route("/login", methods=["POST"])
def process_login():
    """Log user into site."""
    
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        query = User.query
        if query.filter_by(username=f"{username}").first():
            curr_user = User.query.filter_by(username=f"{username}").one()
            if password == curr_user.password:
                session['username'] = username
                flash("Login successful!")
                return redirect(url_for('goober_home')) 
            else: 
                flash('Username or Password invalid.')
                return render_template('goober_login.html')
        else: 
            flash("Username or Password invalid.")
            return render_template('goober_login.html')
        
@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username',None)
    return redirect(url_for('goober_home'))

@app.route('/register', methods=["POST"])
def register():
    #Add a new user
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        full_name = request.form['alias']
        state = request.form['state']
        
        query = User.query
        
        #Check input fields
        if username and password and full_name and state:
            #Check if the username exists in the database
            if not query.filter_by(username=f"{username}").first():
                new_user = User(username=username,
                                password=password,
                                full_name=full_name,
                                state=state)
                
                db.session.add(new_user)
                db.session.commit()
                flash("User created successfully, you may now log in.")
                return render_template('goober_login.html')
            else:
                flash("That username is taken.")
                return render_template('goober_login.html')
            
        else:
            flash("You must fill out all fields.")
            return render_template('goober_login.html')
        
total_bacon={
        0:36,
        1:24,
        2:23,
        3:12,
        4:33,
        5:12,
        6:57,
        7:44}
lvl_names = {
        0:"Lolligagging through Liz Land",
        1:"Hopping Turtle Mountain",
        2:"Raiding the Pride",
        3:"Caverns of the Wise",
        4:"Jump, Monke! Jump!",
        5:"Ralta's Respite",
        6:"Steve",
        7:"Pincer Cape"} 
   
@app.route('/lvl/<id>')
def lvl_page(id):
    id = int(id)
    #Dictionaries for personal data table, as well as time comparisons with other players.
    user_data = {}
    user_data['total_bacon'] = total_bacon[id]
    user_data['lvl_name'] = lvl_names[id]
    
    #If the user is logged in, this fetches the best level data stored for the user.
    #These records are not matched by when they were entered, it is simply the best for each category.
    if 'username' in session:
        
        #We query the database for the user, and any level data tied to their id
        user = session['username']
        user_query = User.query.filter_by(username=f"{user}").one()
        user_data_query = LVL.query.filter_by(user_id=f"{user_query.user_id}",lvl_id=id)
        
        #Then we fill our user_data dictionary with the relevant values to be displayed in the level details corresponding.
        user_data['nickname'] = user_query.full_name
        
        for lvl_data in user_data_query:
            if not 'lvl_time' in user_data:
                user_data['lvl_time'] = create_time(lvl_data.lvl_time)
            else:
                time = create_time(lvl_data.lvl_time)
                time = deconstruct_time(time)
                if deconstruct_time(user_data['lvl_time']) > time:
                    user_data['lvl_time'] = create_time(lvl_data.lvl_time)
            
            if not 'lvl_bacon' in user_data:
                user_data['lvl_bacon'] = lvl_data.lvl_bacon
            else:
                if user_data['lvl_bacon'] < lvl_data.lvl_bacon:
                    user_data['lvl_bacon'] = lvl_data.lvl_bacon
            
            #These statements use the 1s and 0s in void egg as boolean values.
            #There is only ever one void egg per level so these statements will evaluate properly.
            if not 'lvl_void_egg' in user_data:
                user_data['lvl_void_egg'] = lvl_data.lvl_void_egg
            else:
                if not user_data['lvl_void_egg'] and lvl_data.lvl_void_egg:
                    user_data['lvl_void_egg'] = lvl_data.lvl_void_egg
      
    data = {
    'best_time': {},
    'best_time_plus_egg': {},
    'best_time_plus_breakfast': {}}
  
    time_query = LVL.query.filter_by(lvl_id=id).order_by(asc(LVL.lvl_time))
    best_time_count = 0
    while best_time_count < 9:
        for lvl_data in time_query:
            user_query = User.query.filter_by(user_id=lvl_data.user_id).first()
            
            if lvl_data.user_id in data['best_time']:
                if deconstruct_time(data['best_time'][lvl_data.user_id]['lvl_time']) > lvl_data.lvl_time:
                    data['best_time'][lvl_data.user_id]['lvl_time'] = create_time(lvl_data.lvl_time)
                    data['best_time'][lvl_data.user_id]['nickname'] = user_query.full_name
                    data['best_time'][lvl_data.user_id]['state'] = user_query.state
            else:
                data['best_time'][lvl_data.user_id] = {}
                data['best_time'][lvl_data.user_id]['lvl_time'] = create_time(lvl_data.lvl_time)
                data['best_time'][lvl_data.user_id]['nickname'] = user_query.full_name
                data['best_time'][lvl_data.user_id]['state'] = user_query.state

            best_time_count += 1
    
    best_time_plus_egg_count = 0
    egg_query = LVL.query.filter_by(lvl_id=id).filter_by(lvl_void_egg=True).order_by(asc(LVL.lvl_time))
    while best_time_plus_egg_count < 9:
        if lvl_data in egg_query:
            for lvl_data in egg_query:
                user_query = User.query.filter_by(user_id=lvl_data.user_id).first()
                
                if lvl_data.user_id in data['best_time_plus_egg']:
                    if deconstruct_time(data['best_time_plus_egg'][lvl_data.user_id]['lvl_time']) > lvl_data.lvl_time:
                        data['best_time_plus_egg'][lvl_data.user_id]['lvl_time'] = create_time(lvl_data.lvl_time)
                        data['best_time_plus_egg'][lvl_data.user_id]['nickname'] = user_query.full_name
                        data['best_time_plus_egg'][lvl_data.user_id]['state'] = user_query.state
                else:
                    data['best_time_plus_egg'][lvl_data.user_id] = {}
                    data['best_time_plus_egg'][lvl_data.user_id]['lvl_time'] = create_time(lvl_data.lvl_time)
                    data['best_time_plus_egg'][lvl_data.user_id]['nickname'] = user_query.full_name
                    data['best_time_plus_egg'][lvl_data.user_id]['state'] = user_query.state
                
                best_time_plus_egg_count += 1
        else:
            best_time_plus_egg_count += 1
            
    best_time_plus_breakfast_count = 0
    breakfast_query = LVL.query.filter_by(lvl_id=id).filter_by(lvl_void_egg=True).filter_by(lvl_bacon=total_bacon[id]).order_by(asc(LVL.lvl_time))
    print(breakfast_query)
    while best_time_plus_breakfast_count < 9:
        if lvl_data in breakfast_query:
            for lvl_data in breakfast_query:
                user_query = User.query.filter_by(user_id=lvl_data.user_id).first()
                
                if lvl_data.user_id in data['best_time_plus_breakfast']:
                    if deconstruct_time(data['best_time_plus_breakfast'][lvl_data.user_id]['lvl_time']) > lvl_data.lvl_time:
                        data['best_time_plus_breakfast'][lvl_data.user_id]['lvl_time'] = create_time(lvl_data.lvl_time)
                        data['best_time_plus_breakfast'][lvl_data.user_id]['nickname'] = user_query.full_name
                        data['best_time_plus_breakfast'][lvl_data.user_id]['state'] = user_query.state
                else:
                    data['best_time_plus_breakfast'][lvl_data.user_id] = {}
                    data['best_time_plus_breakfast'][lvl_data.user_id]['lvl_time'] = create_time(lvl_data.lvl_time)
                    data['best_time_plus_breakfast'][lvl_data.user_id]['nickname'] = user_query.full_name
                    data['best_time_plus_breakfast'][lvl_data.user_id]['state'] = user_query.state
                    
                best_time_plus_breakfast_count += 1
        else:
            best_time_plus_breakfast_count += 1
    print(data)
    
    return render_template('lvl_stats.html',
                           user_data=user_data,
                           data=data)

@app.route('/download')
def download_page():
    return render_template('download.html')

@app.route('/goober_data',methods=["POST"])
def goober_data():
    if request.method == "POST":
        data = request.values
        print(data)
        username = request.form['username']
        password = request.form['password']
        lvl = int(request.form['lvl'])
        lvl_name = request.form['lvl_name']
        lvl_time = int(request.form['lvl_time'])
        bacon_amt = int(request.form['bacon_amt'])
        if request.form['egg'] == 'True':
            egg = True
        else:
            egg = False 
        
        query = User.query
        if query.filter_by(username=f"{username}").first():
            user = query.filter_by(username=f"{username}").first()
            if user.password == password:
                lvl_data = LVL(
                            lvl_id=lvl,
                            lvl_name=lvl_name,
                            user_id=user.user_id,
                            lvl_time=lvl_time,
                            lvl_bacon=bacon_amt,
                            lvl_void_egg=egg)
                
                db.session.add(lvl_data)
                db.session.commit()
                
                return "True"
            else:
                return "That username or password did not exist."
    
    return "That username or password did not exist."

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.env = "development"
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    app.run(port=5000, host='0.0.0.0')