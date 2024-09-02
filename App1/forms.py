from django import forms
from .models import Libro

class LibroForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = ['titulo', 'autor', 'editorial', 'fecha', 'isbn', 'numero_pags', 'numero_topografia', 'numero_ejemplar', 'descripcion', 'portada']



from django import forms
from django.contrib.auth.models import User

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']

class UserEmailForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']