from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from .models import Room, User


class MyUserCreationForm(UserCreationForm):

    class Meta:
        model=User
        fields=['avatar','name', 'username','email', 'password1','password2']

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = "__all__"
        exclude = ['host', 'participants']  #to exclude extra fields
        
class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar','name','username','email','bio']