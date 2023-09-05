from pathlib import Path
import os , sys , json
from django.contrib import messages


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

############# secret key 관련 ####################################################3
# secrets.json의 경로
SECRETS_PATH = os.path.join(BASE_DIR, 'secrets.json')
# json파일을 파이썬 객체로 변환
secrets = json.loads(open(SECRETS_PATH).read())
# json파일은 dict로 변환되므로, .items()를 호출해 나온 key와 value를 사용해
# settings모듈에 동적으로 할당
for key, value in secrets.items():
    setattr(sys.modules[__name__], key, value)

#environ을 기존 import에 추가
import environ

env = environ.Env(DEBUG=(bool, True)) #환경변수를 불러올 수 있는 상태로 세팅

#환경변수 파일 읽어오기
environ.Env.read_env(
    env_file=os.path.join(BASE_DIR, '.env')
)

SECRET_KEY = env('SECRET_KEY') #SECEREY_KEY 값 불러오기
DEBUG = env('DEBUG') #DEBUG 값 불러오기
###########################################################################################

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

DEBUG = False
ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'accounts', # 내 정보
    # 'accounts.apps.UsersConfig',
    'board', # 자유게시판
    'education', # 학습
    'translation',
    # 교정탭, 수어스쿨탭, 무느이탭 추가요망
    'phonenumber_field',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',

    'bootstrap4',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mysite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'mysite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',   
#         'HOST': 'localhost',                    
#         'PORT': '3306',
#         'NAME': 'mydb',
#         'USER': 'root',
#         'PASSWORD': 'admin123',
#         },
# }



# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTH_USER_MODEL = 'accounts.user'

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

# LANGUAGE_CODE = 'en-us'
# TIME_ZONE = 'UTC'

LANGUAGE_CODE = 'ko-kr'
TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/


STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'mysite', 'static'),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'static')


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

# DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL ='/'

# CSRF_TRUSTED_ORIGINS = ['http://127.0.0.1:8000/', 'https://127.0.0.1:8000/']
CSRF_TRUSTED_ORIGINS = ['http://127.0.0.1:8000/accounts/login/login_logic', 'https://127.0.0.1:8000/accounts/login/login_logic']

import os, json
from django.core.exceptions import ImproperlyConfigured

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

secret_file = os.path.join(BASE_DIR, 'secrets.json')

with open(secret_file) as f:
    secrets = json.loads(f.read())

def get_secret(setting, secrets=secrets):
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {} environment variable".format(setting)
        raise ImproperlyConfigured(error_msg)

SECRET_KEY = get_secret("SECRET_KEY")

# Simple Mail Transfer Protocol

"""import dj_database_url
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)"""

"""import environ
env = environ.Env(
    #Set casting, default value
    DEBUG=(bool, False) )
env.read_env()"""

from environ import Env

env = Env()
env_path = os.path.join(BASE_DIR, ".env")
if os.path.exists(env_path):
    with open(env_path, "rt", encoding="utf8") as f:
        env.read_env(f, overwrite=True)

if os.path.exists(os.path.join(BASE_DIR, "login.txt")):
    with open(os.path.join(BASE_DIR, "login.txt"), "rt", encoding="utf-8") as f:
        id = f.readline().split('\n')[0]
        pw = f.readline().split('\n')[0]

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_PORT = '587'
EMAIL_HOST = 'smtp.naver.com'
EMAIL_HOST_USER = id
EMAIL_HOST_PASSWORD = pw
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = id

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',     # 권장, 2015년 암호 해싱 경쟁 에서 우승한 알고리즘
                                                            # 만약 안되면 pip install django[argon2]
                                                            # pip install argon2-cffi
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',     # SHA256 + salt 방식, salt는 랜덤이고, hashing 횟수는 커스텀으로 늘려 보안 강화 권장
                                                            # 해싱 알고리즘, 알고리즘 반복 횟수(작업 요소), 무작위 솔트 및 결과 암호 해시로 구성 
                                                            # NIST 에서 권장하는 암호 확장 메커니즘인 SHA256 해시 PBKDF2 알고리즘 사용
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    #'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',   # 암호 저장을 위해 특별히 설계된 널리 사용되는 암호 저장 알고리즘, pip install django[bcrypt], pip install bcrypt
    #'django.contrib.auth.hashers.BCryptPasswordHasher',
    #'django.contrib.auth.hashers.ScryptPasswordHasher',
    #'django.contrib.auth.hashers.SHA1PasswordHasher',
    #'django.contrib.auth.hashers.MD5PasswordHasher',
    #'django.contrib.auth.hashers.UnsaltedSHA1PasswordHasher',
    #'django.contrib.auth.hashers.UnsaltedMD5PasswordHasher',
]

google_file = os.path.join(BASE_DIR, 'google.json')

with open(google_file) as f:
    googles = json.loads(f.read())

GOOGLE_RECAPTCHA_SECRET_KEY = "GOOGLE_KEY"
# 실전에서는 get_secret이나 json에 담아서 보관할것!

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'django.server': {
            '()': 'django.utils.log.ServerFormatter',
            'format': '[{server_time}] {message}',
            'style': '{',
        },
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        },
        'django.server': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'django.server',
        },
        'mail_admins': {
            'level': 'INFO',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'file': {
            'level': 'DEBUG',
            'encoding': 'utf-8',
            'filters': ['require_debug_false'],
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/mysite.log'),
            'maxBytes': 1024*1024*24,  # 24 MB
            'backupCount': 10,
            'formatter': 'standard',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'mail_admins', 'file'],
            'level': 'INFO',
        },
        'django.server': {
            'handlers': ['django.server'],
            'level': 'INFO',
            'propagate': False,
        },
        'my': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
        },
    }
}

FILE_UPLOAD_HANDLERS = [
    'django.core.files.uploadhandler.MemoryFileUploadHandler',
    'django.core.files.uploadhandler.TemporaryFileUploadHandler',
]