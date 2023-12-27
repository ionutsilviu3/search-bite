from dataclasses import dataclass
from flask import Flask, jsonify, request, session
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import psycopg2
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

app = Flask(__name__)
CORS(app, origins="http://localhost:3000")

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/search-bite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['RECIPE_UPLOAD_FOLDER'] = '/uploads/ingredients'
app.config['INGREDIENT_UPLOAD_FOLDER'] = '/uploads/recipes'

db = SQLAlchemy(app)

app.app_context().push()


class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    # image_path = db.Column(db.String(255), unique=True)
    recipes_ingredients = db.relationship(
        'RecipesIngredients', back_populates='ingredient')


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    # image_path = db.Column(db.String(255), unique=True)
    recipes_ingredients = db.relationship(
        'RecipesIngredients', back_populates='recipe')


class RecipesIngredients(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey(
        "recipe.id"), nullable=False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey(
        "ingredient.id"), nullable=False)
    measure = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Float, nullable=False)

    recipe = db.relationship('Recipe', back_populates='recipes_ingredients')
    ingredient = db.relationship(
        'Ingredient', back_populates='recipes_ingredients')


class IngredientSchema(Schema):
    class Meta:
        fields = ('id', 'name')


class RecipeSchema(Schema):
    class Meta:
        fields = ('id', 'name')


class RecipesIngredientsSchema(Schema):
    class Meta:
        fields = ('id', 'recipe_id', 'ingredient_id', 'measure', 'quantity')


ingredient_schema = IngredientSchema()
recipe_schema = RecipeSchema()
recipes_ingredients_schema = RecipesIngredientsSchema()


@app.route('/ingredients', methods=['GET'])
def get_ingredients():
    ingredients = Ingredient.query.all()
    result = ingredient_schema.dump(ingredients, many=True)
    return jsonify(result)


@app.route('/ingredients/<int:ingredient_id>', methods=['GET'])
def get_ingredient(ingredient_id):
    ingredient = Ingredient.query.get_or_404(ingredient_id)
    result = ingredient_schema.dump(ingredient)
    return jsonify(result)


@app.route('/add_ingredient/<ingredient_name>', methods=['GET', 'POST'])
def add_ingredient(ingredient_name):
    new_ingredient = Ingredient(ingredient_name)
    db.session.add(new_ingredient)
    db.session.commit()
    return new_ingredient


@app.route('/recipes', methods=['GET'])
def get_recipes():
    recipes = Recipe.query.all()
    result = recipe_schema.dump(recipes, many=True)
    return jsonify(result)


@app.route('/recipes/<int:recipe_id>', methods=['GET'])
def get_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    result = recipe_schema.dump(recipe)
    return jsonify(result)


@app.route('/recipesingredients', methods=['GET'])
def get_recipes_ingredients():
    recipes_ingredients = RecipesIngredients.query.all()
    result = recipes_ingredients_schema.dump(recipes_ingredients, many=True)
    return jsonify(result)


@app.route('/recipesingredients/<int:recipeingredient_id>', methods=['GET'])
def get_recipes_ingredient(recipeingredient_id):
    recipes_ingredient = RecipesIngredients.query.get_or_404(
        recipeingredient_id)
    result = recipes_ingredients_schema.dump(recipes_ingredient)
    return jsonify(result)


@app.route('/ingredients', methods=['POST'])
def create_ingredient():
    data = request.get_json()
    new_ingredient = Ingredient(name=data['name'])
    db.session.add(new_ingredient)
    db.session.commit()
    result = ingredient_schema.dump(new_ingredient)
    return jsonify(result), 201


@app.route('/ingredients/<int:ingredient_id>', methods=['PUT'])
def update_ingredient(ingredient_id):
    ingredient = Ingredient.query.get_or_404(ingredient_id)
    data = request.get_json()
    ingredient.name = data['name']
    db.session.commit()
    result = ingredient_schema.dump(ingredient)
    return jsonify(result)


@app.route('/ingredients/<int:ingredient_id>', methods=['DELETE'])
def delete_ingredient(ingredient_id):
    ingredient = Ingredient.query.get_or_404(ingredient_id)
    db.session.delete(ingredient)
    db.session.commit()
    return jsonify({"message": "Ingredient deleted successfully"}), 204


if __name__ == "__main__":
    db.create_all()
    print(Ingredient.query.all())
    app.run(debug=True)
