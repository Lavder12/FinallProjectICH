from pathlib import Path
import environ
import os

# Указываем базовую директорию проекта
BASE_DIR = Path(__file__).resolve().parent.parent

# Подключение переменных окружения
env = environ.Env()
environ.Env.read_env(BASE_DIR / '.env')

# Секретный ключ и отладка
SECRET_KEY = env('SECRET_KEY', default='replace-me-with-your-secret-key')
DEBUG = env.bool('DEBUG', default=True)
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['127.0.0.1', 'localhost'])

# Установленные приложения
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Ваши локальные приложения
    'web_room',
    'users',
]

# Промежуточное ПО (middleware)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Файл маршрутов
ROOT_URLCONF = 'main.urls'

# Настройки шаблонов
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # Добавлен каталог шаблонов на случай, если он используется
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI приложение
WSGI_APPLICATION = 'main.wsgi.application'

# Настройки базы данных
DATABASES = {
    'default': {
        'ENGINE': env('ENGINE', default='django.db.backends.mysql'),
        'NAME': env('NAME', default='your_database_name'),
        'USER': env('USER', default='root'),
        'PASSWORD': env('PASSWORD', default='root'),
        'HOST': env('HOST', default='localhost'),
        'PORT': env('PORT', default='3306'),
    }
}

# Валидация паролей
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

# Локализация и часовой пояс
LANGUAGE_CODE = 'ru'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Настройки статических файлов
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
    os.path.join(BASE_DIR, 'users/static'),
    os.path.join(BASE_DIR, 'web_room/static'),
]

# Настройки для загружаемых медиафайлов
MEDIA_URL = '/media/'  # URL для загружаемых файлов
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # Папка для медиафайлов

# Тип первичного ключа по умолчанию
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Настройки авторизации
LOGIN_REDIRECT_URL = 'web_room:home'
LOGIN_URL = 'users:login'
