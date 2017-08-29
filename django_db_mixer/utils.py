import django.apps
from django.db import connections
from django.db.utils import OperationalError


def check_db():
    db_conn = connections['mixer']
    try:
        db_conn.cursor()
    except OperationalError:
        connected = False
    else:
        connected = True

    return connected


def get_models():
    models = []
    labels = [x.label for x in django.apps.apps.get_app_configs() if x.label != 'django_db_mixer']
    for label in labels:
        generator_models = django.apps.apps.get_app_config(label).get_models()
        for model in generator_models:
            models.append(model)
    return models
