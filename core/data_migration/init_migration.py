from core.data_migration.const import LANGUAGES, TECHNOLOGIES


def fill_languages(apps, schema_editor):
    Language = apps.get_model('core', 'Language')

    Language.objects.bulk_create([Language(name=language) for language in LANGUAGES])


def fill_technologies(apps, schema_editor):
    Technology = apps.get_model('core', 'Technology')

    Technology.objects.bulk_create([Technology(**tech) for tech in TECHNOLOGIES])
