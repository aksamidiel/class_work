# Generated by Django 2.2.7 on 2019-11-05 17:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0004_record_slug'),
    ]

    operations = [
        migrations.RunSQL("""UPDATE feed_record set slug=title""")
    ]

