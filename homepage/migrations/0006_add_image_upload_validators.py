from django.db import migrations, models

import homepage.validators


class Migration(migrations.Migration):
    dependencies = [
        ('homepage', '0005_article_created_at_article_updated_at_author_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='image',
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to='news/',
                validators=[homepage.validators.validate_image_upload],
            ),
        ),
        migrations.AlterField(
            model_name='shortcut',
            name='image',
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to='shortcuts/',
                validators=[homepage.validators.validate_image_upload],
            ),
        ),
    ]
