from dashboard.models import Switches, Commands, Devices, DataPoints
from telnetlib import Telnet
import re

class ConvertNetUnits():
    @staticmethod
    def convertToBytes(data: float, unit: str, rate: bool, interval) -> int:
        unit_lower = unit.lower()
        if 'giga' in unit_lower or 'G' in unit:
            data = data * 1000000000
        elif 'mega' in unit_lower or 'M' in unit:
            data = data * 1000000
        elif 'kilo' in unit_lower or 'K' in unit:
            data = data * 1000

        if 'bit' in unit_lower or ('b' in unit and 'byte' not in unit_lower):
            data = data / 8.0
        
        if rate:
            if 'ps' in unit_lower or 'per sec' in unit_lower:
                data = data * interval.total_seconds()
            elif 'pm' in unit_lower or 'per min' in unit_lower:
                data = data * (interval.total_seconds() / 60.0)
              
        return data


class TelnetConnection:
    def __init__(self, id: int):
        self.switch = Switches.objects.get(pk=id)
        self.connection = None
        self.devices = Devices.objects.filter(switch=self.switch).order_by('port')

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, exc_tb):
        if self.connection is not None:
            try:
                self.sendString('exit')
                self.connection.read_all()
            finally:
                self.connection.close()


    def sendString(self, input: str):
        self.connection.write(input.encode('ascii') + b'\n')


    def login(self, command):
        self.connection = Telnet(self.switch.address, command.port)
        self.connection.read_until(command.login_prompt.encode('ascii'))
        self.sendString(self.switch.username)
        self.connection.read_until(command.password_prompt.encode('ascii'))
        self.sendString(self.switch.password)
        self.connection.read_until(command.bash_prompt.encode('ascii'))

    def queryData(self, command) -> list:
        new_data = []
        for device in self.devices:
            self.sendString(command.query.replace('[PORT]', device.port))
            response = self.connection.read_until(command.bash_prompt.encode('ascii')).decode('ascii')
            match = re.search(command.query_regex, response)
            if match is not None:
                input_bytes = ConvertNetUnits.convertToBytes(float(match.group('input_data')), match.group('input_unit'), command.rate, command.query_interval)
                output_bytes = ConvertNetUnits.convertToBytes(float(match.group('output_data')), match.group('output_unit'), command.rate, command.query_interval)

                new_data.append(DataPoints(device=device, interval=command.query_interval, input=True, bytes=input_bytes))
                new_data.append(DataPoints(device=device, interval=command.query_interval, input=False, bytes=output_bytes))
        
        return new_data if len(new_data) != 0 else None


class SSHConnection():
    pass


class SwitchConnection():
    @staticmethod
    def pollSwitchData(id: int):
        new_data = None
        for command in Commands.objects.filter(switch=Switches.objects.get(pk=id)).order_by('priority'):
            if command.protocol == 'telnet':
                with TelnetConnection(id) as switch:
                    switch.login(command)
                    new_data = switch.queryData(command)
                    if new_data is not None: break

            elif command.protocol == 'ssh':
                pass

        if new_data is not None:
            for data in new_data:
                data.save()
