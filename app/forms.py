from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm


class RegistrationForm(UserCreationForm):
    name = forms.CharField(
        label='Enter Your Name', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(
        label='Create Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(
        label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.CharField(
        label='Email', required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    op1 = forms.IntegerField(widget=forms.PasswordInput(attrs={"class": "form-control"}),
                             label="Position of Image 1", min_value=1, max_value=9)
    op2 = forms.IntegerField(widget=forms.PasswordInput(attrs={"class": "form-control"}),
                             label="Position of Image 2", min_value=1, max_value=9)
    op3 = forms.IntegerField(widget=forms.PasswordInput(attrs={"class": "form-control"}),
                             label="Position of Image 3", min_value=1, max_value=9)

    class Meta:
        model = User
        fields = ['name', 'email', 'password1',
                  'password2', 'op1', 'op2', 'op3']

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.name = self.cleaned_data['name']
        user.username = self.cleaned_data['email']
        user.email = self.cleaned_data['email']
        op1 = self.cleaned_data['op1']
        op2 = self.cleaned_data['op2']
        op3 = self.cleaned_data['op3']
        pattern = str(op1) + str(op2) + str(op3)
        user.pattern_order = pattern
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"}))


class Level2Form(forms.Form):
    op1 = forms.IntegerField(widget=forms.PasswordInput(attrs={"class": "form-control"}),
                             label="Position of Image 1", min_value=1, max_value=9)
    op2 = forms.IntegerField(widget=forms.PasswordInput(attrs={"class": "form-control"}),
                             label="Position of Image 2", min_value=1, max_value=9)
    op3 = forms.IntegerField(widget=forms.PasswordInput(attrs={"class": "form-control"}),
                             label="Position of Image 3", min_value=1, max_value=9)


class Level3Form(forms.Form):
    otp = forms.IntegerField(widget=forms.NumberInput(attrs={"class": "form-control"}),
                             label="Enter The OTP")
