from flask_wtf import FlaskForm
from wtforms import StringField, DateField, IntegerField, SelectField
from wtforms.validators import DataRequired, InputRequired

from models import *

class NewBuilidng(FlaskForm):
    address = StringField(
        "Address",
        validators = [DataRequired()
        ])
    unit_num = StringField(
        "Unit Number",
        validators = [DataRequired()
        ])

class NewExpense(FlaskForm):
    month = StringField(
        "Month",
        validators = [DataRequired()
        ])
    year = StringField(
        "Year",
        validators = [DataRequired()
        ])
    name = StringField(
        "Name",
        validators = [DataRequired()
        ])
    amount = StringField(
        "Amount",
        validators = [DataRequired()
        ])


class NewIncome(FlaskForm):
    month = StringField(
        "Month",
        validators = [DataRequired()
        ])
    year = StringField(
        "Year",
        validators = [DataRequired()
        ])
    name = StringField(
        "Name",
        validators = [DataRequired()
        ])
    amount = StringField(
        "Amount",
        validators = [DataRequired()
        ])
    unit = SelectField(
        u"Select Unit"
    )


class NewUnit(FlaskForm):
    new = StringField(
        "New Unit",
        validators = [DataRequired()
        ])
