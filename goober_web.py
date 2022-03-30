from distutils.log import debug
from flask import Flask, request, render_template, session, flash, redirect, url_for
from goober_database import connect_to_db, db, User
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
        
        if username and password and full_name and state:
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
        
@app.route('/lvl1')
def lvl1_page():
    return render_template('lvl1_stats.html')


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.env = "development"
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    app.run(port=5000, host='0.0.0.0')