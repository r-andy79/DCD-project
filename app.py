import os
import datetime
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

@app.route('/add_recipe', methods=['GET', 'POST'])
def add_recipe():
  if request.method =='POST':
    form = request.form.to_dict()
    # currentDate = datetime.datetime.now()
    recipes = recipes_collection
    recipes.insert_one(
      {
        'name': form['name'],
        'author': form['author'],
        'cuisine': form['cuisine'],
        'allergens': form['allergens'],
        'ingredients': (form['ingredients'].split(',')),
        'preparation': form['preparation'],
        'like': bool('false'),
        'votes': int('0'),
        'date_added': datetime.datetime.now()
      }
    )
  return render_template('add_recipe.html')

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
      flash("Passwords do not match")

  return render_template('register.html')

# user login
@app.route('/login')
def login():

  return render_template('login.html')



