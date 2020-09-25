from peewee import *

DATABASE = SqliteDatabase('my_calculations.db')

class Base(Model):
    class Meta:
        database = DATABASE

class MonthlyBase(Base):
    month = CharField()
    year = IntegerField()
    amount = IntegerField()


class Building(Base): 
    building_id = IntegerField(primary_key=True, unique=True)
    address = CharField(max_length = 100, default = "Address")

class Unit(Base):
    unit_id = IntegerField(primary_key=True, unique=True)
    building = ForeignKeyField(Building, backref = "units")
    unit_num = CharField(max_length = 10)

class ExpenseType(Base):
    expense_type_id = IntegerField(primary_key=True, unique=True)
    expense_type = CharField(max_length = 20)

class Expense(MonthlyBase):
    expense_id = IntegerField(primary_key=True, unique=True)
    building = ForeignKeyField(Building, backref = "expenses")
    expense_type = ForeignKeyField(ExpenseType)

class Income(MonthlyBase):
    income_id = IntegerField(primary_key=True, unique=True)
    unit = ForeignKeyField(Unit, backref = "incomes")
    




DATABASE.connect()
DATABASE.create_tables([Building, Unit, Expense, Income, ExpenseType], safe=True)
DATABASE.close()
