# Generated by Django 3.2.9 on 2021-12-11 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exhibitions', '0007_auto_20211211_1853'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cooprequest',
            name='visitor',
            field=models.ManyToManyField(null=True, related_name='coop_request', to='exhibitions.Visitor'),
        ),
        migrations.AlterField(
            model_name='products',
            name='visitor',
            field=models.ManyToManyField(null=True, related_name='products_request', to='exhibitions.Visitor'),
        ),
    ]
