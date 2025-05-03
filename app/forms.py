from django import forms
from .models import User
from django.contrib.auth import authenticate


class LoginForm(forms.Form):
    username = forms.CharField(
        label='Nome de usuário',
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'Digite seu nome de usuário...', 'required': True})
    )
    password = forms.CharField(
        label='Senha',
        max_length=128,
        widget=forms.PasswordInput(attrs={'placeholder': 'Digite sua senha...', 'required': True})
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError("Esse nome de usuário não existe!")

        user = authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError("Senha incorreta!")
        
        return cleaned_data


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password',  'image_profile', 'bio')

        widgets = {
            'username': forms.TextInput(attrs={'name': 'username', 'placeholder': 'Nome de usuário', 'required': True}),
            'email': forms.EmailInput(attrs={'name': 'email', 'placeholder': 'Seu E-mail', 'required': True}),
            'password': forms.PasswordInput(attrs={'name': 'password', 'placeholder': 'Sua Senha', 'required': True}),
            'image_profile': forms.FileInput(attrs={'name': 'avatar', 'placeholder': 'Imagem de perfil (Opcional)', 'accept': 'image/*'}),
            'bio': forms.Textarea(attrs={'name': 'bio', 'placeholder': 'Sobre você (Opcional)', 'rows': 3})
        }
 
    def clean_username(self):
        current_username = self.instance.username
        username = self.cleaned_data.get('username')
        if current_username != username:
            if User.objects.filter(username=username).exists():
                raise forms.ValidationError("Esse nome de usuário já existe.")
        return username
    
    def clean_email(self):
        current_email = self.instance.email
        email = self.cleaned_data.get('email')
        if current_email != email:
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError("Esse e-mail já existe.")
        return email
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise forms.ValidationError("A senha deve ter pelo menos 8 caracteres.")
        return password
