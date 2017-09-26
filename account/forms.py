from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label="Username")
    password = forms.CharField(widget=forms.PasswordInput)

class SearchUsersForm(forms.Form):
    search_text = forms.CharField(max_length=60)
