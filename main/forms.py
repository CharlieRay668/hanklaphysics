from django import forms
import datetime as dt
from .models import Question, PhysicsClass, Answer


class CreateNewQuestion(forms.ModelForm):
    title = forms.CharField()
    body = forms.TextInput()
    physics_class = forms.ChoiceField(label = "Which class are you in?", choices=[(1,'AP Physics'),
                                        (2,'Standard Physics'),
                                        (3,'Honors Physics')])
    class Meta:
        model = Question
        fields = ['title', 'body', 'physics_class']
        #     'title' : forms.CharField(),
        #     'body' : forms.TextInput(),
        #     'physics_class' :forms.ChoiceField(label="crossover_select", choices=class_choices)
        # }

class CreateNewAnswer(forms.ModelForm):
    body = forms.TextInput()
    class Meta:
        model = Answer
        fields = ['body']

class CreateNewClass(forms.ModelForm):
    name = forms.CharField()

    class Meta:
        model = PhysicsClass
        fields = ['name']
    
class SearchForm(forms.Form):
    score_sort = forms.CheckboxInput()
    date_sort = forms.CheckboxInput()