from dashboard.models import Switches, Commands, Devices, DataPoints
from telnetlib import Telnet
import re

class convertNetUnits():
    @staticmethod
    def convertToBytes(data: int, unit: str, expected_unit: str) -> int:
        unit_lower = unit.lower()
        if 'giga' in unit_lower or 'G' in unit:
            data = data * 1000000000
        elif 'mega' in unit_lower or 'M' in unit:
            data = data * 1000000
        elif 'kilo' in unit_lower or 'K' in unit:
            data = data * 1000

        if 'bit' in unit_lower or 'b' in unit:
            data = data / 8
        
        return data

    @staticmethod
    def convertToBytes(data: int, expected_unit: str) -> int:
        if 'G' in expected_unit:
            data = data * 1000000000
        elif 'M' in expected_unit:
            data = data * 1000000
        elif 'K' in expected_unit:
            data = data * 1000

        if 'b' in expected_unit:
            data = data / 8
        
        return data

class TelnetConnection():
    def __enter__(self, id: int):
        self.connection = None
        self.switch = Switches.objects.get(pk=id)
        self.devices = Devices.objects.filter(switch=self.switch).order_by('port')

        return self
    
    def __exit__(self):
        if self.connection is not None:
            sendString('exit')
            self.connection.read_all()
            self.connection.close()


    def sendString(self, input: str):
        self.connection.write(command.encode('ascii') + b'\n')


    def login(self, command):
        self.connection = Telnet(self.switch.address, command.port)
        self.connection.read_until(command.login_prompt.encode('ascii'))
        sendString(switch.username)
        self.connection.read_until(command.password_prompt.encode('ascii'))
        sendString(switch.password)
        # Read for 1 sec to clear pipe
        self.connection.read_until(b"`!@#", 1)

    def queryData(self, command) -> list:
        for device in self.devices:
            sendString(command.query.replace('[PORT]', device.port))

        sendString('exit')
        data = self.connection.read_all()
        self.connection.close()
        self.connection = None

        
        matches = re.findall(command.query_regex, data)
        if len(matches) != self.devices.count():
            print("[ERROR] The number of matches does not match the number of devices.")
            return None

        new_data = []
        for match, device in zip(matches, self.devices):
            # Two capture groups
            if type(match) == tuple:
                bytes = int(match[0].replace(',', ''))
                unit = match[1]
                bytes = ConvertNetUnits.convertToBytes(bytes, unit, command.query_unit)
            # One capture group
            else:
                bytes = int(match.replace(',', ''))
                bytes = ConvertNetUnits.convertToBytes(bytes, command.query_unit)

            new_data.append(DataPoints(device=device, interval=command.query_interval, bytes=bytes))
        
        return new_data


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
                    new_data = switch.querydata(command)
                    if new_data is not None: break

            elif command.protocol == 'ssh':
                pass
        
        if new_data is not None:
            print(new_data)
            #for data in new_data:
            #    data.save()
