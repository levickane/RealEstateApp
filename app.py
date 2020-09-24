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


@app.route('/entries/<int:id>/new_expense', methods=('GET', 'POST'))
@app.route('/details/<int:id>/new_expense', methods=('GET', 'POST'))
def new_expense(id):
    form = forms.NewExpense()
    if form.validate_on_submit():
        models.Expense.create(
            building_id = id,
            month = form.month.data,
            year = form.year.data,
            name = form.name.data,
            amount = form.amount.data
        ).save()
        flash("Entry Saved!", "Success!")
        return redirect(url_for('index'))
    return render_template('new_expense.html', form=form)



@app.route('/entries/<int:id>/new_income', methods=('GET', 'POST'))
@app.route('/details/<int:id>/new_income', methods=('GET', 'POST'))
def new_income(id):
    formi = forms.NewIncome()
    building_units = models.Unit.select(models.Unit.unit_id, models.Unit.unit_num).where(models.Unit.building_id == id)
    formi.unit.choices = [(i.unit_id, i.unit_num) for i in building_units]
    if formi.validate_on_submit():
        models.Income.create(
            unit_id = formi.unit.data,
            month = formi.month.data,
            year = formi.year.data,
            name = formi.name.data,
            amount = formi.amount.data
        ).save()
        flash("Entry Saved!", "Success!")
        return redirect(url_for('index'))
    return render_template('new_income.html', formi=formi)


@app.route('/detail/<int:id>')
def detail(id):
    form = forms.NewUnit()
    expenses = (models.Building
        .select(models.Building, 
                models.Expense.month, 
                models.Expense.year, 
                models.Expense.name, 
                models.Expense.amount)
        .join(models.Expense)
        .where(models.Building.building_id == id)
        )
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
    building = models.Building.select(models.Building.address).where(models.Building.building_id == id).first()
    return render_template('building_detail.html', expenses=expenses, incomes=incomes, form=form, id=id, building=building)


@app.route('/index/new_building', methods=('GET', 'POST'))
def add_building():
    form = forms.NewBuilidng()
    if form.validate_on_submit():
        building1 = models.Building.create(
            address = form.address.data)
        building1.save()
        models.Unit.create(
            building = building1,
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
        building.address = form.address.data
        return redirect(url_for('index'))
    return render_template('edit_building.html', form=form, building=building)


@app.route('/detail/<int:id>/new_unit', methods=["POST"])
def new_unit(id):
    form = forms.NewUnit()
    if form.validate_on_submit():
        models.Unit.create(
            unit_num = form.new.data,
            building_id = id
        ).save()
        return redirect('/detail/'+ str(id))
    return redirect(url_for('index'))


@app.route('/entries/<int:id>/delete')
def delete_entry(id):
    models.Building.get(models.Building.building_id == id).delete_instance()
    return redirect(url_for('index'))


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404