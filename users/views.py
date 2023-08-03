from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, \
PasswordResetConfirmView
from django.urls import reverse
from django.views.decorators.http import require_POST

from .forms import CustomUserCreationForm, ProfileForm, CustomPasswordChangeForm, AddressCreationForm
from blog.models import Category, Comment
from .models import Profile, Address
from shop.models import Cart
from shop.cart import Cart as myCart


def login_view(request):
    categories = Category.objects.all()
    context = {
        'categories': categories
    }

    if request.user.is_authenticated:
        # Если пользователь выполнил вход
        return redirect('blog:index')

    if request.method == 'POST':
        # Если нажали кнопку входа
        username = request.POST['username'].lower()
        password = request.POST['password']

        # Вход по юзернейму
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Вход успешен
            login(request, user)
            # Загружаю последнюю сохраненную корзину в сессию

            cart = myCart(request)
            try:
                cart_obj = Cart.objects.get(owner=request.user.profile)
                cart.setter(cart_obj.data)
            except Cart.DoesNotExist:
                pass
            # Переход на next, иначе на индекс
            return redirect(request.POST['next'] if request.POST['next'] != '' else 'blog:index')
        else:
            messages.error(request, 'Неправильные данные для входа')

    return render(request, 'login.html', context)


def logout_view(request):
    cart = myCart(request)
    # Получаю последнюю сохранненую корзину в бд
    try:
        last_cart_obj = Cart.objects.get(owner=request.user.profile)
        last_cart_obj.delete()
    except Cart.DoesNotExist:
        pass

    # Создаю новый объект корзины и сохраняю его
    cart_obj = Cart(owner=request.user.profile, data=cart.cart)
    cart_obj.save()
    logout(request)
    messages.info(request, 'Вы вышли из учетной записи')
    return redirect('users:login')


def registration_view(request):
    """
    Регистрация пользователя
    """
    categories = Category.objects.all()
    form = CustomUserCreationForm()

    if request.POST:
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            # Если пользователь с таким именем уже существует
            if User.objects.filter(username=user.username).exists():
                messages.error(request, 'Пользователь с таким именем уже существует')
            else:
                user.save()
                authenticated_user = authenticate(request,
                                                  username=user.username,
                                                  password=form.cleaned_data['password1'])
                if authenticated_user is not None:
                    login(request, authenticated_user)
                    messages.success(request, 'Аккаунт успешно создан')

                    return redirect('users:profile')
                else:
                    messages.error(request, 'Ошибка при попытке входа на сайт')
        else:
            messages.error(request, 'Во время регистрации возникла ошибка')

    context = {
        'categories': categories,
        'form': form

    }
    return render(request, 'registration.html', context)


@login_required
def profile_view(request):
    categories = Category.objects.all()
    profile = Profile.objects.get(user=request.user)
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            if 'avatar-clear' in request.POST:
                profile.avatar = settings.DEFAULT_AVATAR
            form.save()
            messages.success(request, 'Данные профиля обновлены')
            return redirect('users:profile')
        else:
            messages.error(request, 'Ошибка изменения данных')

    context = {
        'categories': categories,
        'form': form
    }
    return render(request, 'profile.html', context)


@login_required
def profile_security_view(request):
    categories = Category.objects.all()

    form = CustomPasswordChangeForm(request.user)

    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Ваш пароль был успешно изменен')
            return redirect('users:security')
        else:
            messages.error(request, 'Ошибка. Пожалуйста проверьте вводимые данные')
    context = {
        'categories': categories,
        'form': form
    }
    return render(request, 'profile_security.html', context)


class PasswordRecoveryView(PasswordResetView):
    template_name = 'password_recovery.html'
    email_template_name = 'mail/reset_password.txt'
    subject_template_name = 'mail/reset_subject.txt'

    def get_form_class(self):
        form_class = super().get_form_class()
        for field in form_class.base_fields.values():
            field.widget.attrs.update({'class': 'form-control'})
        return form_class

    def get_success_url(self):
        return reverse('users:recovery_done')


class PasswordRecoveryDoneView(PasswordResetDoneView):
    template_name = 'password_recovery_done.html'


class PasswordRecoveryConfirmView(PasswordResetConfirmView):
    template_name = 'password_recovery_confirm.html'
    post_reset_login = True

    def get_form_class(self):
        """
        Добавляю свои классы полям
        """
        form_class = super().get_form_class()
        for field in form_class.base_fields.values():
            field.widget.attrs.update({'class': 'form-control'})
        return form_class

    def get_success_url(self):
        return reverse('blog:index')


@login_required
def activity_view(request):
    categories = Category.objects.all()
    comments = Comment.objects.filter(owner=request.user.profile)

    if request.method == 'POST':
        comment_id = int(request.POST['comment_id'])
        comment = Comment.objects.get(id=comment_id)
        if request.user.is_superuser or request.user.profile == comment.owner:
            comment.delete()
            messages.success(request, 'Комментарий удалён')
        else:
            messages.error(request, 'У Вас недостаточно прав на удаление этого комментария')
        return redirect('users:activity')

    context = {
        'categories': categories,
        'comments': comments
    }

    return render(request, 'activity.html', context)


@login_required
def addresses_view(request):
    categories = Category.objects.all()
    user_profile = Profile.objects.get(user=request.user)
    addresses = user_profile.address.all()
    context = {
        'categories': categories,
        'addresses': addresses
    }
    return render(request, 'addresses.html', context)


@login_required
def create_address(request):
    categories = Category.objects.all()

    if request.method == 'POST':
        form = AddressCreationForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user.profile
            address.save()
            messages.success(request, f'Адрес {address.name} добавлен')
            return redirect('users:addresses')
        else:
            messages.error(request, 'Ошибка. Проверьте вводимые данные')
    else:
        form = AddressCreationForm()

    context = {
        'categories': categories,
        'form': form
    }

    return render(request, 'create_address.html', context)


@login_required
def change_address(request, aid):
    categories = Category.objects.all()
    address = get_object_or_404(Address, id=aid, user=request.user.profile)

    if request.method == 'POST':
        form = AddressCreationForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            messages.success(request, f'Адрес { address.name } изменён')
            return redirect('users:addresses')
    else:
        form = AddressCreationForm(instance=address)

    context = {
        'categories': categories,
        'form': form
    }
    return render(request, 'change_address.html', context)


@login_required
@require_POST
def delete_address(request, aid):
    address = get_object_or_404(Address, id=aid)
    if address:
        aname = address.name
        address.delete()
        messages.success(request, f'Адрес { aname } удалён')
    else:
        messages.error(request, 'Ошибка. Что-то пошло не так')

    return redirect('users:addresses')


@login_required
@require_POST
def select_main_address(request, aid):
    address = get_object_or_404(Address, id=aid, user=request.user.profile)
    address.is_main = True
    address.save()
    user_profile = request.user.profile
    user_profile.address.exclude(id=address.id).update(is_main=False)
    return redirect('users:addresses')