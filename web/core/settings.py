import os
from pathlib import Path

import dj_database_url
from django.contrib import messages
from django.utils.translation import gettext_lazy as _

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("SECRET_KEY", None)

DEBUG = str(os.environ.get("DEBUG")) == "True"
SITE_URL = os.environ.get("SITE_URL")


if DEBUG:
    ALLOWED_HOSTS = ["127.0.0.1", "localhost"]
else:
    ALLOWED_HOSTS = [os.environ.get("SITE_HOST")]


if not DEBUG:
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    CSRF_TRUSTED_ORIGINS = [
        os.environ.get("SITE_URL"),
        os.environ.get("SITE_URL2", None),
    ]
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")


CORS_ALLOWED_ORIGIN_REGEXES = [SITE_URL, os.environ.get("SITE_URL2", None)]


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.contrib.sitemaps",
    "django_cleanup.apps.CleanupConfig",
    "log_viewer",
    "ckeditor",
    "ckeditor_uploader",
    "rosetta",
    "axes",
    "activities",
    "bats",
    "base",
    "administration",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.gzip.GZipMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "core.middleware.MaintenanceModeMiddleware",
    "axes.middleware.AxesMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "core.context_processors.site_info",
                "core.context_processors.config",
                "core.context_processors.menu",
                "core.context_processors.footer_menu",
                "core.context_processors.admin_menu",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"

SITE_ID = 1


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB"),
        "USER": os.environ.get("POSTGRES_USER"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
        "HOST": os.environ.get("POSTGRES_HOST"),
        "PORT": os.environ.get("POSTGRES_PORT"),
    }
}

DATABASE_URL = os.environ.get("DATABASE_URL", None)
if DATABASE_URL:
    db_from_env = dj_database_url.config(default=DATABASE_URL, conn_max_age=1800)
    DATABASES["default"].update(db_from_env)


AUTHENTICATION_BACKENDS = [
    # "axes.backends.AxesStandaloneBackend",
    "django.contrib.auth.backends.ModelBackend",
]


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {
            "min_length": 12,
        },
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


LOGIN_URL = "administration:login"
LOGIN_REDIRECT_URL = "administration:dashboard"

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Baku"

USE_I18N = True

USE_L10N = True

USE_TZ = True

LANGUAGE_CODE = "az"

LANGUAGES = (
    ("az", _("Azerbaijani")),
    ("en", _("English")),
)

LOCALE_PATHS = (BASE_DIR / "locale/",)


LOG_DIR = BASE_DIR / "logs"
LOG_FILE = "/info.log"
LOG_PATH = f"{LOG_DIR}/{LOG_FILE}"

if not os.path.exists(LOG_DIR):
    os.mkdir(LOG_DIR)

if not os.path.exists(LOG_PATH):
    f = open(LOG_PATH, "a").close()
else:
    f = open(LOG_PATH, "w").close()

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
        "main": {
            "format": "{levelname} at {asctime} in {module} - {name} - {message}",
            "style": "{",
        },
    },
    "filters": {
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "filters": ["require_debug_true"],
            "class": "logging.StreamHandler",
            "formatter": "main",
        },
        "mail_admins": {
            "level": "ERROR",
            "class": "django.utils.log.AdminEmailHandler",
            "formatter": "main",
        },
        "file": {
            "level": "WARNING",
            "formatter": "main",
            "class": "logging.FileHandler",
            "filename": LOG_PATH,
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file", "console"],
            "propagate": True,
        },
        "django.request": {
            "handlers": ["file", "console"],
            "level": "ERROR",
            "propagate": False,
        },
        "main": {
            "handlers": ["file", "console"],
            "propagate": True,
            "level": "WARNING",
        },
    },
}

LOG_VIEWER_FILES = ["info"]
LOG_VIEWER_FILES_PATTERN = "*.log*"
LOG_VIEWER_FILES_DIR = "logs/"
LOG_VIEWER_PAGE_LENGTH = 25
LOG_VIEWER_MAX_READ_LINES = 1000
LOG_VIEWER_FILE_LIST_MAX_ITEMS_PER_PAGE = 25
LOG_VIEWER_PATTERNS = ["[INFO]", "[DEBUG]", "[WARNING]", "[ERROR]", "[CRITICAL]"]
LOG_VIEWER_EXCLUDE_TEXT_PATTERN = None


STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static_cdn"
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


SERVER_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", "")
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", "")
EMAIL_BACKEND = "django_smtp_ssl.SSLEmailBackend"
EMAIL_HOST = os.environ.get("EMAIL_HOST", "")
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
EMAIL_PORT = os.environ.get("EMAIL_PORT", "")
EMAIL_USE_TLS = str(os.environ.get("EMAIL_USE_TLS")) == "1"
EMAIL_USE_SSL = str(os.environ.get("EMAIL_USE_SSL")) == "1"
EMAIL_USE_LOCALTIME = True


CKEDITOR_ALLOW_NONIMAGE_FILES = False
CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_CONFIGS = {
    "default": {
        "height": 900,
    },
}


MESSAGE_TAGS = {
    messages.constants.DEBUG: "alert-secondary",
    messages.constants.INFO: "alert-info",
    messages.constants.SUCCESS: "alert-success",
    messages.constants.WARNING: "alert-warning",
    messages.constants.ERROR: "alert-danger",
}


AXES_COOLOFF_TIME = 0.20
AXES_FAILURE_LIMIT = 10
AXES_RESET_ON_SUCCESS = True


MAINTENANCE_MODE = int(os.environ.get("MAINTENANCE_MODE", 0))
MAINTENANCE_BYPASS_QUERY = os.environ.get("MAINTENANCE_BYPASS_QUERY")


DJANGO_ADMIN_URL_SUFFIX = os.environ.get("DJANGO_ADMIN_URL_SUFFIX")
ADMIN_URL_SUFFIX = os.environ.get("ADMIN_URL_SUFFIX")
