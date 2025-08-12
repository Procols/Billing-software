from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0008_remove_booking_checkin_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='checkin_datetime',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='booking',
            name='invoice_number',
            field=models.CharField(blank=True, max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='booking',
            name='status',
            field=models.CharField(choices=[('booked', 'Booked'), ('pre_booked', 'Pre Booked'), ('completed', 'Completed')], default='pre_booked', max_length=20),
        ),
    ]
