"""
Django settings for fakturomat project.

Generated by 'django-admin startproject' using Django 2.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = (os.environ['DEBUG'] == 'True')

EXTRA_MIDDLEWARE = []
if not DEBUG:
	CSRF_COOKIE_HTTPONLY = True
	CSRF_COOKIE_NAME = '__Host-csrftoken'
	CSRF_COOKIE_SAMESITE = 'Strict'
	CSRF_COOKIE_SECURE = True
	SESSION_COOKIE_AGE = 2 * 3600
	SESSION_COOKIE_HTTPONLY = True
	SESSION_COOKIE_NAME = '__Host-sessionid'
	SESSION_COOKIE_SAMESITE = 'Strict'
	SESSION_COOKIE_SECURE = True
	CSP_DEFAULT_SRC = ('https://ksiazekrzysztof.pl:443', )
	CSRF_COOKIE_SECURE = True
	REFERRER_POLICY = 'same-origin'
	SECURE_BROWSER_XSS_FILTER = True
	SECURE_CONTENT_TYPE_NOSNIFF = True
	SECURE_HSTS_INCLUDE_SUBDOMAINS = True
	SECURE_HSTS_PRELOAD = True
	SECURE_HSTS_SECONDS = 2592000 # 30 dni
	SESSION_COOKIE_SECURE = True
	X_FRAME_OPTIONS = 'DENY'

	FEATURE_POLICY = {
		'accelerometer': 'none',
		'ambient-light-sensor': 'none',
		'autoplay': 'none',
		'camera': 'none',
		'document-domain': 'none',
		'fullscreen': 'none',
		'execution-while-not-rendered': 'none',
		'execution-while-out-of-viewport': 'none',
		'gyroscope': 'none',
		'magnetometer': 'none',
		'microphone': 'none',
		'midi': 'none',
		'payment': 'none',
		'picture-in-picture': 'none',
		'publickey-credentials': 'none',
		'sync-xhr': 'none',
		'usb': 'none',
		'wake-lock': 'none',
		'xr-spatial-tracking': 'none'
	}
	EXTRA_MIDDLEWARE = [
		'csp.middleware.CSPMiddleware',
		'django_feature_policy.FeaturePolicyMiddleware',
		'django_referrer_policy.middleware.ReferrerPolicyMiddleware',
	]
ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'faktury.apps.FakturyConfig',
]

MIDDLEWARE = [
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.locale.LocaleMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
] + EXTRA_MIDDLEWARE

ROOT_URLCONF = 'fakturomat.urls'

TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [os.path.join(BASE_DIR, 'templates')]
		,
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

WSGI_APPLICATION = 'fakturomat.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.postgresql',
		'NAME': os.environ['DB_NAME'],
		'USER': os.environ['DB_USER'],
		'PASSWORD': os.environ['DB_PASSWORD'],
		'HOST': os.environ['DB_HOST'],
		'PORT': 5432,
	}
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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


# internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'pl-pl'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/
ROOT_PATH = os.path.dirname(__file__)
STATIC_ROOT = os.path.join(ROOT_PATH, 'static')
STATIC_URL = '/static/'
LOGIN_URL = '/accounts/login'
