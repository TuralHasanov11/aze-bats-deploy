# Generated by Django 4.2.2 on 2023-06-10 11:57

import administration.models
import core.helpers
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', administration.models.NameField(max_length=200)),
                ('url', models.URLField(blank=True, null=True)),
                ('author', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cover_image', administration.models.ImageField(upload_to=core.helpers.UploadImageStrategy.uploadTo)),
            ],
        ),
        migrations.CreateModel(
            name='SiteInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('facebook_link', models.URLField(blank=True, null=True)),
                ('instagram_link', models.URLField(blank=True, null=True)),
                ('youtube_link', models.URLField(blank=True, null=True)),
                ('banner_image', models.ImageField(blank=True, default='site/banner.jpg', null=True, upload_to='site/')),
                ('article_promo_image', models.ImageField(blank=True, default='site/article_promo_image.jpg', null=True, upload_to='site/')),
                ('bat_promo_image', models.ImageField(blank=True, default='site/bat_promo_image.jpg', null=True, upload_to='site/')),
                ('project_promo_image', models.ImageField(blank=True, default='site/project_promo_image.jpg', null=True, upload_to='site/')),
                ('site_info_promo_image', models.ImageField(blank=True, default='site/site_info_promo_image.jpg', null=True, upload_to='site/')),
                ('logo_image', models.ImageField(blank=True, default='site/logo.png', null=True, upload_to='site/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Site Infos',
            },
        ),
        migrations.CreateModel(
            name='SiteText',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', administration.models.LanguageField(choices=[('en', 'English'), ('az', 'Azerbaijani')], default='az', max_length=2)),
                ('about', models.TextField(blank=True, null=True)),
                ('banner', administration.models.RichTextEditorField(blank=True, null=True)),
                ('privacy_policy', administration.models.RichTextEditorField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Site Texts',
            },
        ),
        migrations.CreateModel(
            name='AuthorAttributes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', administration.models.NameField(max_length=200, unique=True)),
                ('description', administration.models.RichTextEditorField(blank=True, null=True)),
                ('language', administration.models.LanguageField(choices=[('en', 'English'), ('az', 'Azerbaijani')], default='az', max_length=2)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author_attributes', to='base.author')),
            ],
        ),
    ]
