# Generated by Django 4.0.3 on 2022-03-17 21:34

import dashboard.validators
from django.db import migrations, models
import django.db.models.deletion
import encrypted_model_fields.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Switches',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Unknown', max_length=255)),
                ('interval', models.DurationField(help_text='How often to poll the switch for data.')),
                ('autostart', models.BooleanField(default=True)),
                ('address', models.CharField(help_text='The domain or IPv4 address of the switch.', max_length=255, unique=True, validators=[dashboard.validators.validate_domain_or_ipv4])),
                ('username', models.CharField(max_length=255)),
                ('password', encrypted_model_fields.fields.EncryptedCharField()),
            ],
        ),
        migrations.CreateModel(
            name='Devices',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Unknown', max_length=255)),
                ('port', models.CharField(help_text='The port as identified by the switch.', max_length=20)),
                ('switch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.switches')),
            ],
            options={
                'unique_together': {('switch', 'port')},
            },
        ),
        migrations.CreateModel(
            name='DataPoints',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('interval', models.DurationField()),
                ('bytes', models.BigIntegerField()),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.devices')),
            ],
        ),
        migrations.CreateModel(
            name='Commands',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('protocol', models.CharField(choices=[('telnet', 'Telnet'), ('ssh', 'SSH')], default='telnet', max_length=10)),
                ('port', models.IntegerField(default=23, help_text='The port to connect on.')),
                ('priority', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default=1, help_text='The priority for fallback connections, lower is preferred.')),
                ('query', models.CharField(help_text='The command to pull info for a port.', max_length=255, validators=[dashboard.validators.validate_query])),
                ('query_regex', models.CharField(help_text='A regex capturing transfer size and unit info in capture groups as needed.', max_length=255, validators=[dashboard.validators.validate_regex])),
                ('query_unit', models.CharField(choices=[('full', 'Auto (Full: bytes)'), ('short', 'Auto (Short: B)'), ('GB', 'Gigabytes'), ('Gb', 'Gigabits'), ('MB', 'Megabytes'), ('Mb', 'Megabits'), ('KB', 'Kilobytes'), ('Kb', 'Kilobits'), ('B', 'Bytes'), ('b', 'Bits')], help_text='The unit to be expected from the query.', max_length=10)),
                ('query_interval', models.DurationField(help_text='The interval that the query covers.')),
                ('login_prompt', models.CharField(blank=True, help_text='Unique charectors that match the login prompt for telnet connections.', max_length=255)),
                ('password_prompt', models.CharField(blank=True, help_text='Unique charectors that match the password prompt for telnet connections.', max_length=255)),
                ('switch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.switches')),
            ],
            options={
                'unique_together': {('switch', 'priority')},
            },
        ),
    ]
