import os
import configparser
from pathlib import Path
from django.urls.base import reverse_lazy

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Импортирую конфиг
config = configparser.ConfigParser()
config.read(os.path.join(Path(__file__).resolve().parent, 'conf.ini'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-ac@qt216vew_(k=+49oerripksf#b&v0&$%^&pu4e!orox0(vr'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog.apps.BlogConfig',
    'users.apps.UsersConfig',
    'shop.apps.ShopConfig',
    'order.apps.OrderConfig'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries': {
                'custom_filters': 'blog.templatetags.filters',
            },
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'ru-Ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
STATIC_DIR = os.path.join(BASE_DIR, 'static/')
STATICFILES_DIRS = [STATIC_DIR]

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

LOGIN_URL = reverse_lazy('users:login')
LOGOUT_URL = reverse_lazy('users:logout')

PER_PAGE = 2

CART_SESSION_ID = 'cart'
COUPON_SESSION_ID = 'promocode'

DEFAULT_AVATAR = 'avatars/default.png'
MAX_FILE_SIZE_MB = 5

EMAIL_BACKEND = 'django_smtp_ssl.SSLEmailBackend'
EMAIL_HOST = config.get('settings', 'EMAIL_HOST')  # Замените на адрес вашего SMTP-сервера
EMAIL_PORT = 465  # Порт вашего SMTP-сервера (обычно 587 или 25)
EMAIL_HOST_USER = config.get('settings', 'EMAIL_HOST_USER')  # Ваше имя пользователя для авторизации на SMTP-сервере
EMAIL_HOST_PASSWORD = config.get('settings', 'EMAIL_HOST_PASSWORD')  # Ваш пароль для авторизации на SMTP-сервере
# EMAIL_USE_TLS = True  # Использовать ли шифрование TLS/SSL
EMAIL_USE_SSL = True
DEFAULT_FROM_EMAIL = config.get('settings', 'DEFAULT_FROM_EMAIL')  # Ваш адрес электронной почты

PASSWORD_RESET_TOKEN_TIMEOUT = 24*3600

SESSION_COOKIE_SECURE = True

BASE_URL = 'http://127.0.0.1:8000/'