from flask import (Flask, g, render_template, flash, redirect, url_for,
                  abort)
from peewee import *
import models

DEBUG = True
PORT = 8000
HOST = '0.0.0.0'

app = Flask(__name__)
app.secret_key = 'auoesh.bouoastuh.43,uoausoehuosth3ououea.auoub!'

@app.before_request
def before_request():
    """Connect to the database before each request."""
    g.db = models.DATABASE
    g.db.connect()


@app.after_request
def after_request(response):
    """Close the database connection after each request."""
    g.db.close()
    return response

@app.route('/')
def index():
    buildings = models.Building.select()
    return render_template('index.html', buildings=buildings)

@app.route('/detail/<int:id>')
def detail(id):
    expense = (models.Building
        .select(models.Building, 
                models.Expense.month, 
                models.Expense.year, 
                models.Expense.name, 
                models.Expense.amount)
        .join(models.Expense)
        .where(models.Building.building_id == id)
        ).first()
    incomes = (models.Building
        .select(models.Building,
                models.Unit.unit_num,
                models.Income.month,
                models.Income.year,
                models.Income.name,
                models.Income.amount)
        .join(models.Unit)
        .join(models.Income)
        .where(models.Building.building_id == id)
        )
    # for income in incomes:
    #     print("asdf")
    #     print(income.unit.income.amount)
    return render_template('building_detail.html', expense=expense.expense, incomes=incomes)

