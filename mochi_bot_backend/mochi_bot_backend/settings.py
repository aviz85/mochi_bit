import os
from dotenv import load_dotenv
from pathlib import Path
import logging

logging.basicConfig(level=logging.DEBUG)

load_dotenv()

# Define BASE_DIR
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY', 'fv^9mvmy#ft6j7z=so2=%9u$w98*#=uqy+1-vtseztykz%u^0!')

DEBUG = os.getenv('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '*').split(',')

AUTH_USER_MODEL = 'auth.User'

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

CHATBOT_TYPES = {
    'echo': {
        'name': 'Echo',
        'description': 'A simple chatbot that echoes messages',
        'class': 'chatbot.chatbot_types.echo.chatbot.EchoChatbot',
        'settings': {
            'echo_prefix': {
                'type': 'string',
                'default': 'Echo: ',
                'description': 'Prefix to add before echoing the message'
            }
        }
    },
'claudie': {
    'name': 'Claudie',
    'description': 'A chatbot powered by Anthropic AI',
    'class': 'chatbot.chatbot_types.claudie.chatbot.ClaudieChatbot',
    'settings': {
        'character': {
            'type': 'string',
            'default': 'You are a helpful AI assistant.',
            'description': 'The character or system prompt for the chatbot'
        },
        'temperature': {
            'type': 'number',
            'default': 1.0,
            'description': 'The temperature setting for the chatbot response, from 0 to 1.',
            'minimum': 0,
            'maximum': 1
        }
    }
},
    # Add other chatbot types here
}
# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# JWT settings
from datetime import timedelta
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'chatbot',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',  # Ensure this is before AuthenticationMiddleware
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'mochi_bot_backend.csrf_logging_middleware.CsrfLoggingMiddleware',  # Custom middleware
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

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
        },
    },
]

SIMPLE_JWT = {
    'AUTH_HEADER_TYPES': ('Bearer',),
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
}

# CORS settings
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://127.0.0.1:3000'
]

# CSRF settings
CSRF_TRUSTED_ORIGINS = [
    'http://localhost:3000',  # Allow localhost:3000
    'http://127.0.0.1:3000',  # Allow 127.0.0.1:3000 if you're using it
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

ROOT_URLCONF = 'mochi_bot_backend.urls'
WSGI_APPLICATION = 'mochi_bot_backend.wsgi.application'