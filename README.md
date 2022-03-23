# graphMonitor
#### Name:
Kai McGregor
#### Location:
Raleigh NC, USA

#### Video Demo: someurlhere
### Description:
This is a django webserver for querying and displaying network traffic data from switches. Switch traffic is queried through telnet connections by sending the provided query to the switch and matching it with a provided regex to return input and output rates and units.
This is done to provide flexibility in the software being run on the switch, but comes at the cost of a more involved setup process.

Graph display is done through Chart.js while bootstrap provides a clean layout and interface.

Scheduling is done through the python threading class and utilizes timers for low-overhead. This method was chosen over cron jobs and pythons Celery library as it is platform independant and doesn't require the additional setup of workers.

### Data Input:
**Underlined fields are required**

#### Switches Fields:
- <ins>Name:</ins> the name, used for display purposes
- <ins>Interval:</ins> an HH:MM:SS time interval to poll the switch at
- <ins>Autostart:</ins> a boolean that indicates whether to start polling at server startup
- <ins>Address:</ins> the domain or ipv4 address of the switch
- <ins>Username:</ins> the username to access the switch
- <ins>Password:</ins> the password to access the switch, this is encrypted with a unique key at rest

#### Commands Fields:
- <ins>Switch:</ins> the switch on which to run the command
- <ins>Protocol:</ins> the protocol to use to connect, currently only telnet is supported
- <ins>Port:</ins> the port on which to access the switch
- <ins>Query:</ins> the command to send to the switch that will return input and output rates and units
- <ins>Query Regex:</ins> a regex that will match and place the input and output rates and units in named capture groups
    - To name a regex capture group, place "?P<capture_name>" at the start of your capture groups, where your capture names would be input_unit, input_rate, output_unit, and output_rate
- <ins>Rate:</ins> a boolean that indicates whether the returned data should be interpreted as a rate
- <ins>Query Interval:</ins> the interval of time the query covers
- Bash Prompt: the bash prompt displayed by a telnet connection
- Login Prompt: the login prompt displayed by a telnet connection
- Password Prompt: the password prompt displayed by a telnet connection

#### Device Fields:
- <ins>Switch:</ins> the switch the device is connected to
- <ins>Name:</ins> the name, used for display purposes
- <ins>Port:</ins> the port, as identified by the switch and placed in the query when a command is sent

### File Contents:
#### graphmonitor/dashboard:
- [static:](graphmonitor/dashboard/static) contains static css and javascript files
- [templates:](graphmonitor/dashboard/templates) contains html template files utlizing the django template language and its features
- [templatetags:](graphmonitor/dashboard/templatetags) contains a template tag for accessing items dictionary items by key with the django template language
- [apps.py:](graphmonitor/dashboard/apps.py) contains startup code for initializing the static object that holds the switch query process objects
- [connections.py:](graphmonitor/dashboard/connections.py) python code for querying switches over different protocols, currently only telnet
- [forms.py:](graphmonitor/dashboard/forms.py) django objects that aid in displaying and processing user input information
- [models.py:](graphmonitor/dashboard/models.py) django objects representing tables in a database
- [scheduler.py:](graphmonitor/dashboard/scheduler.py) contains a class for scheduling switch queries and a static class for holding and syncing access to said objects
- [urls.py:](graphmonitor/dashboard/urls.py) contains the registered paths for the application
- [validators.py:](graphmonitor/dashboard/validators.py) contains database field validators
- [views.py:](graphmonitor/dashboard/views.py) code to provide response to http requests

#### graphmonitor/graphmonitor:
- [settings.py:](graphmonitor/graphmonitor/settings.py) contains server settings such as the database connection and password encryption key
- [urls.py:](graphmonitor/graphmonitor/urls.py) contains the registered paths for the application
