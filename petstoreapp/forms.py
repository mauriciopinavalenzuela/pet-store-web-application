from django import forms
from .models import Producto
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'marca', 'categoria', 'precio', 'descripcion', 'imagen', 'stock']

    def clean(self):
        cleaned_data = super().clean()
        nombre = cleaned_data.get('nombre')
        marca = cleaned_data.get('marca')
        categoria = cleaned_data.get('categoria')

        if not nombre and not marca and not categoria:
            raise forms.ValidationError("Debes seleccionar al menos uno de los campos: nombre, marca o categoría.")

        return cleaned_data

    def clean_precio(self):
        precio = self.cleaned_data['precio']
        if precio <= 0:
            raise forms.ValidationError("El precio debe ser mayor que cero.")
        return precio

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class RegistroForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()

    class Meta:
        model=User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("El correo electrónico ya está registrado.")
        return email
