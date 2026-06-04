# projectsite/settings.py
import os
from pathlib import Path

# 1. Core Paths & System Settings
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-local-development-key-change-this-in-production'
DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'techassist.pythonanywhere.com']
ROOT_URLCONF = 'projectsite.urls'
WSGI_APPLICATION = 'projectsite.wsgi.application'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 2. Installed Modules Configuration
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    
    # Custom Application Module
    'tickets',
    'widget_tweaks',
    
    # Django AllAuth Architecture
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    
    # Progressive Web Application Container
    'pwa',
]

SITE_ID = 1

# 3. Security, Authentication & Session Routing
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/accounts/login/'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# 4. Engine Core Database Mapping
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# 5. Rendering Engine Context Assembly
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

# 6. Localization Rules
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# 7. Static Asset Directories Layout Routing
STATIC_URL = 'static/'
STATICFILES_DIRS = [ BASE_DIR / 'static' ]
STATIC_ROOT = BASE_DIR / 'staticfiles'

# 8. PWA Service Worker Manifest Mapping (Required for PWA Module Initialization)
PWA_APP_NAME = 'TechAssist'
PWA_APP_DESCRIPTION = "TechAssist IT Helpdesk System Workspace"
PWA_APP_THEME_COLOR = '#0f172a'
PWA_APP_BACKGROUND_COLOR = '#f8fafc'
PWA_APP_DISPLAY = 'standalone'
PWA_APP_START_URL = '/'
PWA_SERVICE_WORKER_PATH = os.path.join(BASE_DIR, 'static', 'js', 'serviceworker.js')