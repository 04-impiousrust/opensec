from django.db import migrations


def add_default_categories(apps, schema_editor):
    Category = apps.get_model('resources', 'Category')
    categories = [
        'Web',
        'Networking',
        'Linux',
        'Operating Systems',
        'Security',
        'Tools',
        'Programming',
    ]
    for name in categories:
        Category.objects.get_or_create(name=name)


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_default_categories, migrations.RunPython.noop),
    ]
