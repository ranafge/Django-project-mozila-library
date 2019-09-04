# Generated by Django 2.2 on 2019-08-26 13:57

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0006_auto_20190826_1445'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookinstance',
            name='id',
            field=models.UUIDField(default=uuid.UUID('58e9696f-bc21-4c69-bfbf-fff615f2284f'), help_text='Unique ID for this particular book across whole library', primary_key=True, serialize=False),
        ),
    ]
