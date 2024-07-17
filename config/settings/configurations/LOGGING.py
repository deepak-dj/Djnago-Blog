LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} : {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} : {message} : {asctime}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'ERROR',  # You can adjust the logging level here
            'propagate': True,
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'blog_app': {  # Replace 'myapp' with your app's name or your custom logger
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}
