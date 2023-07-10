# haku/forms.py

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from wtforms_sqlalchemy.fields import QuerySelectField
from haku.models.user import User
from haku.models.community import Community

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    bio = TextAreaField('Bio',
                        validators=[Length(max=500)])
    submit = SubmitField('Update')

class UpdatePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=8)])
    confirm_new_password = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Update Password')

def community_choices():
    return Community.query

class TextPostForm(FlaskForm):
    community = QuerySelectField('Community', query_factory=community_choices, get_label='name', allow_blank=False, validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post', id='text-submit')

class LinkPostForm(FlaskForm):
    community = QuerySelectField('Community', query_factory=community_choices, get_label='name', allow_blank=False, validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    link_url = StringField('Link URL', validators=[DataRequired()])
    submit = SubmitField('Post', id='link-submit')

class ImagePostForm(FlaskForm):
    community = QuerySelectField('Community', query_factory=community_choices, get_label='name', allow_blank=False, validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    image_file = FileField('Upload Image/Video', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif', 'mp4', 'mov', 'avi', 'mkv'])])
    submit = SubmitField('Post', id='image-submit')

class CommunityForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Create Community')