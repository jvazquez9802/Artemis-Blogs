from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length
        
class PostForm(FlaskForm):
    title = StringField('Tittle', validators=[DataRequired(), Length(min=2, max=100)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=2, max=250)])
    content = TextAreaField('Content', validators=[DataRequired()])
    labels = StringField('Add Labels', validators=[DataRequired(), Length(min=2, max=100)])
    
    submit = SubmitField('Send')