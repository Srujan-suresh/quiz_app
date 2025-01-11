from django import forms
from django.contrib.auth.models import User
from .models import Question

class UserSignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class QuizAnswerForm(forms.Form):
    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question')  # Pass the Question object dynamically.
        super().__init__(*args, **kwargs)
        # Define choices for the quiz question options using 'A', 'B', 'C', 'D':
        self.fields['answer'] = forms.ChoiceField(
            choices=[
                ('A', question.option_1),  # Use 'A' for option 1
                ('B', question.option_2),  # Use 'B' for option 2
                ('C', question.option_3),  # Use 'C' for option 3
                ('D', question.option_4),  # Use 'D' for option 4
            ],
            widget=forms.RadioSelect,  # Display as radio buttons.
        )