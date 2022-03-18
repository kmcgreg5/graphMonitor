from django.apps import AppConfig
from django.db.backends.signals import connection_created
import os


def temp(id):
    pass


class DashboardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dashboard'

    def ready(self):
        from dashboard.scheduler import Processes
        from dashboard.models import Switches

        # Prevents activation when executed in threads other than the main one
        if os.environ.get('RUN_MAIN', None) == 'true':
            switches = Switches.objects.all()
            for switch in switches:
                Processes.addProcess(switch.pk, switch.interval.total_seconds(), temp)
                if switch.autostart is True:
                    Processes.startProcess(switch.pk)
