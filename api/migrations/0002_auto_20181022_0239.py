# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='worker',
            name='how_much_cigarettes',
            field=models.IntegerField(blank=True, null=True, verbose_name=b'\xc2\xbfCuantos cigarrillos al dia?', choices=[(0, b'De 1 a 5 cigarrillos'), (1, b'De 6 a 15 cigarrillos'), (2, b'16 o mas cigarrillos'), (3, b'3'), (4, b'4'), (5, b'5'), (6, b'6'), (7, b'7'), (8, b'8'), (9, b'9')]),
        ),
    ]
