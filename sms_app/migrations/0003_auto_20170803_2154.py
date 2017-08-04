# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sms_app', '0002_subscriber_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriber',
            name='language',
            field=models.CharField(max_length=3),
        ),
    ]
