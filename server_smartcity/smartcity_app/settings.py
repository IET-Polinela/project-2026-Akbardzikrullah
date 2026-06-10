from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY
SECRET_KEY = 'django-insecure-%j_c-&4e-fsl%_1c9qbh8dfx3v)$gh-z=l^_#w2lke46-mgnw6'
DEBUG = True
ALLOWED_HOSTS = ['*'] # 🛠️ UBAHAN 1: Diubah agar bisa diakses oleh server luar 

# APPLICATIONS
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders', # 🔥 BARU: Tambahkan corsheaders di sini

    # APP KAMU
    'main_app',
    'about',
    'contacts',
    'usermanagement_24782035',
    'dashboard_24782035',
]

# MIDDLEWARE
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware', # 🔥 BARU: Wajib diletakkan paling atas!
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'smartcity_app.urls' # 🛠️ UBAHAN 2: Referensi folder diubah ke smartcity_app 

# TEMPLATES
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # 🔥 penting untuk login.html
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

WSGI_APPLICATION = 'smartcity_app.wsgi.application' # 🛠️ UBAHAN 3: Referensi folder diubah ke smartcity_app 

# DATABASE (PostgreSQL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'smartcity_db',
        'USER': 'postgres',
        'PASSWORD': 'akbar123',  # ganti kalau beda
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# PASSWORD VALIDATION
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# INTERNATIONAL
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# STATIC FILES
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles' # 🛠️ UBAHAN 4: Menambahkan Static Root untuk deployment 

# DEFAULT AUTO FIELD
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CUSTOM USER MODEL
AUTH_USER_MODEL = 'usermanagement_24782035.CustomUser'

# LOGIN & LOGOUT REDIRECT
LOGOUT_REDIRECT_URL = '/'
LOGIN_REDIRECT_URL = '/reports/'


REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

# 🔥 BARU: Konfigurasi akses CORS (Ditaruh di paling bawah)
# CORS Settings
CORS_ALLOW_ALL_ORIGINS = True # Mengizinkan semua domain untuk mengakses API [cite: 52]