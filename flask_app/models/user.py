
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session, request
from flask_app.models import recipe # doing class association properly....
import re
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
# The above is used when we do login registration, be sure to install flask-bcrypt: pipenv install flask-bcrypt


class User:
    db = "recipes" #which database are you using for this project
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.recipes = []
        # What changes need to be made above for this project?
        #What needs to be added her for class association?



    # Create Users Models
    @classmethod
    def create_user(cls, form_data):
        if not cls.validate_user(form_data):
            return False
        form_data = form_data.copy()
        form_data['password'] = bcrypt.generate_password_hash(form_data['password'])
        query="""
            INSERT INTO user (first_name, last_name, email, password)
            VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)
        ;"""
        new_users_id = connectToMySQL(cls.db).query_db(query, form_data)
        session['user_id'] = new_users_id
        session['user_first_name'] = f"{form_data['first_name']}"
        session['user_last_name'] = f"{form_data['last_name']}"
        return new_users_id
    
    @staticmethod
    def validate_user(user):
        isValid = True
        #validate first name
        if len(user['first_name']) < 2:
            flash('First name must be at least 2 characters.')
            isValid = False
        if re.search(r'\d', user['first_name']): #using build in regex function (re.search) to search for any digit (r'\d') within the user['first_name'] string
            flash('First name cannot have any numbers in it.')
            isValid = False

        #validate last name
        if len(user['last_name']) < 2:
            flash('Last name must be at least 2 characters.')
            isValid = False
        if re.search(r'\d', user['last_name']): #using build in regex function (re.search) to search for any digit (r'\d') within the user['last_name'] string
            flash('Last name cannot have any numbers in it.')
            isValid = False
        
        #validate email
        if len(user['email']) < 7: #email must be at least 7 chars - a@b.com
            flash('Please enter a valid email address.')
            isValid = False
        if not re.search(r'\d', user['password']):
            flash('Password must contain at least ONE (1) number.')
            isValid = False
        if not re.search(r'[A-Z]', user['password']):
            flash('Password must have at least ONE (1) uppercase letter.')
            isValid = False
        else:
            EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') #email must have email expected characters
            if not EMAIL_REGEX.match(user['email']):
                flash('You must use the correct email format, ie name@email.com.')
                isValid = False
            else: #query db to check if email exists already
                query = """
                    SELECT * FROM user
                    WHERE email = %(email)s
                ;"""
                data = {'email':user['email']}
                email_exists = connectToMySQL('recipes').query_db(query,data) # MAKE SURE YOU CHANGE THE DB HERE!
                if email_exists:
                    flash('Email is already registered and in use.')
                    isValid = False
    
        #validate password
        if len(user['password']) < 8:
            flash('Password must be at least 8 characters long.')
            isValid = False
        if request.form['password'] != request.form['confirm_password']:
            flash('Password fields do not match.')
            isValid = False
    
        return isValid

    @classmethod
    def get_user_by_id(cls, id):
        query ="""
            SELECT * from user
            WHERE id = %(id)s
        """
        data = {'id' : id}
        user_by_id = connectToMySQL(cls.db).query_db(query, data)
        return cls(user_by_id[0])
    

    # Read Users Models
    @classmethod
    def get_user_by_email(cls, email):
        query ="""
            SELECT * FROM user
            WHERE email = %(email)s
        ;"""
        data = {'email' : email}
        user_by_email = connectToMySQL(cls.db).query_db(query, data)
        if user_by_email:
            return cls(user_by_email[0])
        return None
    
    @classmethod
    def get_one_recipe_by_id(cls, id):
        query = """
            SELECT *
            FROM user
            JOIN recipe ON user.id = recipe.user_id
            WHERE recipe.id = %(id)s
        ;"""
        data = {'id': id}
        results = connectToMySQL(cls.db).query_db(query, data) #from here onwards, we're doing class association, in our model, associating a user with a recipe
        print (results)
        user_with_recipe = cls(results[0]) # initializing a vairable, that will hold the query - a user and recipe table joined where recipe id is equal to whatever is passed in
        for row_from_db in results: #for each dictionary in the list of results...
            recipe_data = {
                'id' : row_from_db['recipe.id'],
                'name' : row_from_db['name'],
                'description'  : row_from_db['instructions'],
                'date_cooked' : row_from_db['date_cooked'],
                'instructions' : row_from_db['instructions'],
                'under_30_mins' : row_from_db['under_30_mins'],
                'created_at' : row_from_db['created_at'],
                'updated_at' : row_from_db['updated_at']
            }
            user_with_recipe.recipes.append(recipe.Recipe(recipe_data)) # 1. take that dictionary with the query result and.. 2. inside of the init attribute that it has - self.recipes... 3. go into the recipe file.. 4. go into the recipe class.. 5. create an instance of a recipe with the recipe_data data dictionary.
        print (user_with_recipe)
        return(user_with_recipe)


    @classmethod
    def parse_login_data(cls, form_data):
        this_user = User.get_user_by_email(form_data['email'])
        if this_user:
            if bcrypt.check_password_hash(this_user.password, form_data['password']):
                session['user_id'] = this_user.id
                session['user_first_name'] = this_user.first_name
                session['user_last_name'] = this_user.last_name
                return True
        flash('Invalid email or password.')
        return False
    
    @classmethod
    def show_all_recipes(cls):
        query="""
            select recipe.id, user_id, name, under_30_mins, first_name, last_name from user
            join recipe
            on user.id = recipe.user_id
        ;"""
        all_recipes = connectToMySQL(cls.db).query_db(query)
        return(all_recipes)

    # Update Users Models



    # Delete Users Models