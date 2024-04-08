REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Dagestan travel',
    'DESCRIPTION': 'Dagestan travel backend service',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}
