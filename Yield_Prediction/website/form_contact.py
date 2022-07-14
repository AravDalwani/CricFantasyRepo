from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, TextAreaField, SubmitField, IntegerField, SelectField, FloatField, DecimalField
from wtforms.validators import DataRequired, Email, NumberRange

csrf = CSRFProtect()

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired('Please Enter Your Name')])
    email = StringField('E-mail', validators=[DataRequired('Please Enter a Correct Email'),Email('Please Enter a Correct Email')])
    subject = StringField('Subject', validators=[DataRequired('Please Enter the Subject')])
    message = TextAreaField('Message', validators=[DataRequired('Please Enter the Message')])
    submit = SubmitField("Submit")

class PredForm(FlaskForm):
    nitrogen = DecimalField('Nitrogen', validators=[DataRequired('Please Enter a Valid Amount')])
    pottasium = DecimalField('Pottasium', validators=[DataRequired('Please Enter a Valid Amount')])
    phosphorous = DecimalField('Phosphorous', validators=[DataRequired('Please Enter a Valid Amount')])
    carbon = DecimalField('Carbon %', validators=[DataRequired('Please Enter a Valid Amount')])
    zinc = DecimalField('Zinc', validators=[DataRequired('Please Enter a Valid Amount')])
    iron = DecimalField('Iron', validators=[DataRequired('Please Enter a Valid Amount')])
    copper = DecimalField('Copper', validators=[DataRequired('Please Enter the Message')])
    manganese = DecimalField('Manganese', validators=[DataRequired('Please Enter a Valid Amount')])
    boron = DecimalField('Boron', validators=[DataRequired('Please Enter a Valid Amount')])
    sulfur = DecimalField('Sulfur', validators=[DataRequired('Please Enter a Valid Amount')])
    submit = SubmitField('Submit')
