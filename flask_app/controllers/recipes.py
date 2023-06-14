from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import user, recipe #import entire file, rather than class, to avoid circular imports. may need to import more than one file if you have multiple tables.
import re
# Create Users Controller

@app.route ('/recipes/create/submit', methods=['POST'])
def create_recipe_submit():
    if not recipe.Recipe.validate_recipe(request.form):
        return redirect('/recipes/create')
    recipe.Recipe.create_recipe(request.form)
    return redirect('/recipes')


# Read Users Controller

@app.route ('/recipes/create')
def create_recipe():
    if 'user_id' not in session:
        return redirect('/access_denied')
    return render_template('create_recipe.html')

# Update Users Controller
@app.route('/recipes/<int:id>/edit')
def edit_recipe_page(id):
    if 'user_id' not in session:
        return redirect('/access_denied')
    single_user = user.User.get_one_recipe_by_id(id)
    single_user.recipes = single_user.recipes[0]
    date_value = single_user.recipes.date_cooked
    return render_template('edit_recipe.html', single_user=single_user, date_value=date_value)

@app.route('/recipes/<int:id>/edit/submit', methods=['POST'])
def edit_recipe(id):
    if not recipe.Recipe.validate_recipe(request.form):
        return redirect(f'/recipes/{id}/edit')
    recipe.Recipe.edit_recipe(request.form)
    return redirect('/recipes')

# Delete Users Controller
@app.route('/recipes/<int:id>/delete', methods=['POST'])
def delete_recipe(id):
    recipe.Recipe.delete_recipe_by_id(id)
    return redirect('/recipes')

# Notes:
# 1 - Use meaningful names
# 2 - Do not overwrite function names
# 3 - No matchy, no worky
# 4 - Use consistent naming conventions 
# 5 - Keep it clean
# 6 - Test every little line before progressing
# 7 - READ ERROR MESSAGES!!!!!!
# 8 - Error messages are found in the browser and terminal




# How to use path variables:
# @app.route('/<int:id>')
# def index(id):
#     user_info = user.User.get_user_by_id(id)
#     return render_template('index.html', user_info)

# Converter -	Description
# string -	Accepts any text without a slash (the default).
# int -	Accepts integers.
# float -	Like int but for floating point values.
# path 	-Like string but accepts slashes.