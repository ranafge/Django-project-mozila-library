# Generated by Django 2.2 on 2019-09-02 06:31

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0009_auto_20190830_1638'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bookinstance',
            options={'ordering': ['due_back'], 'permissions': (('can_mark_returned', 'set book as returned'), ('can_mark_retunred_admin', 'set book as returned admin'))},
        ),
        migrations.AlterField(
            model_name='bookinstance',
            name='id',
            field=models.UUIDField(default=uuid.UUID('142735bb-4dc4-4d4f-84c9-ab151ea5ee37'), help_text='Unique ID for this particular book across whole library', primary_key=True, serialize=False),
        ),
    ]
