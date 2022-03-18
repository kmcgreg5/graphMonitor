from django.apps import AppConfig
from django.db.backends.signals import connection_created
import os


class DashboardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dashboard'

    def ready(self):
        from dashboard.scheduler import Processes
        from dashboard.models import Switches
        from dashboard.connections import SwitchConnection

        # Prevents activation when executed in threads other than the main one
        if os.environ.get('RUN_MAIN', None) == 'true':
            switches = Switches.objects.all()
            for switch in switches:
                Processes.addProcess(switch.pk, switch.interval.total_seconds(), SwitchConnection.pollSwitchData)
                if switch.autostart is True:
                    Processes.startProcess(switch.pk)
