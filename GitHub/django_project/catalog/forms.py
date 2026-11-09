from django import forms
from .models import Item
class FeedbackForm(forms.Form):
 name=forms.CharField(label='Ім’я',max_length=60)
 email=forms.EmailField(label='Електронна пошта')
 category=forms.ChoiceField(label='Тип звернення',choices=[('question','Запитання'),('idea','Пропозиція')])
 message=forms.CharField(label='Повідомлення',widget=forms.Textarea)
 def clean_message(self):
  value=self.cleaned_data['message'].strip()
  if len(value.split())<3:raise forms.ValidationError('Введіть щонайменше три слова')
  return value
class ItemForm(forms.ModelForm):
 class Meta:
  model=Item;fields=['title','category','price','description','available']
