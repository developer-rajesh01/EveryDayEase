# Generated by Django 5.1.6 on 2025-03-27 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_shopkeeperprofile_country_code_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopkeeperprofile',
            name='gst_number',
            field=models.CharField(blank=True, max_length=15, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='shopkeeperprofile',
            name='country_code',
            field=models.CharField(choices=[('+91', '🇮🇳 India (+91)'), ('+1', ' USA (+1)'), ('+44', '🇬🇧 UK (+44)'), ('+61', '🇦🇺 Australia (+61)'), ('+81', '🇯🇵 Japan (+81)'), ('+49', '🇩🇪 Germany (+49)'), ('+33', '🇫🇷 France (+33)'), ('+39', '🇮🇹 Italy (+39)'), ('+86', '🇨🇳 China (+86)'), ('+7', ' Russia (+7)'), ('+55', '🇧🇷 Brazil (+55)'), ('+971', '🇦🇪 UAE (+971)'), ('+27', '🇿🇦 South Africa (+27)'), ('+92', '🇵🇰 Pakistan (+92)'), ('+62', '🇮🇩 Indonesia (+62)')], default='+91', max_length=25),
        ),
    ]
