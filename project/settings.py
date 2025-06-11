from pathlib import Path
from decouple import config
import cloudinary_storage


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY')

DEBUG = False

ALLOWED_HOSTS = ['.railway.app', '*']
CSRF_TRUSTED_ORIGINS = [
    'https://web-production-50a2b.up.railway.app',
]


INSTALLED_APPS = [
    'jazzmin',
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cloudinary',
    'cloudinary_storage',
    'channels',
    'app'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI_APPLICATION = 'project.wsgi.application'
ASGI_APPLICATION = 'project.asgi.application'
AUTH_USER_MODEL = 'app.User'

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [config("REDIS_URL")],
        },
    }
}


CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": [config("REDIS_URL")],
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DATABASE_NAME'),
        'USER': config('DATABASE_USER'),
        'PASSWORD': config('DATABASE_PASSWORD'),
        'HOST': config('DATABASE_HOST'),  # ou o IP/hostname do servidor do banco
        'PORT': config('DATABASE_PORT'),       # porta padrão do PostgreSQL
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

# whitenoise settings
FORCE_BUILD = True
STATIC_URL = '/static/'
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
STATICFILES_DIRS = (
    BASE_DIR / 'base_static',
)
STATIC_ROOT = BASE_DIR / 'static'


MEDIA_ROOT = BASE_DIR / 'media'

if DEBUG:
    MEDIA_URL = '/media/'
else:
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

    CLOUDINARY_STORAGE = {
        'CLOUD_NAME': config('CLOUDINARY_NAME'),
        'API_KEY': config('CLOUDINARY_API_KEY'),
        'API_SECRET': config('CLOUDINARY_API_SECRET'),  
    }


# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



JAZZMIN_SETTINGS = {
    # title of the window (Will default to current_admin_site.site_title if absent or None)
    'site_title': 'Painel do ADM',

    # Title on the login screen (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    'site_header': 'Painel do ADM',

    # Title on the brand (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    'site_brand': 'Painel do ADM',

    'icons': {
        'auth': 'fas fa-users-cog',
        'auth.user': 'fas fa-user',
        'auth.Group': 'fas fa-users',
        'products.Brand': 'fas fa-copyright',
        'products.Category': 'fas fa-object-group',
        'products.Product': 'fas fa-box',
    },

    # Welcome text on the login screen
    'welcome_sign': 'Bem-vindo(a) ao painel administrativo',

    # Copyright on the footer
    'copyright': '@pedromariva | Todos os direitos reservados',

    # List of model admins to search from the search bar, search bar omitted if excluded
    # If you want to use a single search field you dont need to use a list, you can use a simple string 
    'search_model': ['app.User',],

    # Whether to show the UI customizer on the sidebar
    'show_ui_builder': True,
}
