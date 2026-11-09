from flask_wtf import FlaskForm
from wtforms import StringField,EmailField,SelectField,TextAreaField,SubmitField
from wtforms.validators import DataRequired,Length,Email,ValidationError
class FeedbackForm(FlaskForm):
 name=StringField('Ім’я',[DataRequired(),Length(max=60)])
 email=EmailField('Електронна пошта',[DataRequired(),Email()])
 category=SelectField('Тип звернення',choices=[('question','Запитання'),('idea','Пропозиція')])
 message=TextAreaField('Повідомлення',[DataRequired()])
 submit=SubmitField('Надіслати')
 def validate_message(self,field):
  if len(field.data.strip().split())<3:raise ValidationError('Введіть щонайменше три слова')
