from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm

from django.contrib.auth.models import User
from django.conf import settings
from django import forms

from .models import Profile, Address


class CustomAvatarWidget(forms.ClearableFileInput):
    """
    Свой шаблон виджета file_input
    """
    template_name = 'widgets/custom_avatar_widget.html'


class CustomUserCreationForm(UserCreationForm):
    """
    Форма регистрации
    """
    first_name = forms.CharField(max_length=32, required=True, label='Имя')
    last_name = forms.CharField(max_length=32, required=True, label='Фамилия')
    email = forms.EmailField(max_length=128, required=True, label='Email')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email',
                  'username', 'password1', 'password2']
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'email': 'Email',
            'username': 'Логин',
            'password1': 'Пароль',
            'password2': 'Подтверждение пароля'
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            self.add_error('password2', 'Пароли не совпадают')

        return password2

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control form-control-lg'})


class ProfileForm(forms.ModelForm):
    """
    Форма профиля
    """
    avatar = forms.ImageField(widget=CustomAvatarWidget(), required=False)
    email = forms.EmailField(max_length=128, required=True, label='Email')

    def clean_avatar(self):
        """
        Проверяю размер файла
        """
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            if avatar.size > settings.MAX_FILE_SIZE_MB * 1024 * 1024:
                raise forms.ValidationError(f'Максимальный размер файла - {settings.MAX_FILE_SIZE_MB} MB')
        return avatar

    class Meta:
        model = Profile
        fields = [
            'first_name', 'last_name', 'surname',
            'email', 'avatar', 'gender'
        ]

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name != 'avatar':
                field.widget.attrs.update({'class': 'form-control'})
                if name == 'gender':
                    field.widget.attrs.update({'class': 'form-control form-select'})


class CustomPasswordChangeForm(PasswordChangeForm):
    class Meta:
        fields = ["old_password", "new_password1", "new_password2"]
        labels = {
            "old_password": 'Старый пароль',
            "new_password1": 'Новый пароль',
            "new_password2": 'Подтвердите новый пароль'
        }

    def __init__(self, *args, **kwargs):
        super(CustomPasswordChangeForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})


class AddressCreationForm(forms.ModelForm):

    class Meta:
        model = Address
        fields = ['name', 'full_name', 'phone_number', 'address_line',
                  'city', 'postal_code', 'region', 'country']

        labels = {
            'name': 'Название адреса*',
            'full_name': 'ФИО полностью*',
            'phone_number': 'Номер телефона*',
            'address_line': 'Адрес (улица, корпус, дом, квартира)*',
            'city': 'Город*',
            'postal_code': 'Почтовый индекс*',
            'region': 'Регион (необязательно)',
            'country': 'Страна*'
        }

    def __init__(self, *args, **kwargs):
        super(AddressCreationForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
