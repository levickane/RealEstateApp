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
    building_expense = models.Expense.select(models.Expense.expense_id, models.Expense.expense_type).where(models.Expense.building_id == id)
    form.choices = [(i.expense_id, i.expense_type) for i in building_expense]
    if form.validate_on_submit():
        models.Expense.create(
            expense_type = form.new_expense_name.data,
            month = form.month.data,
            year = form.year.data,
            amount = form.amount.data
        ).save()
        flash("Entry Saved!", "Success!")
        return redirect(url_for('index'))
    return render_template('new_expense.html', form=form)



@app.route('/entries/<int:id>/new_income', methods=('GET', 'POST'))
@app.route('/details/<int:id>/new_income', methods=('GET', 'POST'))
def new_income(id):
    form = forms.NewIncome()
    building_units = models.Unit.select(models.Unit.unit_id, models.Unit.unit_num).where(models.Unit.building_id == id)
    form.unit.choices = [(i.unit_id, i.unit_num) for i in building_units]
    if form.validate_on_submit():
        models.Income.create(
            unit_id = form.unit.data,
            month = form.month.data,
            year = form.year.data,
            amount = form.amount.data
        ).save()
        flash("Entry Saved!", "Success!")
        return redirect(url_for('index'))
    return render_template('new_income.html', form=form)


@app.route('/detail/<int:id>')
def detail(id):
    form = forms.NewUnit()
    expenses = (models.Building
        .select(models.Building, 
                models.Expense.month, 
                models.Expense.year, 
                models.Expense.expense_type,
                models.Expense.amount)
        .join(models.Expense)
        .where(models.Building.building_id == id)
        )
    incomes = (models.Building
        .select(models.Building,
                models.Unit.unit_num,
                models.Income.month,
                models.Income.year,
                models.Income.amount)
        .join(models.Unit)
        .join(models.Income)
        .where(models.Building.building_id == id)
        )
    building = models.Building.select(models.Building.address).where(models.Building.building_id == id).first()
    return render_template('building_detail.html', expenses=expenses, incomes=incomes, form=form, id=id, building=building)


@app.route('/index/new_building', methods=('GET', 'POST'))
def add_building():
    form = forms.NewBuilding()
    if form.validate_on_submit():
        building = models.Building.create(
            address = form.address.data)
        building.save()
        flash("Entry Saved!", "Success!")
        return redirect(url_for('index'))
    return render_template('new_building.html', form=form)


@app.route('/entries/<int:id>/edit', methods=('GET', 'POST'))
def edit_building(id):
    building = models.Building.get(models.Building.building_id == id)
    form = forms.NewBuilding()
    print("hello")
    if form.validate_on_submit():
        building.address = form.address.data
        building.save()
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



@app.route('/detail/<int:id>/new_expense_name', methods=["POST"])
def new_expense_name(id):
    form = forms.NewExpenseName()
    if form.validate_on_submit():
        models.Expense.create(
            expense_type = form.expense_name.data,
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