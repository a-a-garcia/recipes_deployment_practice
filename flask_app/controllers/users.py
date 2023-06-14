from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models import user, recipe #import entire file, rather than class, to avoid circular imports. may need to import more than one file if you have multiple tables.

# Create Users Controller
@app.route('/register', methods=["POST"])
def create_user():
    if not user.User.validate_user(request.form):
        return redirect('/register')
    user.User.create_user(request.form)
    return redirect('/recipes')


# Read Users Controller

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/access_denied')
def deny_access():
    return render_template('access_denied.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/recipes')
def display_recipes_page():
    if 'user_id' not in session:
        return redirect('/access_denied')
    all_recipes = user.User.show_all_recipes()
    print(session)
    return render_template('recipes.html', all_recipes=all_recipes)

@app.route('/recipes/<int:id>')
def show_single_user_with_recipe_by_id(id):
    if 'user_id' not in session:
        return redirect('/access_denied')
    single_user = user.User.get_one_recipe_by_id(id) #this returns that data dictionary, but you cannot access the associated class list by just doing {{single_user.name}} even if the print statement seems to indicate otherwise. more below
    single_user.recipes = single_user.recipes[0]
    return render_template('view_recipe.html', single_user=single_user)

    #when you call get_one_recipe_by_id, it constructs a user_with_recipe object with a list of one recipe, but this object itself only has the attributes of a User
    #the 'name', 'description' etc.. attributes belong to the RECIPE, NOT the User.
    #hence, line 21. initialize a variable that allows you to go into the list of one recipe, and display it in the template.


@app.route('/login', methods=['POST'])
def login():
    if not user.User.parse_login_data(request.form):
        return redirect('/')
    return redirect('/recipes')

@app.route('/logout')
def logout():
    session.clear()
    return render_template('/login.html')

# Update Users Controller



# Delete Users Controller


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