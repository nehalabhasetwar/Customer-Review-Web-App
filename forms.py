from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField , TextField
from wtforms.validators import DataRequired, Length


class ReviewForm(FlaskForm):
    """customer review form."""

    username = StringField('Name',[DataRequired()])
    product = StringField('Product Name', [DataRequired()])
    review = TextField( 'Message',[ DataRequired(), Length(min=4,message=('Your message is too short.'))])
    '''recaptcha = RecaptchaField()'''
    submit = SubmitField('Submit')

class SearchForm(FlaskForm):

    product_name = StringField('Product Name', [DataRequired()])
    submit = SubmitField('Submit')


class DeleteTaskForm(FlaskForm):
    submit = SubmitField('Delete')