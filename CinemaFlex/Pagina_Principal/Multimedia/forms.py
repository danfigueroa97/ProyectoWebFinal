from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Multimedia, Comentario, Respuesta

class NuevoUsuarioForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ("email","username", "password1", "password2")

	def save(self, commit=True):
		user = super(NuevoUsuarioForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user

class UpdateUsuarioForm(forms.ModelForm):
    password1 = forms.CharField(required=False, widget=forms.PasswordInput)
    password2 = forms.CharField(required=False, widget=forms.PasswordInput)
    email = forms.EmailField(required=False)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super(UpdateUsuarioForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = None

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 or password2:
            if password1 != password2:
                raise forms.ValidationError("Las contraseñas no coinciden")
        return password2

    def save(self, commit=True):
        user = super(UpdateUsuarioForm, self).save(commit=False)
        email = self.cleaned_data.get('email')
        password1 = self.cleaned_data.get('password1')

        if email:
            user.email = email
        if password1:
            user.set_password(password1)
        if commit:
            user.save()
        return user


	
class MultimediaForm(forms.ModelForm):
    class Meta:
        model = Multimedia
        fields = ['Nombre', 'Descripcion', 'Imagen', 'categoria','Link']
        widgets = {
			'Imagen': forms.FileInput(attrs={'enctype': 'multipart/form-data'}),
			'Link': forms.URLInput(attrs={'placeholder': 'Enter Youtube link here'}),
			}

class SearchForm(forms.Form):
    query = forms.CharField(label='Buscar', max_length=255)

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['texto']

class RespuestaForm(forms.ModelForm):
    class Meta:
        model = Respuesta
        fields = ['contenido']


