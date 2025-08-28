import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: Keep this secret in production!
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")

OPENROUTER_API_KEY = "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"


# SECURITY WARNING: Don't run with debug=True in production!
DEBUG = os.getenv("DEBUG", "True") == "True"

# Allowed hosts
ALLOWED_HOSTS = ["*"]

CSRF_TRUSTED_ORIGINS = [
    "https://sellitnow-production.up.railway.app",
]

# Application definition
INSTALLED_APPS = [
    "admin_interface",
    "colorfield",  # Dependency for admin-interface
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "app",  # Your custom app
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # ✅ Ensure this is here!
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = "sellitnow.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "app/templates"],  # Template directory
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",  # Required for allauth
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "sellitnow.wsgi.application"

# Database Configuration
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# ...
#

# ✅ Updated: Cloud-hosted PostgreSQL (Railway)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv("DB_NAME", "railway"),
        'USER': os.getenv("DB_USER", "postgres"),
        'PASSWORD': os.getenv("DB_PASSWORD", "hSEjZdGIqLGMoYOtbIYLPxbNxwQrtKFc"),
        'HOST': os.getenv("DB_HOST", "interchange.proxy.rlwy.net"),
        'PORT': os.getenv("DB_PORT", "50440"),
        "default": dj_database_url.config(
        default=os.environ.get("interchange.proxy.rlwy.net"),
        conn_max_age=600,
        ssl_require=True
    }
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'app/static']  # Ensure this path is correct
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files (Uploaded content)
DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"

CLOUDINARY_STORAGE = {
    "CLOUD_NAME": os.getenv("CLOUDINARY_CLOUD_NAME"),
    "API_KEY": os.getenv("CLOUDINARY_API_KEY"),
    "API_SECRET": os.getenv("CLOUDINARY_API_SECRET"),
}

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Authentication settings
AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)

# Django-Allauth settings (Updated)
ACCOUNT_RATE_LIMITS = {
    "login_failed": "5/m",  # 5 failed login attempts per minute
    "login": "10/m",  # 10 successful logins per minute
}

# Allow login with either username or email
ACCOUNT_AUTHENTICATION_METHOD = "username_email"

# Make username required
ACCOUNT_USERNAME_REQUIRED = True

# Keep email optional (if needed)
ACCOUNT_EMAIL_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = "optional"  # Adjust as needed


# Login URLs
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

# Email settings (Use environment variables for production security)
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.getenv("EMAIL_HOST", "sandbox.smtp.mailtrap.io")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "5618690533dd66")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "72a7bccc645082")
EMAIL_PORT = os.getenv("EMAIL_PORT", "2525")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", "no-reply@sellitnow.com")

# Enable Whitenoise for static file management (Optional)
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Cloudinary settings for media files
DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"
CLOUDINARY_STORAGE = {
    "CLOUD_NAME": os.getenv("CLOUDINARY_CLOUD_NAME"),
    "API_KEY": os.getenv("CLOUDINARY_API_KEY"),
    "API_SECRET": os.getenv("CLOUDINARY_API_SECRET"),
}

# Customizing session settings (Optional)
SESSION_ENGINE = "django.contrib.sessions.backends.db"
SESSION_COOKIE_NAME = "sessionid"
