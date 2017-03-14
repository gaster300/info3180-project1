"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from forms import LoginForm, AddProfile
from models import UserProfile
import os
from datetime import date, datetime
from time import strftime
from werkzeug import secure_filename
import random


###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')

@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html')
    

@app.route('/profile', methods=["GET", "POST"])
def profile():
    form=AddProfile()
    if request.method=='POST':
        username = request.form ['username']
        id = random.randint(1000, 1099)
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        age = request.form['age']
        biography = request.form['biography']
        gender =  request.form['gender']
       
        file = request.files['image']
        image = secure_filename(file.filename)
        file.save(os.path.join("app/static/images", image))
       
        created_on= datetime.now().strftime("%a, %d %b %Y")

        profile = UserProfile (id, username, firstname, lastname, age, biography, gender, image, created_on)
        db.session.add(profile)
        db.session.commit()
        
        flash ('User ' + username + ' sucessfully added!', 'success')
        flash ('Please proceed to "Login"', 'success')
        return redirect (url_for('profile'))
   
    
    flash_errors(form)        
    return render_template('profile.html', form=form)
    
    
def flash_errors(form):
    for field, errors in form.errors.items():
        
        for error in errors:
            flash(u"Error in the %s field - %s" % (getattr(form, field).label.text,error), 'danger')

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "POST":
        # change this to actually validate the entire form submission
        # and not just one field
        if form.username.data:
            # Get the username and password values from the form.

            # using your model, query database for a user based on the username
            # and password submitted
            # store the result of that query to a `user` variable so it can be
            # passed to the login_user() method.

            # get user id, load into session
            login_user(user)

            # remember to flash a message to the user
            return redirect(url_for("home")) # they should be redirected to a secure-page route instead
    return render_template("login.html", form=form)

# user_loader callback. This callback is used to reload the user object from
# the user ID stored in the session
@login_manager.user_loader
def load_user(id):
    return UserProfile.query.get(int(id))

###
# The functions below should be applicable to all Flask apps.
###

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)
    
@app.route('/profiles',  methods=["GET", "POST"])
def listprofiles():
    display = db.session.query(UserProfile).all()
    if request.method=="POST":

        lists = []
        for user in display:
            
            lists.append({'Username': user.username,'id': user.id})
            display = {'Users': lists}
            
        return jsonify(display)
    return render_template('profile_lists.html',display=display)
    
    
@app.route('/profile/<int:id>', methods=["GET", "POST"])
def profileview(id):
     selected = db.session.query(UserProfile).filter_by(id=id).first()
     image_get = url_for('static', filename='images/'+selected.image)
     if request.method=="POST":
         return jsonify(id=selected.id, username = selected.username, image = selected.image, gender = selected.gender, age = selected.age, created_on = selected.created_on)
     else:
         selected_one = {'id':selected.id,'usern':selected.username,'image':image_get,'age':selected.age,'firstname':selected.firstname,'lastname':selected.lastname, 'created_on':selected.created_on,'gender':selected.gender,'biography':selected.biography}
         return render_template('profileview.html',selected_one=selected_one)
     
    
    
@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8080")
