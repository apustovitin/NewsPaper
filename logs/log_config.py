from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent
LOGCONF = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "debug": {
            "format": "%(asctime)s %(levelname)s %(message)s"
        },
        "warning": {
            "format": "%(asctime)s %(levelname)s %(pathname)s %(message)s"
        },
        "error": {
            "format": "%(asctime)s %(levelname)s  %(pathname)s %(exc_info)s %(message)s"
        },
        "info": {
            "format": "%(asctime)s %(levelname)s %(module)s %(message)s"
        },
    },
    "filters": {
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    "handlers": {
        "console_error": {
            "level": "ERROR",
            "class": "logging.StreamHandler",
            "formatter": "error"
        },
        "console_warning": {
            "level": "WARNING",
            "class": "logging.StreamHandler",
            "formatter": "warning"
        },
        "console_debug": {
            "level": "DEBUG",
            "filters": ["require_debug_true"],
            "class": "logging.StreamHandler",
            "formatter": "debug"
        },
        "file_info": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": BASE_DIR / "general.log",
            "formatter": "info"
        },
        "file_error": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "filename": BASE_DIR / "errors.log",
            "formatter": "error"
        },
        "file_security": {
            "class": "logging.FileHandler",
            "filename": BASE_DIR / "security.log",
            "formatter": "info"
        },
        "mail_admins": {
            "level": "ERROR",
            "class": "django.utils.log.AdminEmailHandler",
            "formatter": "warning"
        }
    },
    "loggers": {
        "django": {
            "handlers": ["console_error","console_warning","console_debug","file_info"],
            "propagate": True,
        },
        "django.request": {
            "handlers": ["file_error","mail_admins"],
            "propagate": True,
        },
        "django.server": {
            "handlers": ["file_error","mail_admins"],
            "propagate": True,
        },
        "django.template": {
            "handlers": ["file_error"],
            "propagate": True,
        },
        "django.db_backends": {
            "handlers": ["file_error"],
            "propagate": True,
        },
        "django.security": {
            "handlers": ["file_security"],
            "propagate": True,
        },
    }
}