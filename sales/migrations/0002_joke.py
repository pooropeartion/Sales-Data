# Generated by Django 5.1.2 on 2024-10-30 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Joke',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('setup', models.CharField(blank=True, max_length=255, null=True)),
                ('punchline', models.CharField(blank=True, max_length=255, null=True)),
                ('joke_text', models.TextField(blank=True, null=True)),
                ('category', models.CharField(max_length=50)),
                ('type', models.CharField(max_length=50)),
                ('nsfw', models.BooleanField(default=False)),
                ('political', models.BooleanField(default=False)),
                ('sexist', models.BooleanField(default=False)),
                ('safe', models.BooleanField(default=False)),
                ('lang', models.CharField(max_length=10)),
            ],
        ),
    ]
