from django.core.management.base import BaseCommand
from django.db.models.fields import related, reverse_related

from django_db_mixer import utils
from django_db_mixer.models import ModelSetting, FieldSetting


class Command(BaseCommand):

    def handle(self, *args, **options):
        models = utils.get_models()
        priority = 0
        exists_models_in_db = set()
        while models:
            priority += 1
            for model in models:
                is_rel_field = 0
                rel_models = set()
                for field in model._meta.get_fields():
                    if isinstance(field, (related.ManyToManyField, related.ForeignKey)) and priority == 1:
                        is_rel_field = 1
                    if isinstance(field, (reverse_related.ManyToOneRel, reverse_related.ManyToManyRel)) and priority > 1:
                        is_rel_field = 1
                    if isinstance(field, (related.ManyToManyField, related.ForeignKey)) and priority > 1:
                        rel_models.add(field.related_model)

                if not rel_models <= exists_models_in_db and priority > 1:
                    is_rel_field = 1
                elif priority > 1:
                    is_rel_field = 0

                if is_rel_field == 0:
                    model_obj = ModelSetting.objects.create(
                        model=model,
                        name=model._meta.verbose_name,
                        priority=priority,
                    )
                    exists_models_in_db.add(model)
                    for field in model._meta.get_fields():
                        FieldSetting.objects.create(
                            model=model_obj,
                            name=field.name,
                            field=field,
                        )
                    models.remove(model)
