from flask import (Flask, g, render_template, flash, redirect, url_for,
                  abort)
from peewee import *
import models
import forms

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
@app.route('/entries')
def index():
    buildings = models.Building.select()
    return render_template('index.html', buildings=buildings)


@app.route('/entries/<int:id>/new_month', methods=('GET', 'POST'))
@app.route('/details/<int:id>/new_month', methods=('GET', 'POST'))
def new_month(id):
    form = forms.NewMonth()
    forme = forms.NewMonthIncome()
    if form.validate_on_submit():
        models.Expense.create(
            month = form.month.data,
            year = form.year.data,
            name = form.name.data,
            amount = form.amount.data
        ).save()
        models.Income.create(
            month = form.month.data,
            year = form.year.data,
            name = form.name.data,
            amount = form.amount.data
        ).save()
        flash("Entry Saved!", "Success!")
        return redirect(url_for('index'))
    return render_template('new_month.html', form=form, forme=forme)

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
    return render_template('building_detail.html', expense=expense.expense, incomes=incomes)


@app.route('/index/new_building', methods=('GET', 'POST'))
def add_building():
    form = forms.NewBuilidng()
    if form.validate_on_submit():
        print("hello")
        models.Building.create(
            address = form.address.data).save()
        models.Unit.create(
            unit_num = form.unit_num.data).save()
        flash("Entry Saved!", "Success!")
        return redirect(url_for('index'))
    return render_template('new_building.html', form=form)


@app.route('/entries/<int:id>/edit', methods=('GET', 'POST'))
def edit_building(id):
    try:
        building = models.Building.get(models.Building.building_id == id)
    except models.DoesNotExist:
        abort(404)
    form = forms.NewBuilidng()
    if form.validate_on_submit():
        builindg.address = form.address.data
        entry.save()
        return redirect(url_for('index'))
    return render_template('edit_building.html', form=form, building=building)


@app.route('/entries/<int:id>/delete')
def delete_entry(id):
    models.Building.get(models.Building.building_id == id).delete_instance()
    return redirect(url_for('index'))


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404