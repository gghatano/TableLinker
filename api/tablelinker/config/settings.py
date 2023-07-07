import os
import yaml
from datetime import timedelta
# from datasets.item_mapping.mapping import Similarity

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "w7rf)z5hk#pavinpv84@_gjuzxv%1!%ggh*2(j6fond(4zp3tt"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG") is not None

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_celery_results",
    "django_ses",
    "django_extensions",
    "rest_framework",
    "django_filters",
    "storages",
    "convertors.celery",
    "users.apps.UsersConfig",
    "datasets.apps.DatasetsConfig",
    "dataset_convertors.apps.DatasetConvertorsConfig",
    "dataset_templates.apps.DatasetTemplatesConfig",
    "graphene_django",
    "corsheaders",
    "graphql_jwt.refresh_token.apps.RefreshTokenConfig",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "shared/templates"), ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "shared.context_processors.debug",
            ],
            "libraries": {"utility": "shared.templatetags.shared_extras"},
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.getenv("DB_NAME", "tablelinker"),
        "USER": os.getenv("DB_USER", ""),
        "PASSWORD": os.getenv("DB_PASSWORD", ""),
        "HOST": os.getenv("DB_HOST", "root"),
        "PORT": os.getenv("DB_PORT", ""),
        "ATOMIC_REQUESTS": False,
    }
}
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator", },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator", },
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator", },
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator", },
]

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = os.getenv("LANGUAGE", "ja-JP")
TIME_ZONE = os.getenv("TZ", "Asia/Tokyo")

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = "/static/"

# Auth And Login
AUTH_USER_MODEL = "users.User"

# Login
LOGIN_URL = "users:login"
LOGIN_REDIRECT_URL = "datasets:list"
LOGOUT_REDIRECT_URL = "users:login"

# EMAIL メールサーバーへの接続設定
if os.getenv("AWS_SES_REGION_NAME") is not None:
    EMAIL_BACKEND = "django_ses.SESBackend"
    AWS_SES_REGION_NAME = os.getenv("AWS_SES_REGION_NAME")
    AWS_SES_REGION_ENDPOINT = os.getenv("AWS_SES_REGION_ENDPOINT")
    AWS_SES_ACCESS_KEY_ID = os.getenv("AWS_SES_ACCESS_KEY_ID")
    AWS_SES_REGION_ENDPOINT = os.getenv("AWS_SES_REGION_ENDPOINT")
    DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL")
else:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = os.getenv("MAIL_HOST", "")
    EMAIL_PORT = os.getenv("MAIL_PORT", "587")
    EMAIL_HOST_USER = os.getenv("MAIL_USER", "")
    EMAIL_HOST_PASSWORD = os.getenv("MAIL_PASSWORD", "")
    EMAIL_USE_TLS = True if os.getenv("MAIL_USE_TLS", "0") == "1" else False


# File Upload
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

if os.getenv("AWS_STORAGE_BUCKET_NAME") is not None:
    DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
    AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

    # AWS_QUERYSTRING_EXPIRE = 3600
    AWS_DEFAULT_ACL = None

# JOBQUEUE CELERY
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://redis:6379/1")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/2")
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = TIME_ZONE

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer", "rest_framework.renderers.BrowsableAPIRenderer", ],
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated", "shared.permissions.IsOwnerOrReadOnly",),
    "DEFAULT_AUTHENTICATION_CLASSES": ["rest_framework.authentication.SessionAuthentication", ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
}

MODEL_FILEPATH = os.getenv("MODEL_FILEPATH", "similar_search/jawiki-20190820.model")  # 10MB

# CORS
CORS_ORIGIN_WHITELIST = [
    # "http://localhost:8080",
]

if os.getenv("AWS_STORAGE_BUCKET_NAME") is not None:
    AWS_STORAGE = True
    CORS_ORIGIN_WHITELIST.append("https://" + os.getenv("AWS_STORAGE_BUCKET_NAME") + ".s3.amazonaws.com")
else:
    AWS_STORAGE = False

CORS_ALLOW_CREDENTIALS = True

# convertors
CONV_FILTES_DIRS = [os.path.join(BASE_DIR, "customs")]

if DEBUG:
    import os
    import socket

    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS = [ip[:-1] + "1" for ip in ips] + ["127.0.0.1", "10.0.2.2"]
    # INTERNAL_IPS = ('127.0.0.1', 'localhost')

    # SQLをログに出力する
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "handlers": {"console": {"level": "DEBUG", "class": "logging.StreamHandler", }, },
        # "loggers": {
        #     "django.db.backends": {"handlers": ["console"], "level": "DEBUG",},
        # },
    }
else:
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "production": {
                "format": "%(asctime)s [%(levelname)s] %(process)d %(thread)d " "%(pathname)s:%(lineno)d %(message)s"
            },
        },
        "handlers": {"console": {"level": "INFO", "class": "logging.StreamHandler", "formatter": "production", }, },
        "loggers": {
            "": {"handlers": ["console"], "level": "DEBUG", "propagate": False, },
            # Djangoの警告・エラー
            "django": {"handlers": ["console"], "level": "DEBUG", "propagate": False, },
            # SQL
            "django.db.backends": {"handlers": ["console"], "level": "INFO", },
        },
    }

GRAPHENE = {
    "SCHEMA": "graphql_schema.root_schema.schema",
    "MIDDLEWARE": ["graphql_jwt.middleware.JSONWebTokenMiddleware", ],
}

AUTHENTICATION_BACKENDS = [
    "graphql_jwt.backends.JSONWebTokenBackend",
    "django.contrib.auth.backends.ModelBackend",
]

GRAPHQL_JWT = {
    "JWT_VERIFY_EXPIRATION": True,
    "JWT_LONG_RUNNING_REFRESH_TOKEN": True,
    "JWT_EXPIRATION_DELTA": timedelta(days=7),
    "JWT_REFRESH_EXPIRATION_DELTA": timedelta(days=7),
}

PASSWORD_RESET_SUBJECT = "パスワード変更コードの通知"

WIKIDATA_MAP_PATH = os.path.join(BASE_DIR, "mapping/wikidata.yml")
WIKIDATA_MAP = {}
with open(WIKIDATA_MAP_PATH) as file:
    yaml_map = yaml.safe_load(file)
    WIKIDATA_MAP = yaml_map["wikidata_map"]

COLUMN_NAME_MAP_PATH = os.path.join(BASE_DIR, "mapping/column_name.yml")
COLUMN_NAME_MAP = {}
with open(COLUMN_NAME_MAP_PATH) as file:
    yaml_map = yaml.safe_load(file)
    COLUMN_NAME_MAP = yaml_map["column_name_map"]

# SIMILARTY = Similarity()
