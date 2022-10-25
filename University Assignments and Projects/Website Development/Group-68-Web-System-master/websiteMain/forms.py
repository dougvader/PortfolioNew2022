from django.contrib.auth import get_user_model
from django import forms

USER_TYPE_CHOICES = (
    ('Tourist', 'Tourist'),
	('Student', 'Student'),
	('Businessman', 'Businessman')
)

User = get_user_model()

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    user_type = forms.ChoiceField(choices = USER_TYPE_CHOICES, required=True)
	
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'user_type', 'password']
        
