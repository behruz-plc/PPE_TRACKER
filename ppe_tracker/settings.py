from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-rs8rt4x_0t6ts=^_5$crpx)0z7a)=#&a2p&_pmr+tiru0(9(-@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["ppetracker.onrender.com"]

# Application definition
INSTALLED_APPS = [
    'jazzmin',
    'Группы',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

# Updated Jazmin settings with improved aesthetics
JAZZMIN_SETTINGS = {
    "site_title": False,
    "site_header": False,
    "site_brand": False,
    "welcome_sign": "Добро пожаловать на сайт контроля средств индивидуальной защиты ЦЛ КИП и А",
    "site_logo": "images/uaplogo.png",  # Add your logo
    "login_logo": "images/nkmkuaplogo.png",
    # "login_background": "images/background.jpg",
    # "site_icon": "static/favicon.ico",

    # 🌈 Color Scheme (Soft & Modern)
    "theme": "solar",  # Elegant and modern look
    "primary_color": "#4CAF50",  # Soft Green
    "secondary_color": "#16A085",  # Teal
    "body_background": "#F7F9FC",  # Very light gray/white
    "navbar_color": "#4CAF50",  # Same as primary
    "sidebar_color": "#4CAF50",  # Dark Blue-Gray
    "sidebar_hover_color": "#1ABC9C",  # Teal
    "sidebar_nav_link_color": "#ECF0F1",  # Light Gray
    "sidebar_nav_link_hover_color": "#FFFFFF",  # White text on hover

    # 🎨 Sidebar & Menu Customization
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": ["reports"],
    "hide_models": [],
    "order_with_respect_to": ["auth", "Группы"],
    "default_icon_parents": "fas fa-folder",
    "default_icon_children": "fas fa-file-alt",

    # 🖼️ App Icons (Modern & Clean)
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.group": "fas fa-users",
        "Группы.Employee": "fas fa-user-tie",
        "Группы.PPEItem": "fas fa-hard-hat",
        "Группы.IssuedPPE": "fas fa-clipboard-list",
        "Группы.ReplacementPeriod": "fas fa-calendar-alt",
    },

    # ✨ UI Enhancements
    "custom_css": "static/custom_admin.css",  # Custom styling
    "custom_js": "static/custom_admin.js",  # Custom JS (Animations)
    "use_google_fonts_cdn": True,
    "changeform_format": "horizontal_tabs",  # Tabs for better usability
    "changeform_format_overrides": {
        "auth.user": "collapsible",
        "Группы.Employee": "horizontal_tabs",
    },

    # 📊 Dashboard Customization
    "user_avatar": None,
    "related_modal_active": True,  # Modern popups
    "show_ui_builder": False,  # Hide Jazzmin UI Tweaks (Not needed)
    "show_sidebar_quicklinks": True,
    "show_sidebar_recent": False,  # Hide "Recent Actions"
    "show_recent": False,  # Fully disable "Recent Actions"
    "show_sidebar_apps": False,

    # 🔗 Top Menu Links
    "topmenu_links": [
        {"name": "Домашняя страница", "url": "admin:index", },  # "permissions": ["auth.view_user"]
        {"model": "auth.User"},
        {"app": "Группы"},
        {"name": "Уведомления о СИЗ",
         "url": "http://172.17.39.30:8000/%D0%93%D1%80%D1%83%D0%BF%D0%BF%D1%8B/notifications/", "icon": "fas fa-bell"}
    ],

    "usermenu_links": [
        {"model": "auth.user"},
    ],

    # 🚀 Footer & Branding
    "copyright": "Tursunpo'lotov Behruz",
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-cyan",
    "accent": "accent-indigo",
    "navbar": "navbar-indigo navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": True,
    "sidebar_fixed": True,
    "sidebar": "sidebar-light-indigo",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "minty",
    "dark_mode_theme": False,
    "button_classes": {
        "primary": "btn btn-success",
        "secondary": "btn btn-outline-secondary",
        "info": "btn btn-info",
        "warning": "btn btn-warning",
        "danger": "btn btn-danger",
        "success": "btn btn-success"
    },
    "actions_sticky_top": False,
    "rounded_buttons": True,
    "rounded_corners": True,
    "animations": True,
    "sidebar_small_text": False
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',

]

ROOT_URLCONF = 'ppe_tracker.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "Группы/templates/"],  # Make sure 'templates/' is included
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

WSGI_APPLICATION = 'ppe_tracker.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Asia/Tashkent'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")  # Add this line
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

PPE_ALERT_DAYS = 30  # Number of days before alert
