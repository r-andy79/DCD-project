import os
from flask import Flask, render_template, redirect, request, url_for, flash, session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)


mongo = PyMongo(app)

users_collection = mongo.db.users
recipes_collection = mongo.db.recipes

@app.route('/')
@app.route('/get_recipes')
def get_recipes():
  return render_template('recipes.html', recipes=recipes_collection.find())

# user registration
@app.route('/register', methods=['GET', 'POST'])
def register():
  if request.method =='POST':
    form = request.form.to_dict()
    if form['password'] == form['password1']:
      user = users_collection.find_one({'username' : form['username']})
      if user:
        flash("User already exists", "warning")
        return redirect(url_for('register'))
      else:
        hash_password = generate_password_hash(form['password'])
        users_collection.insert_one(
          {
            'username': form['username'],
            'email': form['email'],
            'password': hash_password,
            'recipes': [],
            'votes': 0
          }
        )
        flash("Your account has been created.", "success")
    else:
      flash("Passwords do not match", "warning")

  return render_template('register.html')

# user login
@app.route('/login')
def login():

  return render_template('login.html')



