from flask_wtf import FlaskForm
# from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField, SelectField, DateField, TimeField, DateTimeField, FieldList, EmailField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, Regexp, InputRequired, NumberRange, Email
from .models import User
from flask_login import current_user
from datetime import datetime, timedelta, date
import phonenumbers

class RegistrationForm(FlaskForm):
    username = StringField('Username *', validators=[DataRequired(), Length(min=2, max=30)])
    firstname = StringField('First Name *', validators=[DataRequired(), Length(min=2, max=30)])
    lastname = StringField('Last Name *', validators=[DataRequired(), Length(min=2, max=30)])
    email = StringField('Email *', validators=[DataRequired(), Email()])
    password = PasswordField('Password *', validators=[DataRequired()]) #, Regexp('^(?=.*\d).{6,8}$', message='Your password should be between 6 and 8 Charaters long and contain at least 1 number')])
    confirm_password = PasswordField('Confirm Password *', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        if User.query.filter_by(username=username.data).first():
            raise ValidationError('Display Name already Taken. Please choose a different one.')

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError('Email already Used. Please Use a different one.')

class LoginForm(FlaskForm):
    username_email = StringField('Username or Email')
    password = PasswordField('Password', validators=[DataRequired(), ]) # Regexp('^(?=.*\d).{6,8}$', message='Your password should be between 6 and 8 Charaters long and contain at least 1 number')
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
    
class UpdateAccountForm(FlaskForm):
    username = StringField('Display Name *', validators=[DataRequired(), Length(min=2, max=30)])
    # email = StringField('Email *', validators=[DataRequired(), Email()])
    firstname = StringField('First Name *', validators=[DataRequired(), Length(min=2, max=30)])
    lastname = StringField('Last Name *', validators=[DataRequired(), Length(min=2, max=30)])
    submit = SubmitField('Update Account')

    def validate_username(self, username):
        if username.data.lower() != current_user.username.lower():
            if  User.query.filter_by(username=username.data).first():
                raise ValidationError('Display Name already Taken. Please choose a different one.')

    # def validate_email(self, email):
    #     if email.data != current_user.email:
    #         if User.query.filter_by(email=email.data).first():
    #             raise ValidationError('Email already Used. Please Use a different one.')

class PasswordChangeForm(FlaskForm):
    old_password = PasswordField('Old Password *', validators=[DataRequired()])
    new_password = PasswordField('New Password *', validators=[DataRequired()]) #, Regexp('^(? = .*\d).{6,8}$', message = 'Your password should be between 6 and 8 Charaters long and contain at least 1 number')])
    confirm_new_password = PasswordField('Confirm New Password *', validators=[DataRequired(), EqualTo('new_password', message = 'Passwords do not match')])
    submit = SubmitField('Change Password')

class ContactForm(FlaskForm):
    title = StringField('Title *', validators=[DataRequired(), Length(min=5, max=120)])
    firstname = StringField('First Name *', validators=[DataRequired(), Length(min=2, max=30)])
    lastname = PasswordField('Last Name *', validators=[DataRequired(), Length(min=2, max=30)])
    email = EmailField('Email *', validators=[DataRequired(), Length(min=7, max=255)])
    phone_number = IntegerField('Phone Number (+44)', validators=[DataRequired(), Length(min=0, max=11)])
    description = TextAreaField('Add some information *', validators=[DataRequired()])
    submit = SubmitField('Send')

    # This might help for future implementations https://stackoverflow.com/questions/36251149/validating-us-phone-number-in-wtforms
    # def validate_phone_number(self, phone_number):
    #     if len(phone_number.data) > 11:
    #         raise ValidationError('Invalid phone number.')
    #     try:
    #         input_number = phonenumbers.parse(phone_number.data)
    #         if not (phonenumbers.is_valid_number(input_number)):
    #             raise ValidationError('Invalid phone number.')
    #     except:
    #         input_number = phonenumbers.parse("+44"+phone_number.data)
    #         if not (phonenumbers.is_valid_number(input_number)):
    #             raise ValidationError('Invalid phone number.')