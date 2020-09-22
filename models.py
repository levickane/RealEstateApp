from peewee import *

DATABASE = SqliteDatabase('my_calculations.db')

class Base(Model):
    class Meta:
        database = DATABASE

class MonthlyBase(Base):
    month = CharField()
    year = IntegerField()
    name = CharField()
    amount = IntegerField()


class Building(Base): 
    building_id = IntegerField(primary_key=True, unique=True)
    address = CharField(max_length = 100)

class Unit(Base):
    unit_id = IntegerField(primary_key=True, unique=True)
    building = ForeignKeyField(Building, backref = "unit")
    unit_num = CharField(max_length = 10)

class Expense(MonthlyBase):
    expense_id = IntegerField(primary_key=True, unique=True)
    building = ForeignKeyField(Building, backref = "expenses")

class Income(MonthlyBase):
    income_id = IntegerField(primary_key=True, unique=True)
    unit = ForeignKeyField(Unit, backref = "income")
    


DATABASE.connect()
DATABASE.create_tables([Building, Unit, Expense, Income], safe=True)
DATABASE.close()
