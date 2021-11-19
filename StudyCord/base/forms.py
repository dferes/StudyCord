from django.db.models import fields
from django.forms import ModelForm
from .models import Room, User
from django.contrib.auth.forms import UserCreationForm

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2'] # By using 'password1' and 'password2', Django will verify that the two strings match 


class RoomForm(ModelForm):
    class Meta:
        model = Room
        #fields = ['name','body','etc']
        fields = '__all__'
        exclude = ['host', 'participants']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'name', 'username', 'email', 'bio']
