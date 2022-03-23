# graphMonitor
Web interface for displaying switch data
### Description:
This is a django webserver for querying and displaying network traffic data from switches. Switch traffic is queried through telnet connections by sending the provided query to the switch and matching it with a provided regex to return input and output rates and units.

#### Data Input:
##### Switches Fields:
- **Name:** the name, used for display purposes
- **Interval:** an HH:MM:SS time interval to poll the switch at
- **Autostart:** a boolean that indicates whether to start polling at server startup
- **Address:** the domain or ipv4 address of the switch
- **Username:** the username to access the switch
- **Password:** the password to access the switch, this is encrypted with a unique key at rest

##### Commands Fields:
- **Switch:** the switch on which to run the command
- **Protocol:** the protocol to use to connect, currently only telnet is supported
- **Port:** the port on which to access the switch
- **Query:** the command to send to the switch that will return input and output rates and units
- **Query Regex:** a regex that will match and place the input and output rates and units in named capture groups
    - To name a regex capture group, place "?P<capture_name>" at the start of your capture groups, where your capture names would be input_unit, input_rate, output_unit, and output_rate
- **Rate:** a boolean that indicates whether the returned data should be interpreted as a rate
- **Query Interval:** the interval of time the query covers
- Bash Prompt: the bash prompt displayed by a telnet connection
- Login Prompt: the login prompt displayed by a telnet connection
- Password Prompt: the password prompt displayed by a telnet connection

##### Device Fields:
- **Switch:** the switch the device is connected to
- **Name:** the name, used for display purposes
- **Port:** the port, as identified by the switch and placed in the query when a command is sent

#### File Contents:

