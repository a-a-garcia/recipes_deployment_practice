
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session, request
import re
# from flask_bcrypt import Bcrypt
# bcrypt = Bcrypt(app)
# The above is used when we do login registration, be sure to install flask-bcrypt: pipenv install flask-bcrypt


class Recipe:
    db = "recipes" #which database are you using for this project
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_cooked = data['date_cooked']
        self.under_30_mins = data['under_30_mins']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None
        # What changes need to be made above for this project?
        #What needs to be added her for class association?



    # Create Users Models
    @classmethod
    def create_recipe(cls, data):
        query = """
            INSERT INTO recipe (name, description, instructions, date_cooked, under_30_mins, user_id)
            VALUES (%(name)s, %(description)s, %(instructions)s, %(date_cooked)s, %(under_30_mins)s, %(user_id)s)
        ;"""
        data = Recipe.parse_new_recipe_data(data)
        new_recipe_id = connectToMySQL(cls.db).query_db(query, data)
        return new_recipe_id
    
    @staticmethod
    def validate_recipe(recipe):
        isValid = True
        #validate recipe name
        if len(recipe['name']) < 3:
            flash('Recipe name must have at least 3 characters')
            isValid = False
        if re.search(r'\d', recipe['name']): #using build in regex function (re.search) to search for any digit (r'\d') within the user['first_name'] string
            flash('Recipe name cannot have any numbers in it.')
            isValid = False

        #validate description
        if len(recipe['description']) < 3:
            flash('Description must be at least 3 characters.')
            isValid = False
        
        #validate instructions
        if len(recipe['instructions']) < 3:
            flash('Instructions must be at least 3 characters.')
            isValid = False

        #validate date_cooked
        if len(recipe['date_cooked']) < 10:
            flash('Incorrect, incomplete or empty date input.')
            isValid = False
        if re.search(r'[a-zA-Z]', recipe['date_cooked']): 
            flash('Date cooked cannot have any letters in it.')
            isValid = False

        #validate under 30
        if not recipe.get('under_30_mins'):
            flash('Please specify if recipe can be made in under 30 mins.')
            isValid = False

        return isValid


    # Read Users Models

    # Update Users Models
    @classmethod
    def edit_recipe(cls, data):
        query = """
            UPDATE recipe
            SET name=%(name)s, description=%(description)s, instructions=%(instructions)s, date_cooked=%(date_cooked)s, under_30_mins=%(under_30_mins)s, user_id=%(user_id)s
            WHERE id = %(id)s
        ;"""
        updated_recipe = connectToMySQL(cls.db).query_db(query, data)
        return updated_recipe


    # Delete Users Models
    @classmethod
    def delete_recipe_by_id(cls, id):
        query="""
            DELETE FROM recipe
            WHERE id = %(id)s
        ;"""
        data = {'id' : id}
        deleted_recipe = connectToMySQL(cls.db).query_db(query, data)
        return deleted_recipe



    #Help funcs

    @staticmethod
    def parse_new_recipe_data(data):
        parsed_data = {
            'name' : data['name'],
            'description' : data['description'],
            'instructions' : data['instructions'],
            'date_cooked' : data['date_cooked'],
            'under_30_mins' : data['under_30_mins'],
            'user_id' : session['user_id']
        }
        return(parsed_data)