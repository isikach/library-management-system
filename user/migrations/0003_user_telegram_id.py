# Generated by Django 5.0.3 on 2024-04-02 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0002_alter_user_is_active"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="telegram_id",
            field=models.IntegerField(default=123456778, verbose_name="Telegram ID"),
            preserve_default=False,
        ),
    ]
