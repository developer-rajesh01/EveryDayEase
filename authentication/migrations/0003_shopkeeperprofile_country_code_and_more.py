# Generated by Django 5.1.6 on 2025-03-27 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_profile_update_at_profile_user_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopkeeperprofile',
            name='country_code',
            field=models.CharField(choices=[('🇮🇳 India (+91)', '+91'), ('🇺🇸 USA (+1)', '+1'), ('🇬🇧 UK (+44)', '+44'), ('🇦🇺 Australia (+61)', '+61'), ('🇯🇵 Japan (+81)', '+81'), ('🇩🇪 Germany (+49)', '+49'), ('🇫🇷 France (+33)', '+33'), ('🇮🇹 Italy (+39)', '+39'), ('🇨🇳 China (+86)', '+86'), ('🇷🇺 Russia (+7)', '+7'), ('🇧🇷 Brazil (+55)', '+55'), ('🇦🇪 UAE (+971)', '+971'), ('🇿🇦 South Africa (+27)', '+27'), ('🇵🇰 Pakistan (+92)', '+92'), ('🇮🇩 Indonesia (+62)', '+62')], default='+91', max_length=25),
        ),
        migrations.AddField(
            model_name='shopkeeperprofile',
            name='email',
            field=models.EmailField(blank=True, max_length=254, unique=True),
        ),
        migrations.AddField(
            model_name='shopkeeperprofile',
            name='phone',
            field=models.CharField(blank=True, max_length=15, unique=True),
        ),
        migrations.AddField(
            model_name='shopkeeperprofile',
            name='profile',
            field=models.ImageField(blank=True, null=True, upload_to='profiles/'),
        ),
    ]
