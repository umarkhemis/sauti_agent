import os
from pathlib import Path
import environ

BASE_DIR = Path(__file__).resolve().parent.parent.parent

env = environ.Env(
    DEBUG=(bool, False)
)
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

SECRET_KEY = env('SECRET_KEY', default='dev-secret-key-change-in-production')
DEBUG = env('DEBUG', default=False)
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'apps.users',
    'apps.speech',
    'apps.intent',
    'apps.dialogue',
    'apps.ussd',
    'apps.mobile_money',
    'apps.calls',
    'apps.sms',
    'apps.contacts',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'sautiagent.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'sautiagent.wsgi.application'
ASGI_APPLICATION = 'sautiagent.asgi.application'

DATABASES = {
    'default': env.db('DATABASE_URL', default='sqlite:///db.sqlite3')
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

AUTH_USER_MODEL = 'users.User'

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Kampala'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Cache
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': env('REDIS_URL', default='redis://localhost:6379/0'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# Celery
CELERY_BROKER_URL = env('REDIS_URL', default='redis://localhost:6379/0')
CELERY_RESULT_BACKEND = env('REDIS_URL', default='redis://localhost:6379/0')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Africa/Kampala'

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
}

# File uploads (10MB for audio)
DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760
FILE_UPLOAD_MAX_MEMORY_SIZE = 10485760

# Sunbird AI
SUNBIRD_API_KEY = env('SUNBIRD_API_KEY', default='')
SUNBIRD_API_URL = env('SUNBIRD_API_URL', default='https://api.sunbird.ai/tasks')

# OpenAI
OPENAI_API_KEY = env('OPENAI_API_KEY', default='')

# MTN MoMo
MTN_MOMO_API_USER = env('MTN_MOMO_API_USER', default='')
MTN_MOMO_API_KEY = env('MTN_MOMO_API_KEY', default='')
MTN_MOMO_SUBSCRIPTION_KEY = env('MTN_MOMO_SUBSCRIPTION_KEY', default='')
MTN_MOMO_BASE_URL = env('MTN_MOMO_BASE_URL', default='https://sandbox.momodeveloper.mtn.com')

# Airtel Money
AIRTEL_CLIENT_ID = env('AIRTEL_CLIENT_ID', default='')
AIRTEL_CLIENT_SECRET = env('AIRTEL_CLIENT_SECRET', default='')
AIRTEL_BASE_URL = env('AIRTEL_BASE_URL', default='https://openapi.airtel.africa')

# Supported Languages
SUPPORTED_LANGUAGES = {
    'lug': 'Luganda',
    'ach': 'Acholi',
    'nyn': 'Runyankole',
    'lso': 'Lusoga',
    'lgg': 'Lugbara',
    'eng': 'English',
}

WELCOME_MESSAGES = {
    'welcome_english': ('To use English, start speaking in English', 'eng'),
    'welcome_luganda': ('Okwogera Luganda, yambaza mu Luganda', 'lug'),
    'welcome_runyankole': ('Okukozesa Runyankole, wogerere mu Runyankole', 'nyn'),
    'welcome_acholi': ('Ting lok Acholi, lok ki Acholi', 'ach'),
    'welcome_lusoga': ('Okukozesa Lusoga, yogera mu Lusoga', 'lso'),
    'welcome_lugbara': ('Nze SautiAgent, yaka mu Lugbara', 'lgg'),
}
