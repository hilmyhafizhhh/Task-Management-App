# Import yang diperlukan
from django import forms
from django.contrib.auth.models import User
from .models import Task, Comment

# Form untuk membuat atau mengedit task
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'completed']  # Kolom yang akan digunakan di form

# Form registrasi user baru
class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())  # Menyembunyikan password input

    class Meta:
        model = User
        fields = ['username', 'password', 'email']  # Kolom yang akan digunakan di form

# Form untuk mengedit profil user
class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')  # Kolom yang akan digunakan di form

# Form untuk menambahkan komentar
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)  # Kolom yang akan digunakan di form
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),  # Menambahkan kelas dan ukuran pada textarea
        }
