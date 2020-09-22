from flask_wtf import FlaskForm
from wtforms import StringField, DateField, IntegerField
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

class NewMonth(FlaskForm):
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


class NewMonthIncome(FlaskForm):
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

