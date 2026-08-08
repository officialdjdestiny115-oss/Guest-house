from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0002_room_image_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='rooms/'),
        ),
    ]
